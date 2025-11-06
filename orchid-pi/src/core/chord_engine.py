"""
Chord Engine for Orchid-Pi
Main engine for chord generation, voice-leading, and processing
"""

from typing import List, Optional, Tuple
from .music_theory import MusicTheory, CHORD_FORMULAS
from .voice_leading import VoiceLeading


class ChordEngine:
    """
    Main chord processing engine
    Combines music theory, voice-leading, and intelligent chord generation
    """

    def __init__(self, default_chord_type='maj7', octave=4):
        self.theory = MusicTheory()
        self.voice_leading = VoiceLeading()

        # Engine state
        self.current_chord_type = default_chord_type
        self.current_root = None
        self.current_chord_notes = []
        self.octave = octave
        self.transpose_semitones = 0

        # Voice-leading settings
        self.use_voice_leading = True
        self.current_inversion = 0
        self.voicing_rotation = 0

        # Bass settings
        self.bass_enabled = True
        self.bass_octaves_down = 1

    def set_chord_type(self, chord_type: str):
        """Set the current chord type"""
        if chord_type in CHORD_FORMULAS:
            self.current_chord_type = chord_type
        else:
            print(f"Warning: Unknown chord type '{chord_type}', using 'maj7'")
            self.current_chord_type = 'maj7'

    def set_octave(self, octave: int):
        """Set the base octave (0-8)"""
        self.octave = max(0, min(8, octave))

    def set_transpose(self, semitones: int):
        """Set global transpose in semitones"""
        self.transpose_semitones = semitones

    def set_inversion(self, inversion: int):
        """Set specific inversion (0=root, 1=1st inv, etc.)"""
        self.current_inversion = max(0, inversion)

    def rotate_voicing(self, steps: int = 1):
        """
        Rotate voicing dial (like Orchid's physical dial)
        Positive steps = rotate up, negative = rotate down
        """
        self.voicing_rotation += steps

        if self.current_chord_notes:
            self.current_chord_notes = self.voice_leading.rotate_voicing(
                self.current_chord_notes, steps
            )

        return self.current_chord_notes

    def process_note(self, midi_note: int, velocity: int = 100,
                     use_voice_leading: Optional[bool] = None) -> Tuple[List[int], int]:
        """
        Main processing function: convert input note to full chord

        Args:
            midi_note: Input MIDI note (0-127)
            velocity: Note velocity (0-127)
            use_voice_leading: Override default voice-leading setting

        Returns:
            Tuple of (chord_notes, bass_note)
        """
        # Apply transpose
        root = midi_note + self.transpose_semitones
        root = max(0, min(127, root))  # Clamp to valid MIDI range

        self.current_root = root

        # Generate raw chord from theory
        raw_chord = self.theory.generate_chord(
            root,
            self.current_chord_type,
            octave_range=1
        )

        # Apply voice-leading or forced inversion
        vl = use_voice_leading if use_voice_leading is not None else self.use_voice_leading

        if self.current_inversion > 0:
            # Force specific inversion
            voiced_chord = self.voice_leading.voice_chord(
                raw_chord,
                use_voice_leading=False,
                force_inversion=self.current_inversion
            )
        else:
            # Use intelligent voice-leading
            voiced_chord = self.voice_leading.voice_chord(
                raw_chord,
                use_voice_leading=vl
            )

        # Apply any voicing rotation
        if self.voicing_rotation != 0:
            voiced_chord = self.voice_leading.rotate_voicing(
                voiced_chord,
                steps=0  # Already applied
            )

        self.current_chord_notes = voiced_chord

        # Generate bass note
        bass_note = None
        if self.bass_enabled:
            bass_note = self.theory.get_bass_note(
                voiced_chord,
                octaves_down=self.bass_octaves_down
            )

        return (voiced_chord, bass_note)

    def get_current_chord_name(self) -> str:
        """Get human-readable name of current chord"""
        if self.current_root is None:
            return "---"

        return self.theory.get_chord_name(self.current_root, self.current_chord_type)

    def get_current_voicing_info(self) -> dict:
        """Get detailed info about current voicing"""
        return {
            'chord_name': self.get_current_chord_name(),
            'root_note': self.theory.midi_to_note_name(self.current_root) if self.current_root else None,
            'chord_type': self.current_chord_type,
            'inversion': self.current_inversion,
            'voicing_rotation': self.voicing_rotation,
            'notes': [self.theory.midi_to_note_name(n) for n in self.current_chord_notes],
            'midi_notes': self.current_chord_notes,
            'bass_enabled': self.bass_enabled,
            'octave': self.octave,
            'transpose': self.transpose_semitones
        }

    def enable_bass(self, enabled: bool = True):
        """Enable/disable bass note generation"""
        self.bass_enabled = enabled

    def set_bass_octaves(self, octaves: int):
        """Set how many octaves down the bass note should be"""
        self.bass_octaves_down = max(1, min(3, octaves))

    def enable_voice_leading(self, enabled: bool = True):
        """Enable/disable intelligent voice-leading"""
        self.use_voice_leading = enabled

    def reset_voice_leading(self):
        """Reset voice-leading memory"""
        self.voice_leading.reset()

    def get_available_chord_types(self) -> List[str]:
        """Get list of all available chord types"""
        return sorted(CHORD_FORMULAS.keys())


if __name__ == '__main__':
    # Test the chord engine
    engine = ChordEngine(default_chord_type='maj7')

    print("Orchid-Pi Chord Engine Test\n" + "=" * 50)

    # Process C note
    print("\n1. Process C4 (MIDI 60) as maj7:")
    chord, bass = engine.process_note(60, velocity=100)
    print(f"   Chord: {chord}")
    print(f"   Bass: {bass}")
    print(f"   Info: {engine.get_current_chord_name()}")

    # Change to minor chord
    print("\n2. Change to minor chord:")
    engine.set_chord_type('min7')
    chord, bass = engine.process_note(60)
    print(f"   Chord: {chord}")
    print(f"   {engine.get_current_chord_name()}")

    # Test voice-leading
    print("\n3. Voice-leading test (C → F):")
    engine.set_chord_type('maj7')
    c_chord, _ = engine.process_note(60)
    print(f"   C: {c_chord}")

    f_chord, _ = engine.process_note(65)  # F
    print(f"   F: {f_chord}")
    print(f"   (Voice-leading minimized movement)")

    # Test inversion
    print("\n4. Test 1st inversion:")
    engine.set_inversion(1)
    inv_chord, _ = engine.process_note(60)
    print(f"   Cmaj7 (1st inv): {inv_chord}")

    # Test voicing rotation
    print("\n5. Test voicing rotation:")
    engine.set_inversion(0)
    engine.reset_voice_leading()
    orig, _ = engine.process_note(60)
    print(f"   Original: {orig}")

    rotated = engine.rotate_voicing(steps=2)
    print(f"   Rotated +2: {rotated}")

    # Full info
    print("\n6. Full voicing info:")
    info = engine.get_current_voicing_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
