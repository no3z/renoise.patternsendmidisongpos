"""
Pattern Performance Mode for Orchid-Pi
Plays chord notes in rhythmic patterns
"""

import time
import threading
from typing import List, Optional, Tuple
from .base_mode import PerformanceMode
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from midi.midi_router import MIDIRouter


class PatternMode(PerformanceMode):
    """
    Pattern mode: plays chord notes in predefined rhythmic patterns
    """

    def __init__(self, midi_router: Optional[MIDIRouter] = None):
        super().__init__("Pattern", midi_router)

        # Pattern settings
        self.bpm = 120
        self.current_pattern_name = 'basic'

        # Runtime state
        self.pattern_thread = None
        self.stop_flag = False
        self.running = False

        # Define rhythmic patterns
        # Each pattern is a list of tuples: (step, note_indices, duration)
        # step = timing in 16th notes (0-15)
        # note_indices = which notes from chord to play (0=root, 1=2nd, etc., -1=all)
        # duration = how long to hold (in 16th notes)
        self.patterns = {
            'basic': [
                (0, -1, 4),   # All notes on beat 1, hold for quarter note
                (4, -1, 4),   # All notes on beat 2
                (8, -1, 4),   # All notes on beat 3
                (12, -1, 4),  # All notes on beat 4
            ],
            'bounce': [
                (0, [0], 1),   # Root on 1
                (2, [1, 2], 1),  # Middle notes
                (4, [0], 1),   # Root on 2
                (6, [1, 2], 1),  # Middle notes
                (8, [0], 1),   # Root on 3
                (10, [1, 2], 1), # Middle notes
                (12, [0], 1),  # Root on 4
                (14, [1, 2], 1), # Middle notes
            ],
            'latin': [
                (0, -1, 2),    # All notes, short
                (3, [0], 1),   # Root, short
                (4, -1, 2),    # All notes
                (8, -1, 2),    # All notes
                (11, [0], 1),  # Root
                (12, -1, 2),   # All notes
            ],
            'reggae': [
                (2, -1, 2),    # Off-beat emphasis
                (6, -1, 2),
                (10, -1, 2),
                (14, -1, 2),
            ],
            'waltz': [
                (0, -1, 4),    # Beat 1 (strong)
                (4, [1, 2], 2),  # Beat 2 (weak)
                (8, [1, 2], 2),  # Beat 3 (weak)
            ],
            'broken': [
                (0, [0], 2),   # Root
                (2, [2], 2),   # 5th
                (4, [1], 2),   # 3rd
                (6, [3], 2),   # 7th (if exists)
                (8, [2], 2),   # 5th
                (10, [1], 2),  # 3rd
                (12, [0], 2),  # Root
                (14, [2], 2),  # 5th
            ],
            'arpeggio': [
                (0, [0], 2),   # Root
                (2, [1], 2),   # 2nd
                (4, [2], 2),   # 3rd
                (6, [3], 2),   # 4th
                (8, [2], 2),   # 3rd
                (10, [1], 2),  # 2nd
                (12, [0], 2),  # Root
                (14, [1], 2),  # 2nd
            ],
            'bossa': [
                (0, -1, 2),
                (3, [0, 1], 1),
                (6, -1, 2),
                (9, [0, 1], 1),
                (12, -1, 2),
                (15, [0, 1], 1),
            ],
        }

    def set_bpm(self, bpm: int):
        """Set tempo in BPM"""
        self.bpm = max(40, min(240, bpm))

    def set_pattern(self, pattern_name: str):
        """Set current pattern by name"""
        if pattern_name in self.patterns:
            self.current_pattern_name = pattern_name
            return True
        return False

    def get_available_patterns(self) -> List[str]:
        """Get list of available pattern names"""
        return list(self.patterns.keys())

    def get_sixteenth_note_duration(self) -> float:
        """Calculate duration of one 16th note in seconds"""
        # BPM = quarter notes per minute
        # 16th note = 1/4 of quarter note
        quarter_note_duration = 60.0 / self.bpm
        return quarter_note_duration / 4.0

    def process(self, notes: List[int], velocity: int = 100):
        """
        Start playing pattern with chord notes

        Args:
            notes: List of MIDI note numbers
            velocity: Note velocity
        """
        if not self.enabled or not self.midi_router or not notes:
            return

        # Stop any ongoing pattern
        self.stop()

        # Start pattern thread
        self.stop_flag = False
        self.running = True
        self.pattern_thread = threading.Thread(
            target=self._pattern_loop,
            args=(notes, velocity)
        )
        self.pattern_thread.daemon = True
        self.pattern_thread.start()

    def _get_notes_for_pattern_step(self, notes: List[int], note_indices) -> List[int]:
        """Get notes for a pattern step based on indices"""
        if note_indices == -1:
            # Play all notes
            return notes

        # Play specific note indices
        selected = []
        for idx in note_indices:
            if isinstance(idx, int) and 0 <= idx < len(notes):
                selected.append(notes[idx])

        return selected

    def _pattern_loop(self, notes: List[int], velocity: int):
        """Internal pattern loop"""
        pattern = self.patterns[self.current_pattern_name]
        sixteenth_duration = self.get_sixteenth_note_duration()

        # Sort notes for consistent indexing
        sorted_notes = sorted(notes)

        # Track active notes
        active_notes = []

        while not self.stop_flag:
            # Get current time reference
            loop_start = time.time()

            # Process each step in pattern
            for step, note_indices, duration in pattern:
                if self.stop_flag:
                    break

                # Calculate when this step should trigger
                step_time = loop_start + (step * sixteenth_duration)

                # Wait until step time
                current_time = time.time()
                if step_time > current_time:
                    time.sleep(step_time - current_time)

                # Stop currently active notes
                for note in active_notes:
                    self.midi_router.stop_performance_note(note)
                active_notes.clear()

                # Get notes for this step
                step_notes = self._get_notes_for_pattern_step(sorted_notes, note_indices)

                # Send new notes
                for note in step_notes:
                    self.midi_router.send_performance_note(note, velocity)
                    active_notes.append(note)

                # Calculate note-off time
                note_off_time = step_time + (duration * sixteenth_duration)

                # Schedule note-off (will happen in next iteration or at loop end)

            # Wait for pattern to complete (16 sixteenth notes = 1 bar)
            loop_end_time = loop_start + (16 * sixteenth_duration)
            current_time = time.time()
            if loop_end_time > current_time:
                time.sleep(loop_end_time - current_time)

            # Stop all active notes at end of loop
            for note in active_notes:
                self.midi_router.stop_performance_note(note)
            active_notes.clear()

    def stop(self):
        """Stop pattern playback"""
        self.stop_flag = True
        self.running = False

        # Wait for thread to finish
        if self.pattern_thread and self.pattern_thread.is_alive():
            self.pattern_thread.join(timeout=0.5)

        # Stop all performance notes
        if self.midi_router:
            self.midi_router.stop_all_performance_notes()


if __name__ == '__main__':
    # Test pattern mode
    from midi.midi_processor import MIDIProcessor

    print("Pattern Mode Test\n" + "=" * 50)

    processor = MIDIProcessor()
    router = MIDIRouter(processor)

    # Setup MIDI output
    if processor.get_available_output_ports():
        processor.open_output_port(0)
    else:
        processor.create_virtual_output("Orchid-Pi Pattern Test")

    print(f"MIDI Output: {processor.output_port}")

    # Create pattern mode
    pattern = PatternMode(router)
    pattern.enable()
    pattern.set_bpm(120)

    cmaj7 = [60, 64, 67, 71]  # C, E, G, B

    # Test different patterns
    patterns_to_test = ['basic', 'bounce', 'latin', 'reggae']

    for pattern_name in patterns_to_test:
        print(f"\nPlaying pattern: {pattern_name}")
        pattern.set_pattern(pattern_name)
        pattern.process(cmaj7, velocity=100)
        time.sleep(4)  # Play for 4 seconds
        pattern.stop()
        time.sleep(1)

    print("\nTest complete!")
    processor.close()
