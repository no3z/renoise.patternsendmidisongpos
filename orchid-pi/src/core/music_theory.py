"""
Music Theory Module for Orchid-Pi
Provides chord generation, scales, and music theory utilities
"""

# MIDI note constants
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_TO_MIDI = {note: idx for idx, note in enumerate(NOTES)}

# Interval definitions (in semitones)
INTERVALS = {
    'unison': 0,
    'minor_2nd': 1,
    'major_2nd': 2,
    'minor_3rd': 3,
    'major_3rd': 4,
    'perfect_4th': 5,
    'tritone': 6,
    'perfect_5th': 7,
    'minor_6th': 8,
    'major_6th': 9,
    'minor_7th': 10,
    'major_7th': 11,
    'octave': 12
}

# Chord formulas (intervals from root)
CHORD_FORMULAS = {
    # Triads
    'major': [0, 4, 7],
    'minor': [0, 3, 7],
    'diminished': [0, 3, 6],
    'augmented': [0, 4, 8],
    'sus2': [0, 2, 7],
    'sus4': [0, 5, 7],

    # Seventh chords
    'maj7': [0, 4, 7, 11],
    'min7': [0, 3, 7, 10],
    'dom7': [0, 4, 7, 10],
    'dim7': [0, 3, 6, 9],
    'min7b5': [0, 3, 6, 10],  # Half-diminished
    'aug7': [0, 4, 8, 10],
    'maj7#5': [0, 4, 8, 11],

    # Extended chords
    'maj9': [0, 4, 7, 11, 14],
    'min9': [0, 3, 7, 10, 14],
    'dom9': [0, 4, 7, 10, 14],
    '7#9': [0, 4, 7, 10, 15],
    '7b9': [0, 4, 7, 10, 13],
    'dom7b9': [0, 4, 7, 10, 13],  # Alias for 7b9
    'dom7#9': [0, 4, 7, 10, 15],  # Alias for 7#9

    'maj11': [0, 4, 7, 11, 14, 17],
    'min11': [0, 3, 7, 10, 14, 17],
    'dom11': [0, 4, 7, 10, 14, 17],

    'maj13': [0, 4, 7, 11, 14, 17, 21],
    'min13': [0, 3, 7, 10, 14, 17, 21],
    'dom13': [0, 4, 7, 10, 14, 17, 21],

    # Altered dominants
    'dom7#5': [0, 4, 8, 10],  # Augmented 7th
    'dom7#11': [0, 4, 7, 10, 18],  # Lydian dominant

    # Extended with alterations
    'maj7#11': [0, 4, 7, 11, 18],  # Lydian major 7
    'maj9#11': [0, 4, 7, 11, 14, 18],  # Lydian major 9
    'maj13#11': [0, 4, 7, 11, 14, 18, 21],  # Lydian major 13

    # Add chords
    'add9': [0, 4, 7, 14],
    'madd9': [0, 3, 7, 14],
    '6': [0, 4, 7, 9],
    'min6': [0, 3, 7, 9],
    '6/9': [0, 4, 7, 9, 14],
}

# Scale formulas
SCALE_FORMULAS = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
    'pentatonic_major': [0, 2, 4, 7, 9],
    'pentatonic_minor': [0, 3, 5, 7, 10],
    'blues': [0, 3, 5, 6, 7, 10],
}


class MusicTheory:
    """Music theory utilities for chord and scale generation"""

    @staticmethod
    def midi_to_note_name(midi_note):
        """Convert MIDI note number to note name with octave"""
        octave = (midi_note // 12) - 1
        note = NOTES[midi_note % 12]
        return f"{note}{octave}"

    @staticmethod
    def note_name_to_midi(note_name):
        """Convert note name (e.g., 'C4') to MIDI note number"""
        note = note_name[:-1]
        octave = int(note_name[-1])
        return (octave + 1) * 12 + NOTE_TO_MIDI[note]

    @staticmethod
    def generate_chord(root_midi, chord_type='major', octave_range=1):
        """
        Generate chord notes from root MIDI note

        Args:
            root_midi: Root note as MIDI number (0-127)
            chord_type: Type of chord (see CHORD_FORMULAS)
            octave_range: How many octaves to span (1-3)

        Returns:
            List of MIDI note numbers
        """
        if chord_type not in CHORD_FORMULAS:
            chord_type = 'major'

        formula = CHORD_FORMULAS[chord_type]
        notes = [root_midi + interval for interval in formula]

        # Extend to multiple octaves if requested
        if octave_range > 1:
            extended_notes = []
            for octave in range(octave_range):
                extended_notes.extend([n + (12 * octave) for n in notes])
            notes = extended_notes

        # Filter notes within MIDI range
        notes = [n for n in notes if 0 <= n <= 127]

        return notes

    @staticmethod
    def generate_scale(root_midi, scale_type='major', octaves=1):
        """Generate scale notes from root MIDI note"""
        if scale_type not in SCALE_FORMULAS:
            scale_type = 'major'

        formula = SCALE_FORMULAS[scale_type]
        notes = []

        for octave in range(octaves):
            octave_notes = [root_midi + interval + (12 * octave) for interval in formula]
            notes.extend(octave_notes)

        # Add final root note
        notes.append(root_midi + (12 * octaves))

        # Filter notes within MIDI range
        notes = [n for n in notes if 0 <= n <= 127]

        return notes

    @staticmethod
    def get_chord_name(root_midi, chord_type):
        """Get human-readable chord name"""
        root_name = MusicTheory.midi_to_note_name(root_midi)
        # Remove octave number for chord display
        root_note = root_name[:-1]
        return f"{root_note}{chord_type}"

    @staticmethod
    def transpose(midi_note, semitones):
        """Transpose a MIDI note by semitones"""
        transposed = midi_note + semitones
        return max(0, min(127, transposed))  # Clamp to valid MIDI range

    @staticmethod
    def interval_between(note1, note2):
        """Calculate interval in semitones between two notes"""
        return abs(note2 - note1)

    @staticmethod
    def get_bass_note(chord_notes, octaves_down=1):
        """Get bass note from chord (root note transposed down)"""
        root = min(chord_notes)
        bass = root - (12 * octaves_down)
        return max(0, bass)  # Don't go below MIDI 0


if __name__ == '__main__':
    # Test the module
    theory = MusicTheory()

    # Generate C major chord
    c_major = theory.generate_chord(60, 'major')  # C4
    print(f"C major: {c_major}")
    print(f"Notes: {[theory.midi_to_note_name(n) for n in c_major]}")

    # Generate Cmaj7 chord
    cmaj7 = theory.generate_chord(60, 'maj7')
    print(f"\nCmaj7: {cmaj7}")
    print(f"Notes: {[theory.midi_to_note_name(n) for n in cmaj7]}")

    # Generate C major scale
    c_scale = theory.generate_scale(60, 'major', octaves=2)
    print(f"\nC major scale (2 octaves): {c_scale}")

    # Get bass note
    bass = theory.get_bass_note(cmaj7)
    print(f"\nBass note: {bass} ({theory.midi_to_note_name(bass)})")
