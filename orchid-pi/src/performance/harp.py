"""
Harp Performance Mode for Orchid-Pi
Plays notes in a glissando style (like harp sweep)
"""

import time
import threading
from typing import List, Optional
from .base_mode import PerformanceMode
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from midi.midi_router import MIDIRouter


class HarpMode(PerformanceMode):
    """
    Harp mode: plays notes in glissando sweep
    Simulates harp-like cascading notes with natural decay
    """

    def __init__(self, midi_router: Optional[MIDIRouter] = None):
        super().__init__("Harp", midi_router)

        # Harp settings
        self.sweep_time_ms = 100  # Total time for full sweep (50-500ms)
        self.direction = 'up'  # 'up' or 'down'
        self.velocity_decay = True  # Gradually reduce velocity
        self.note_length_ms = 500  # How long each note rings (100-2000ms)

        # Thread control
        self.harp_thread = None
        self.stop_flag = False

    def set_sweep_time(self, ms: int):
        """Set sweep time in milliseconds (50-500ms)"""
        self.sweep_time_ms = max(50, min(500, ms))

    def set_direction(self, direction: str):
        """Set sweep direction: 'up' or 'down'"""
        if direction in ['up', 'down']:
            self.direction = direction

    def set_velocity_decay(self, enabled: bool):
        """Enable/disable velocity decay across sweep"""
        self.velocity_decay = enabled

    def set_note_length(self, ms: int):
        """Set how long notes ring (100-2000ms)"""
        self.note_length_ms = max(100, min(2000, ms))

    def process(self, notes: List[int], velocity: int = 100):
        """
        Process notes with harp glissando effect

        Args:
            notes: List of MIDI note numbers
            velocity: Starting velocity
        """
        if not self.enabled or not self.midi_router or not notes:
            return

        # Stop any ongoing harp
        self.stop()

        # Start new harp sweep in thread
        self.stop_flag = False
        self.harp_thread = threading.Thread(
            target=self._harp_sweep,
            args=(notes, velocity)
        )
        self.harp_thread.daemon = True
        self.harp_thread.start()

    def _harp_sweep(self, notes: List[int], base_velocity: int):
        """Internal method to perform harp sweep"""

        # Sort notes based on direction
        if self.direction == 'down':
            sweep_notes = sorted(notes, reverse=True)  # High to low
        else:  # 'up'
            sweep_notes = sorted(notes)  # Low to high

        num_notes = len(sweep_notes)
        if num_notes == 0:
            return

        # Calculate delay between notes
        delay_between_notes = self.sweep_time_ms / (num_notes * 1000.0)

        # Calculate velocity decay per note
        velocity_step = 0
        if self.velocity_decay and num_notes > 1:
            # Decay from full velocity to ~70% by end
            velocity_range = base_velocity * 0.3
            velocity_step = velocity_range / (num_notes - 1)

        # Track notes for later cleanup
        triggered_notes = []

        # Trigger notes in sequence
        for i, note in enumerate(sweep_notes):
            if self.stop_flag:
                break

            # Calculate velocity with decay
            if self.velocity_decay:
                note_velocity = int(base_velocity - (i * velocity_step))
            else:
                note_velocity = base_velocity

            note_velocity = max(1, min(127, note_velocity))

            # Send note
            self.midi_router.send_performance_note(note, note_velocity)
            triggered_notes.append((note, time.time()))

            # Delay before next note
            if i < num_notes - 1:
                time.sleep(delay_between_notes)

        # Let notes ring for note_length duration
        # Then turn off notes that have exceeded their length
        note_length_seconds = self.note_length_ms / 1000.0

        while triggered_notes and not self.stop_flag:
            current_time = time.time()
            notes_to_remove = []

            for note, trigger_time in triggered_notes:
                # Check if note has been ringing long enough
                if current_time - trigger_time >= note_length_seconds:
                    self.midi_router.stop_performance_note(note)
                    notes_to_remove.append((note, trigger_time))

            # Remove stopped notes from tracking
            for note_info in notes_to_remove:
                triggered_notes.remove(note_info)

            # Small sleep to avoid busy loop
            time.sleep(0.05)

    def stop(self):
        """Stop harp sweep"""
        self.stop_flag = True

        # Wait for thread to finish
        if self.harp_thread and self.harp_thread.is_alive():
            self.harp_thread.join(timeout=0.5)

        # Stop all performance notes
        if self.midi_router:
            self.midi_router.stop_all_performance_notes()


if __name__ == '__main__':
    # Test harp mode
    from midi.midi_processor import MIDIProcessor

    print("Harp Mode Test\n" + "=" * 50)

    processor = MIDIProcessor()
    router = MIDIRouter(processor)

    # Setup MIDI output
    if processor.get_available_output_ports():
        processor.open_output_port(0)
    else:
        processor.create_virtual_output("Orchid-Pi Harp Test")

    print(f"MIDI Output: {processor.output_port}")

    # Create harp mode
    harp = HarpMode(router)
    harp.enable()

    # Test with larger chord for more dramatic effect
    cmaj9 = [60, 64, 67, 71, 74]  # C, E, G, B, D

    print("\n1. Harp sweep UP (100ms, with decay)")
    harp.set_direction('up')
    harp.set_sweep_time(100)
    harp.set_velocity_decay(True)
    harp.set_note_length(1000)
    harp.process(cmaj9, velocity=100)
    time.sleep(2)
    harp.stop()

    print("\n2. Harp sweep DOWN (150ms, with decay)")
    harp.set_direction('down')
    harp.set_sweep_time(150)
    harp.process(cmaj9, velocity=100)
    time.sleep(2)
    harp.stop()

    print("\n3. Fast harp UP (50ms, no decay)")
    harp.set_direction('up')
    harp.set_sweep_time(50)
    harp.set_velocity_decay(False)
    harp.process(cmaj9, velocity=100)
    time.sleep(2)
    harp.stop()

    print("\n4. Slow harp UP (300ms, with decay, long notes)")
    harp.set_direction('up')
    harp.set_sweep_time(300)
    harp.set_velocity_decay(True)
    harp.set_note_length(2000)
    harp.process(cmaj9, velocity=100)
    time.sleep(3)
    harp.stop()

    print("\nTest complete!")
    processor.close()
