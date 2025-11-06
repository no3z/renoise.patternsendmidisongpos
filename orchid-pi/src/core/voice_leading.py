"""
Voice Leading Module for Orchid-Pi
Implements intelligent voice-leading algorithms and chord inversions
"""

from typing import List, Optional


class VoiceLeading:
    """
    Handles voice-leading, inversions, and smooth chord progressions
    Inspired by Orchid's patent-pending voicing system
    """

    def __init__(self):
        self.previous_chord = None
        self.current_inversion = 0

    def apply_inversion(self, chord_notes: List[int], inversion: int) -> List[int]:
        """
        Apply inversion to chord notes

        Args:
            chord_notes: List of MIDI note numbers
            inversion: Inversion number (0=root, 1=1st inv, 2=2nd inv, etc.)

        Returns:
            Inverted chord notes
        """
        if not chord_notes or inversion == 0:
            return sorted(chord_notes)

        notes = sorted(chord_notes)
        num_notes = len(notes)

        # Apply inversion by moving lower notes up an octave
        inversion = inversion % num_notes  # Wrap around

        for _ in range(inversion):
            # Move lowest note up an octave
            notes[0] += 12
            notes = sorted(notes)

        return notes

    def get_all_inversions(self, chord_notes: List[int]) -> List[List[int]]:
        """
        Get all possible inversions of a chord

        Returns:
            List of inverted chord variations
        """
        inversions = []
        num_notes = len(chord_notes)

        for inv in range(num_notes):
            inversions.append(self.apply_inversion(chord_notes, inv))

        return inversions

    def calculate_voice_motion(self, chord1: List[int], chord2: List[int]) -> int:
        """
        Calculate total voice motion between two chords
        Lower values = smoother voice-leading

        Returns:
            Total semitone movement across all voices
        """
        if not chord1 or not chord2:
            return float('inf')

        # Pad shorter chord with None
        max_len = max(len(chord1), len(chord2))
        c1 = list(chord1) + [None] * (max_len - len(chord1))
        c2 = list(chord2) + [None] * (max_len - len(chord2))

        total_motion = 0

        for n1, n2 in zip(sorted(c1), sorted(c2)):
            if n1 is None or n2 is None:
                total_motion += 12  # Penalty for voice appearing/disappearing
            else:
                total_motion += abs(n2 - n1)

        return total_motion

    def find_smoothest_voicing(self, current_chord: List[int],
                                previous_chord: Optional[List[int]] = None) -> List[int]:
        """
        Find the smoothest voicing for current chord based on previous chord
        Uses voice-leading algorithm to minimize voice motion

        Args:
            current_chord: New chord to voice
            previous_chord: Previous chord (if any)

        Returns:
            Best-voiced chord notes
        """
        if previous_chord is None:
            # No previous chord, return root position
            return sorted(current_chord)

        # Get all inversions of current chord
        inversions = self.get_all_inversions(current_chord)

        # Find inversion with minimum voice motion
        best_voicing = current_chord
        min_motion = float('inf')

        for inv in inversions:
            motion = self.calculate_voice_motion(previous_chord, inv)
            if motion < min_motion:
                min_motion = motion
                best_voicing = inv

        return best_voicing

    def voice_chord(self, chord_notes: List[int],
                    use_voice_leading: bool = True,
                    force_inversion: Optional[int] = None) -> List[int]:
        """
        Voice a chord with optional intelligent voice-leading

        Args:
            chord_notes: Raw chord notes
            use_voice_leading: Apply smooth voice-leading based on previous chord
            force_inversion: Force specific inversion (overrides voice-leading)

        Returns:
            Voiced chord notes
        """
        if force_inversion is not None:
            # Force specific inversion
            voiced = self.apply_inversion(chord_notes, force_inversion)
            self.current_inversion = force_inversion
        elif use_voice_leading and self.previous_chord is not None:
            # Use intelligent voice-leading
            voiced = self.find_smoothest_voicing(chord_notes, self.previous_chord)
        else:
            # Root position
            voiced = sorted(chord_notes)
            self.current_inversion = 0

        # Store for next voice-leading calculation
        self.previous_chord = voiced

        return voiced

    def rotate_voicing(self, chord_notes: List[int], steps: int = 1) -> List[int]:
        """
        Rotate voicing by moving notes between octaves
        Simulates Orchid's voicing dial rotation

        Args:
            chord_notes: Current chord
            steps: Number of rotation steps (positive = up, negative = down)

        Returns:
            Rotated chord
        """
        if not chord_notes:
            return chord_notes

        notes = sorted(chord_notes)

        if steps > 0:
            # Rotate up: move lowest note up an octave
            for _ in range(steps):
                notes[0] += 12
                notes = sorted(notes)
        else:
            # Rotate down: move highest note down an octave
            for _ in range(abs(steps)):
                notes[-1] -= 12
                notes = sorted(notes)

        # Filter valid MIDI range
        notes = [n for n in notes if 0 <= n <= 127]

        self.previous_chord = notes
        return notes

    def expand_voicing_range(self, chord_notes: List[int],
                             target_range_semitones: int = 24) -> List[int]:
        """
        Expand chord voicing across a wider range
        Simulates Orchid's expansion from 12 keys to full piano range

        Args:
            chord_notes: Compact chord
            target_range_semitones: Desired range (default 24 = 2 octaves)

        Returns:
            Expanded chord
        """
        if not chord_notes:
            return chord_notes

        notes = sorted(chord_notes)
        current_range = notes[-1] - notes[0]

        if current_range >= target_range_semitones:
            return notes

        # Expand by spreading notes across octaves
        expanded = []
        num_notes = len(notes)
        octave_increment = target_range_semitones // (num_notes - 1) if num_notes > 1 else 0

        for i, note in enumerate(notes):
            expanded_note = notes[0] + (i * octave_increment)
            # Keep same pitch class
            while (expanded_note % 12) != (note % 12):
                expanded_note += 1
            expanded.append(expanded_note)

        # Filter valid MIDI range
        expanded = [n for n in expanded if 0 <= n <= 127]

        return expanded

    def compress_voicing_range(self, chord_notes: List[int],
                                max_range_semitones: int = 12) -> List[int]:
        """
        Compress chord into tighter voicing

        Args:
            chord_notes: Wide chord
            max_range_semitones: Maximum range (default 12 = 1 octave)

        Returns:
            Compressed chord
        """
        if not chord_notes:
            return chord_notes

        notes = sorted(chord_notes)
        root = notes[0]

        compressed = []
        for note in notes:
            # Bring all notes within range of root
            while note - root > max_range_semitones:
                note -= 12
            if note >= root and note not in compressed:
                compressed.append(note)

        return sorted(compressed)

    def reset(self):
        """Reset voice-leading memory"""
        self.previous_chord = None
        self.current_inversion = 0


if __name__ == '__main__':
    # Test voice leading
    vl = VoiceLeading()

    # Test inversions
    c_major = [60, 64, 67]  # C, E, G
    print("C major inversions:")
    for i, inv in enumerate(vl.get_all_inversions(c_major)):
        print(f"  Inversion {i}: {inv}")

    # Test voice-leading between chords
    print("\nVoice-leading test:")
    cmaj = [60, 64, 67]
    fmaj = [65, 69, 72]

    voiced_c = vl.voice_chord(cmaj)
    print(f"C major: {voiced_c}")

    voiced_f = vl.voice_chord(fmaj, use_voice_leading=True)
    print(f"F major (smooth): {voiced_f}")

    motion = vl.calculate_voice_motion(voiced_c, voiced_f)
    print(f"Voice motion: {motion} semitones")

    # Test rotation
    print("\nVoicing rotation:")
    rotated = vl.rotate_voicing(c_major, steps=2)
    print(f"Rotated +2: {rotated}")
