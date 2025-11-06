"""
Arpeggiator Performance Mode for Orchid-Pi
Plays chord notes in sequence at a specific tempo
"""

import time
import threading
from typing import List, Optional
from .base_mode import PerformanceMode
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from midi.midi_router import MIDIRouter


class ArpeggiatorMode(PerformanceMode):
    """
    Arpeggiator mode: plays chord notes in rhythmic sequence
    """

    def __init__(self, midi_router: Optional[MIDIRouter] = None):
        super().__init__("Arpeggiator", midi_router)

        # Arp settings
        self.pattern = 'up'  # 'up', 'down', 'up-down', 'down-up', 'random', 'as-played'
        self.rate = '1/8'  # '1/4', '1/8', '1/16', '1/32'
        self.octaves = 1  # 1-4 octaves
        self.gate = 0.8  # Note length as fraction of interval (0.1-1.0)
        self.bpm = 120  # Tempo

        # Runtime state
        self.arp_thread = None
        self.stop_flag = False
        self.running = False

        # Note tracking
        self.current_notes = []
        self.last_note_sent = None

    def set_pattern(self, pattern: str):
        """Set arpeggiator pattern"""
        valid_patterns = ['up', 'down', 'up-down', 'down-up', 'random', 'as-played']
        if pattern in valid_patterns:
            self.pattern = pattern

    def set_rate(self, rate: str):
        """Set arpeggiator rate (note division)"""
        valid_rates = ['1/4', '1/8', '1/16', '1/32']
        if rate in valid_rates:
            self.rate = rate

    def set_octaves(self, octaves: int):
        """Set number of octaves to arpeggiate (1-4)"""
        self.octaves = max(1, min(4, octaves))

    def set_gate(self, gate: float):
        """Set gate length (0.1-1.0, where 1.0 = legato)"""
        self.gate = max(0.1, min(1.0, gate))

    def set_bpm(self, bpm: int):
        """Set tempo in BPM"""
        self.bpm = max(20, min(300, bpm))

    def get_interval(self) -> float:
        """Calculate interval between notes in seconds"""
        # Calculate beats per second
        beats_per_second = self.bpm / 60.0

        # Calculate interval based on rate
        rate_multipliers = {
            '1/4': 1.0,
            '1/8': 2.0,
            '1/16': 4.0,
            '1/32': 8.0
        }

        multiplier = rate_multipliers.get(self.rate, 2.0)
        interval = 1.0 / (beats_per_second * multiplier)

        return interval

    def generate_arp_sequence(self, notes: List[int]) -> List[int]:
        """Generate arpeggiated note sequence"""
        if not notes:
            return []

        base_notes = sorted(notes)

        # Extend across octaves if needed
        if self.octaves > 1:
            extended = []
            for octave in range(self.octaves):
                extended.extend([n + (12 * octave) for n in base_notes])
            base_notes = [n for n in extended if n <= 127]  # Filter valid MIDI range

        # Apply pattern
        if self.pattern == 'up':
            sequence = base_notes
        elif self.pattern == 'down':
            sequence = sorted(base_notes, reverse=True)
        elif self.pattern == 'up-down':
            sequence = base_notes + sorted(base_notes, reverse=True)[1:-1]
        elif self.pattern == 'down-up':
            down = sorted(base_notes, reverse=True)
            sequence = down + sorted(base_notes)[1:-1]
        elif self.pattern == 'random':
            import random
            sequence = list(base_notes)
            random.shuffle(sequence)
        else:  # 'as-played'
            sequence = list(notes)  # Keep original order

        return sequence

    def process(self, notes: List[int], velocity: int = 100):
        """
        Start arpeggiating notes

        Args:
            notes: List of MIDI note numbers
            velocity: Note velocity
        """
        if not self.enabled or not self.midi_router or not notes:
            return

        # Stop any ongoing arpeggio
        self.stop()

        # Store notes for arpeggiation
        self.current_notes = list(notes)

        # Start arpeggiator thread
        self.stop_flag = False
        self.running = True
        self.arp_thread = threading.Thread(
            target=self._arpeggiator_loop,
            args=(notes, velocity)
        )
        self.arp_thread.daemon = True
        self.arp_thread.start()

    def _arpeggiator_loop(self, notes: List[int], velocity: int):
        """Internal arpeggiator loop"""
        sequence = self.generate_arp_sequence(notes)

        if not sequence:
            return

        index = 0
        interval = self.get_interval()
        gate_time = interval * self.gate

        while not self.stop_flag:
            # Get current note
            note = sequence[index % len(sequence)]

            # Turn off previous note
            if self.last_note_sent is not None:
                self.midi_router.stop_performance_note(self.last_note_sent)

            # Send current note
            self.midi_router.send_performance_note(note, velocity)
            self.last_note_sent = note

            # Wait for gate time
            time.sleep(gate_time)

            # Turn off note if gate < 1.0 (non-legato)
            if self.gate < 1.0:
                self.midi_router.stop_performance_note(note)
                self.last_note_sent = None

                # Wait for remaining interval
                time.sleep(interval - gate_time)
            else:
                # Legato: wait full interval
                time.sleep(interval - gate_time)

            # Move to next note
            index += 1

        # Turn off last note when stopping
        if self.last_note_sent is not None:
            self.midi_router.stop_performance_note(self.last_note_sent)
            self.last_note_sent = None

    def stop(self):
        """Stop arpeggiator"""
        self.stop_flag = True
        self.running = False

        # Wait for thread to finish
        if self.arp_thread and self.arp_thread.is_alive():
            self.arp_thread.join(timeout=0.5)

        # Stop all performance notes
        if self.midi_router:
            self.midi_router.stop_all_performance_notes()

        self.last_note_sent = None


if __name__ == '__main__':
    # Test arpeggiator
    from midi.midi_processor import MIDIProcessor

    print("Arpeggiator Mode Test\n" + "=" * 50)

    processor = MIDIProcessor()
    router = MIDIRouter(processor)

    # Setup MIDI output
    if processor.get_available_output_ports():
        processor.open_output_port(0)
    else:
        processor.create_virtual_output("Orchid-Pi Arp Test")

    print(f"MIDI Output: {processor.output_port}")

    # Create arpeggiator
    arp = ArpeggiatorMode(router)
    arp.enable()

    cmaj = [60, 64, 67]  # C, E, G

    print("\n1. Arp UP, 1/8 notes, 120 BPM")
    arp.set_pattern('up')
    arp.set_rate('1/8')
    arp.set_bpm(120)
    arp.process(cmaj, velocity=100)
    time.sleep(4)
    arp.stop()

    print("\n2. Arp UP-DOWN, 1/16 notes, 2 octaves")
    arp.set_pattern('up-down')
    arp.set_rate('1/16')
    arp.set_octaves(2)
    arp.process(cmaj, velocity=100)
    time.sleep(4)
    arp.stop()

    print("\n3. Arp RANDOM, 1/8 notes")
    arp.set_pattern('random')
    arp.set_rate('1/8')
    arp.set_octaves(1)
    arp.process(cmaj, velocity=100)
    time.sleep(4)
    arp.stop()

    print("\nTest complete!")
    processor.close()
