"""
MIDI Router for Orchid-Pi
Routes MIDI messages to different channels (chords, bass, performance)
"""

import time
from typing import List, Optional
from .midi_processor import MIDIProcessor


class MIDIRouter:
    """
    Routes processed MIDI to multiple channels
    Channel 1: Chords
    Channel 2: Bass
    Channel 3: Performance notes
    """

    def __init__(self, midi_processor: Optional[MIDIProcessor] = None):
        self.midi_processor = midi_processor or MIDIProcessor()

        # Channel assignments
        self.chord_channel = 1
        self.bass_channel = 2
        self.performance_channel = 3

        # Active notes tracking (for note off messages)
        self.active_chord_notes = set()
        self.active_bass_note = None
        self.active_performance_notes = set()

        # Routing settings
        self.chord_enabled = True
        self.bass_enabled = True
        self.performance_enabled = True

    def set_chord_channel(self, channel: int):
        """Set MIDI channel for chord output (1-16)"""
        self.chord_channel = max(1, min(16, channel))

    def set_bass_channel(self, channel: int):
        """Set MIDI channel for bass output (1-16)"""
        self.bass_channel = max(1, min(16, channel))

    def set_performance_channel(self, channel: int):
        """Set MIDI channel for performance notes (1-16)"""
        self.performance_channel = max(1, min(16, channel))

    def send_chord(self, notes: List[int], velocity: int = 100, channel: Optional[int] = None):
        """
        Send chord notes to chord channel

        Args:
            notes: List of MIDI note numbers
            velocity: Note velocity (0-127)
            channel: Override default chord channel
        """
        if not self.chord_enabled:
            return

        ch = channel or self.chord_channel

        # Turn off any previously active chord notes first
        self.stop_chord()

        # Send new chord notes
        for note in notes:
            self.midi_processor.send_note_on(note, velocity, ch)
            self.active_chord_notes.add(note)

    def stop_chord(self, channel: Optional[int] = None):
        """Stop all active chord notes"""
        ch = channel or self.chord_channel

        for note in self.active_chord_notes:
            self.midi_processor.send_note_off(note, ch)

        self.active_chord_notes.clear()

    def send_bass(self, note: int, velocity: int = 100, channel: Optional[int] = None):
        """
        Send bass note to bass channel

        Args:
            note: MIDI note number
            velocity: Note velocity (0-127)
            channel: Override default bass channel
        """
        if not self.bass_enabled or note is None:
            return

        ch = channel or self.bass_channel

        # Stop previous bass note
        self.stop_bass()

        # Send new bass note
        self.midi_processor.send_note_on(note, velocity, ch)
        self.active_bass_note = note

    def stop_bass(self, channel: Optional[int] = None):
        """Stop active bass note"""
        if self.active_bass_note is None:
            return

        ch = channel or self.bass_channel
        self.midi_processor.send_note_off(self.active_bass_note, ch)
        self.active_bass_note = None

    def send_performance_note(self, note: int, velocity: int = 100,
                              channel: Optional[int] = None):
        """
        Send performance note to performance channel

        Args:
            note: MIDI note number
            velocity: Note velocity (0-127)
            channel: Override default performance channel
        """
        if not self.performance_enabled:
            return

        ch = channel or self.performance_channel
        self.midi_processor.send_note_on(note, velocity, ch)
        self.active_performance_notes.add(note)

    def stop_performance_note(self, note: int, channel: Optional[int] = None):
        """Stop specific performance note"""
        ch = channel or self.performance_channel
        self.midi_processor.send_note_off(note, ch)

        if note in self.active_performance_notes:
            self.active_performance_notes.remove(note)

    def stop_all_performance_notes(self, channel: Optional[int] = None):
        """Stop all active performance notes"""
        ch = channel or self.performance_channel

        for note in self.active_performance_notes:
            self.midi_processor.send_note_off(note, ch)

        self.active_performance_notes.clear()

    def send_chord_with_bass(self, chord_notes: List[int], bass_note: Optional[int],
                             velocity: int = 100):
        """
        Send both chord and bass note together

        Args:
            chord_notes: List of chord MIDI notes
            bass_note: Bass MIDI note (or None)
            velocity: Note velocity for both chord and bass
        """
        self.send_chord(chord_notes, velocity)

        if bass_note is not None:
            self.send_bass(bass_note, velocity)

    def stop_all(self):
        """Stop all active notes on all channels"""
        self.stop_chord()
        self.stop_bass()
        self.stop_all_performance_notes()

    def enable_chord_output(self, enabled: bool = True):
        """Enable/disable chord channel output"""
        self.chord_enabled = enabled
        if not enabled:
            self.stop_chord()

    def enable_bass_output(self, enabled: bool = True):
        """Enable/disable bass channel output"""
        self.bass_enabled = enabled
        if not enabled:
            self.stop_bass()

    def enable_performance_output(self, enabled: bool = True):
        """Enable/disable performance channel output"""
        self.performance_enabled = enabled
        if not enabled:
            self.stop_all_performance_notes()

    def get_active_notes_count(self) -> dict:
        """Get count of active notes per channel"""
        return {
            'chord': len(self.active_chord_notes),
            'bass': 1 if self.active_bass_note else 0,
            'performance': len(self.active_performance_notes),
            'total': len(self.active_chord_notes) + (1 if self.active_bass_note else 0) + len(self.active_performance_notes)
        }

    def send_song_position(self, position: int):
        """
        Send Song Position Pointer for DAW sync
        Compatible with Renoise integration
        """
        self.midi_processor.send_song_position(position)

    def panic(self):
        """Emergency: stop all notes on all channels immediately"""
        self.stop_all()

        # Send All Notes Off on all 3 channels
        for ch in [self.chord_channel, self.bass_channel, self.performance_channel]:
            self.midi_processor.all_notes_off(ch)


if __name__ == '__main__':
    # Test MIDI router
    print("Orchid-Pi MIDI Router Test\n" + "=" * 50)

    # Create MIDI processor and router
    processor = MIDIProcessor()
    router = MIDIRouter(processor)

    print("\nAvailable MIDI Output Ports:")
    for i, port in enumerate(processor.get_available_output_ports()):
        print(f"  {i}: {port}")

    # Try to open first available output or create virtual
    if processor.get_available_output_ports():
        processor.open_output_port(0)
    else:
        print("\nNo hardware MIDI ports found. Creating virtual port...")
        processor.create_virtual_output("Orchid-Pi Test Out")

    print(f"\nOutput port: {processor.output_port}")
    print(f"Chord channel: {router.chord_channel}")
    print(f"Bass channel: {router.bass_channel}")
    print(f"Performance channel: {router.performance_channel}")

    # Test sending chord
    print("\n1. Sending Cmaj7 chord...")
    cmaj7 = [60, 64, 67, 71]  # C, E, G, B
    router.send_chord(cmaj7, velocity=100)
    print(f"   Active notes: {router.get_active_notes_count()}")
    time.sleep(1)

    # Test bass
    print("\n2. Adding bass note (C2)...")
    router.send_bass(36, velocity=90)
    print(f"   Active notes: {router.get_active_notes_count()}")
    time.sleep(1)

    # Stop chord
    print("\n3. Stopping chord...")
    router.stop_chord()
    print(f"   Active notes: {router.get_active_notes_count()}")
    time.sleep(0.5)

    # Stop bass
    print("\n4. Stopping bass...")
    router.stop_bass()
    print(f"   Active notes: {router.get_active_notes_count()}")
    time.sleep(0.5)

    # Test chord + bass together
    print("\n5. Sending chord + bass together (Fmaj7)...")
    fmaj7 = [65, 69, 72, 76]  # F, A, C, E
    router.send_chord_with_bass(fmaj7, 41, velocity=100)  # F1 bass
    print(f"   Active notes: {router.get_active_notes_count()}")
    time.sleep(1)

    # Panic test
    print("\n6. PANIC - stop all notes...")
    router.panic()
    print(f"   Active notes: {router.get_active_notes_count()}")

    print("\nTest complete!")
    processor.close()
