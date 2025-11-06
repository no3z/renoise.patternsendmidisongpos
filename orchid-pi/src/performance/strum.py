"""
Strum Performance Mode for Orchid-Pi
Plays chord notes with a slight delay between each (like guitar strum)
"""

import time
import threading
from typing import List, Optional
from .base_mode import PerformanceMode
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from midi.midi_router import MIDIRouter


class StrumMode(PerformanceMode):
    """
    Strum mode: plays chord notes sequentially with delay
    Simulates guitar strumming
    """

    def __init__(self, midi_router: Optional[MIDIRouter] = None):
        super().__init__("Strum", midi_router)

        # Strum settings
        self.delay_ms = 15  # Delay between notes in milliseconds
        self.direction = 'up'  # 'up', 'down', or 'random'

        # Thread control
        self.strum_thread = None
        self.stop_flag = False

    def set_delay(self, delay_ms: int):
        """Set delay between strummed notes (5-100ms)"""
        self.delay_ms = max(5, min(100, delay_ms))

    def set_direction(self, direction: str):
        """Set strum direction: 'up', 'down', or 'random'"""
        if direction in ['up', 'down', 'random']:
            self.direction = direction

    def process(self, notes: List[int], velocity: int = 100):
        """
        Process notes with strum effect

        Args:
            notes: List of MIDI note numbers
            velocity: Note velocity
        """
        if not self.enabled or not self.midi_router or not notes:
            return

        # Stop any ongoing strum
        self.stop()

        # Start new strum in separate thread (non-blocking)
        self.stop_flag = False
        self.strum_thread = threading.Thread(
            target=self._strum_notes,
            args=(notes, velocity)
        )
        self.strum_thread.daemon = True
        self.strum_thread.start()

    def _strum_notes(self, notes: List[int], velocity: int):
        """Internal method to strum notes with delay"""
        # Sort notes based on direction
        if self.direction == 'down':
            strum_notes = sorted(notes, reverse=True)  # High to low
        elif self.direction == 'random':
            import random
            strum_notes = list(notes)
            random.shuffle(strum_notes)
        else:  # 'up'
            strum_notes = sorted(notes)  # Low to high

        # Send notes with delay
        for i, note in enumerate(strum_notes):
            if self.stop_flag:
                break

            # Send via performance channel
            self.midi_router.send_performance_note(note, velocity)

            # Delay before next note (except for last note)
            if i < len(strum_notes) - 1:
                time.sleep(self.delay_ms / 1000.0)

    def stop(self):
        """Stop ongoing strum"""
        self.stop_flag = True

        # Wait for thread to finish
        if self.strum_thread and self.strum_thread.is_alive():
            self.strum_thread.join(timeout=0.5)

        # Stop all performance notes
        if self.midi_router:
            self.midi_router.stop_all_performance_notes()


if __name__ == '__main__':
    # Test strum mode
    from midi.midi_processor import MIDIProcessor

    print("Strum Mode Test\n" + "=" * 50)

    processor = MIDIProcessor()
    router = MIDIRouter(processor)

    # Setup MIDI output
    if processor.get_available_output_ports():
        processor.open_output_port(0)
    else:
        processor.create_virtual_output("Orchid-Pi Strum Test")

    print(f"MIDI Output: {processor.output_port}")

    # Create strum mode
    strum = StrumMode(router)
    strum.enable()

    # Test different settings
    cmaj7 = [60, 64, 67, 71]  # C, E, G, B

    print("\n1. Strum UP (15ms delay)")
    strum.set_direction('up')
    strum.set_delay(15)
    strum.process(cmaj7, velocity=100)
    time.sleep(2)
    strum.stop()

    print("\n2. Strum DOWN (25ms delay)")
    strum.set_direction('down')
    strum.set_delay(25)
    strum.process(cmaj7, velocity=100)
    time.sleep(2)
    strum.stop()

    print("\n3. Strum RANDOM (20ms delay)")
    strum.set_direction('random')
    strum.set_delay(20)
    strum.process(cmaj7, velocity=100)
    time.sleep(2)
    strum.stop()

    print("\nTest complete!")
    processor.close()
