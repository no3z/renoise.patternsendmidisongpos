"""
Progression Player for Orchid-Pi
Converts chord progressions from Roman numeral notation to actual MIDI notes
"""

from typing import List, Tuple, Optional
from .music_theory import MusicTheory
from .chord_progressions import PROGRESSIONS


class ProgressionPlayer:
    """
    Handles conversion of Roman numeral progressions to actual chords
    """

    # Roman numeral to scale degree mapping
    ROMAN_TO_DEGREE = {
        'I': 0, 'i': 0,
        'bII': 1, 'II': 2, 'ii': 2, '#II': 3,
        'bIII': 3, 'III': 4, 'iii': 4, '#III': 5,
        'IV': 5, 'iv': 5, '#IV': 6,
        'bV': 6, 'V': 7, 'v': 7, '#V': 8,
        'bVI': 8, 'VI': 9, 'vi': 9, '#VI': 10,
        'bVII': 10, 'VII': 11, 'vii': 11,
    }

    def __init__(self, key_root=60, scale='major'):
        """
        Initialize progression player

        Args:
            key_root: MIDI note number for tonic (default 60 = C4)
            scale: Scale type (default 'major')
        """
        self.theory = MusicTheory()
        self.key_root = key_root
        self.scale = scale
        self.current_progression = None
        self.current_progression_name = ""
        self.current_chord_index = 0

    def set_key(self, root_midi: int, scale: str = 'major'):
        """Set the key for the progression"""
        self.key_root = root_midi
        self.scale = scale

    def roman_numeral_to_chord(self, numeral: str, quality: str) -> Tuple[int, str]:
        """
        Convert Roman numeral to root note and chord type

        Args:
            numeral: Roman numeral (I, IV, V, ii, etc.)
            quality: Chord quality (major, min7, dom7, etc.)

        Returns:
            Tuple of (root_midi_note, chord_quality)
        """
        # Get scale degree offset
        degree_offset = self.ROMAN_TO_DEGREE.get(numeral, 0)

        # Calculate root note
        root_note = self.key_root + degree_offset

        return (root_note, quality)

    def load_progression(self, genre: str, progression_key: str) -> bool:
        """
        Load a progression from the library

        Args:
            genre: Genre category (e.g., 'jazz', 'pop')
            progression_key: Progression identifier (e.g., 'ii-V-I')

        Returns:
            True if loaded successfully
        """
        if genre not in PROGRESSIONS:
            return False

        genre_progs = PROGRESSIONS[genre]

        if progression_key not in genre_progs:
            return False

        prog_data = genre_progs[progression_key]
        self.current_progression = prog_data['progression']
        self.current_progression_name = prog_data['name']
        self.current_chord_index = 0

        return True

    def get_chord_at_index(self, index: int) -> Optional[Tuple[List[int], str]]:
        """
        Get chord notes at specific index in progression

        Args:
            index: Chord index in progression

        Returns:
            Tuple of (chord_notes_list, chord_name) or None
        """
        if not self.current_progression:
            return None

        if index < 0 or index >= len(self.current_progression):
            return None

        numeral, quality = self.current_progression[index]

        # Convert to actual chord
        root_note, chord_quality = self.roman_numeral_to_chord(numeral, quality)

        # Generate chord notes
        chord_notes = self.theory.generate_chord(root_note, chord_quality)

        # Generate chord name
        chord_name = self.theory.get_chord_name(root_note, chord_quality)

        return (chord_notes, chord_name)

    def get_current_chord(self) -> Optional[Tuple[List[int], str]]:
        """Get chord at current index"""
        return self.get_chord_at_index(self.current_chord_index)

    def next_chord(self) -> Optional[Tuple[List[int], str]]:
        """Advance to next chord in progression"""
        if not self.current_progression:
            return None

        self.current_chord_index = (self.current_chord_index + 1) % len(self.current_progression)
        return self.get_current_chord()

    def previous_chord(self) -> Optional[Tuple[List[int], str]]:
        """Go to previous chord in progression"""
        if not self.current_progression:
            return None

        self.current_chord_index = (self.current_chord_index - 1) % len(self.current_progression)
        return self.get_current_chord()

    def get_full_progression_chords(self) -> List[Tuple[List[int], str]]:
        """
        Get all chords in current progression

        Returns:
            List of (chord_notes, chord_name) tuples
        """
        if not self.current_progression:
            return []

        chords = []
        for i in range(len(self.current_progression)):
            chord_data = self.get_chord_at_index(i)
            if chord_data:
                chords.append(chord_data)

        return chords

    def get_progression_length(self) -> int:
        """Get number of chords in current progression"""
        return len(self.current_progression) if self.current_progression else 0

    def reset(self):
        """Reset to first chord in progression"""
        self.current_chord_index = 0

    def get_progression_info(self) -> dict:
        """Get information about current progression"""
        return {
            'name': self.current_progression_name,
            'length': self.get_progression_length(),
            'current_index': self.current_chord_index,
            'key': self.theory.midi_to_note_name(self.key_root),
            'scale': self.scale
        }


if __name__ == '__main__':
    # Test progression player
    print("Progression Player Test\n" + "=" * 60)

    player = ProgressionPlayer(key_root=60, scale='major')  # C major

    # Load ii-V-I progression
    print("\n1. Loading ii-V-I (Jazz Turnaround) in C major")
    success = player.load_progression('jazz', 'ii-V-I')
    print(f"   Loaded: {success}")

    if success:
        print(f"   Progression: {player.current_progression_name}")
        print(f"   Length: {player.get_progression_length()} chords")

        print("\n2. Getting all chords:")
        chords = player.get_full_progression_chords()
        for i, (notes, name) in enumerate(chords):
            print(f"   {i+1}. {name}: {notes}")

        print("\n3. Stepping through progression:")
        player.reset()
        for i in range(player.get_progression_length()):
            notes, name = player.get_current_chord()
            print(f"   Step {i+1}: {name} - {notes}")
            player.next_chord()

    # Test in different key
    print("\n4. Same progression in F major")
    player.set_key(65, 'major')  # F major
    chords = player.get_full_progression_chords()
    for i, (notes, name) in enumerate(chords):
        print(f"   {i+1}. {name}")

    # Test pop progression
    print("\n5. Loading I-V-vi-IV (Pop Hits) in G major")
    player.set_key(67, 'major')  # G major
    player.load_progression('pop', 'I-V-vi-IV')
    chords = player.get_full_progression_chords()
    for i, (notes, name) in enumerate(chords):
        print(f"   {i+1}. {name}")

    # Info
    print("\n6. Progression info:")
    info = player.get_progression_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
