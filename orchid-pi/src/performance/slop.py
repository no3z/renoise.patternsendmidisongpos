"""
Slop Performance Mode for Orchid-Pi
Adds human-like imperfections to timing and velocity
"""

import time
import random
import threading
from typing import List, Optional
from .base_mode import PerformanceMode
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from midi.midi_router import MIDIRouter


class SlopMode(PerformanceMode):
    """
    Slop mode: adds human imperfections
    - Timing variation
    - Velocity variation
    - Optional pitch micro-detuning
    """

    def __init__(self, midi_router: Optional[MIDIRouter] = None):
        super().__init__("Slop", midi_router)

        # Slop settings (variation ranges)
        self.timing_variation_ms = 10  # ±10ms timing variation
        self.velocity_variation_pct = 10  # ±10% velocity variation
        self.pitch_detune_cents = 0  # Pitch micro-detuning (disabled by default)

        # Thread control
        self.slop_thread = None
        self.stop_flag = False

    def set_timing_variation(self, ms: int):
        """Set timing variation in milliseconds (0-50ms)"""
        self.timing_variation_ms = max(0, min(50, ms))

    def set_velocity_variation(self, percent: int):
        """Set velocity variation percentage (0-30%)"""
        self.velocity_variation_pct = max(0, min(30, percent))

    def set_pitch_detune(self, cents: int):
        """Set pitch detuning in cents (0-50)"""
        self.pitch_detune_cents = max(0, min(50, cents))

    def humanize_velocity(self, velocity: int) -> int:
        """Add random variation to velocity"""
        if self.velocity_variation_pct == 0:
            return velocity

        # Calculate variation range
        variation = int(velocity * (self.velocity_variation_pct / 100.0))

        # Apply random variation
        humanized = velocity + random.randint(-variation, variation)

        # Clamp to valid MIDI range
        return max(1, min(127, humanized))

    def get_timing_delay(self) -> float:
        """Get random timing delay in seconds"""
        if self.timing_variation_ms == 0:
            return 0.0

        # Random delay ± timing_variation_ms
        delay_ms = random.uniform(-self.timing_variation_ms, self.timing_variation_ms)

        # Convert to seconds and ensure non-negative
        return max(0.0, delay_ms / 1000.0)

    def process(self, notes: List[int], velocity: int = 100):
        """
        Process notes with humanization

        Args:
            notes: List of MIDI note numbers
            velocity: Base note velocity
        """
        if not self.enabled or not self.midi_router or not notes:
            return

        # Stop any ongoing process
        self.stop()

        # Start slop processing in thread
        self.stop_flag = False
        self.slop_thread = threading.Thread(
            target=self._process_slop_notes,
            args=(notes, velocity)
        )
        self.slop_thread.daemon = True
        self.slop_thread.start()

    def _process_slop_notes(self, notes: List[int], base_velocity: int):
        """Internal method to process notes with humanization"""

        # Process each note with individual humanization
        for note in notes:
            if self.stop_flag:
                break

            # Humanize velocity
            velocity = self.humanize_velocity(base_velocity)

            # Apply timing delay
            delay = self.get_timing_delay()
            if delay > 0:
                time.sleep(delay)

            # Send note via performance channel
            # Note: Pitch detune would require pitch bend messages
            # For now, we'll send the note as-is
            self.midi_router.send_performance_note(note, velocity)

            # Small delay between notes for natural feel
            time.sleep(0.002)  # 2ms between note triggers

    def stop(self):
        """Stop ongoing processing"""
        self.stop_flag = True

        # Wait for thread to finish
        if self.slop_thread and self.slop_thread.is_alive():
            self.slop_thread.join(timeout=0.5)

        # Stop all performance notes
        if self.midi_router:
            self.midi_router.stop_all_performance_notes()


if __name__ == '__main__':
    # Test slop mode
    from midi.midi_processor import MIDIProcessor

    print("Slop Mode Test\n" + "=" * 50)

    processor = MIDIProcessor()
    router = MIDIRouter(processor)

    # Setup MIDI output
    if processor.get_available_output_ports():
        processor.open_output_port(0)
    else:
        processor.create_virtual_output("Orchid-Pi Slop Test")

    print(f"MIDI Output: {processor.output_port}")

    # Create slop mode
    slop = SlopMode(router)
    slop.enable()

    cmaj7 = [60, 64, 67, 71]  # C, E, G, B

    print("\n1. No humanization (baseline)")
    slop.set_timing_variation(0)
    slop.set_velocity_variation(0)
    for i in range(3):
        slop.process(cmaj7, velocity=100)
        time.sleep(1)
        slop.stop()
        time.sleep(0.5)

    print("\n2. Timing variation (±10ms)")
    slop.set_timing_variation(10)
    slop.set_velocity_variation(0)
    for i in range(3):
        slop.process(cmaj7, velocity=100)
        time.sleep(1)
        slop.stop()
        time.sleep(0.5)

    print("\n3. Velocity variation (±15%)")
    slop.set_timing_variation(0)
    slop.set_velocity_variation(15)
    for i in range(3):
        slop.process(cmaj7, velocity=100)
        time.sleep(1)
        slop.stop()
        time.sleep(0.5)

    print("\n4. Both timing and velocity variation")
    slop.set_timing_variation(10)
    slop.set_velocity_variation(15)
    for i in range(3):
        slop.process(cmaj7, velocity=100)
        time.sleep(1)
        slop.stop()
        time.sleep(0.5)

    print("\nTest complete!")
    processor.close()
