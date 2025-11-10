"""
Chord Visualization Widgets for Orchid-Pi
Provides visual representations of chords on fretboard and piano
"""

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp


class FretboardWidget(RelativeLayout):
    """
    Guitar fretboard visualization showing chord fingerings
    """

    # Standard guitar tuning (MIDI notes for open strings)
    TUNING = [64, 59, 55, 50, 45, 40]  # E4, B3, G3, D3, A2, E2
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_notes = []
        self.chord_name = ""
        self.bind(size=self._draw_fretboard, pos=self._draw_fretboard)

    def _draw_fretboard(self, *args):
        """Draw the fretboard with strings and frets"""
        self.canvas.clear()
        self.clear_widgets()

        if self.width == 0 or self.height == 0:
            return

        with self.canvas:
            # Background
            Color(0.15, 0.1, 0.05, 1)  # Dark wood color
            Rectangle(pos=self.pos, size=self.size)

            # Calculate dimensions
            num_strings = 6
            num_frets = 5
            margin_left = dp(60)
            margin_right = dp(20)
            margin_top = dp(50)
            margin_bottom = dp(40)

            fretboard_width = self.width - margin_left - margin_right
            fretboard_height = self.height - margin_top - margin_bottom

            if fretboard_width <= 0 or fretboard_height <= 0:
                return

            string_spacing = fretboard_height / (num_strings - 1)
            fret_spacing = fretboard_width / num_frets

            # Draw strings (horizontal lines)
            Color(0.7, 0.7, 0.7, 1)
            for i in range(num_strings):
                y = self.y + margin_bottom + i * string_spacing
                x1 = self.x + margin_left
                x2 = self.x + self.width - margin_right
                Line(points=[x1, y, x2, y], width=1.5)

            # Draw frets (vertical lines)
            Color(0.6, 0.6, 0.6, 1)
            for i in range(num_frets + 1):
                x = self.x + margin_left + i * fret_spacing
                y1 = self.y + margin_bottom
                y2 = self.y + self.height - margin_top
                Line(points=[x, y1, x, y2], width=2)

            # Draw nut (thicker line at fret 0)
            Color(0.9, 0.9, 0.9, 1)
            x = self.x + margin_left
            y1 = self.y + margin_bottom
            y2 = self.y + self.height - margin_top
            Line(points=[x, y1, x, y2], width=4)

        # Add string labels (absolute positioning)
        string_names = ['E', 'B', 'G', 'D', 'A', 'E']
        for i, name in enumerate(string_names):
            y = self.y + margin_bottom + i * string_spacing - dp(10)
            label = Label(
                text=name,
                pos=(self.x + dp(10), y),
                size=(dp(40), dp(20)),
                size_hint=(None, None),
                font_size='14sp',
                color=(1, 1, 1, 1)
            )
            self.add_widget(label)

        # Add fret numbers (absolute positioning)
        for i in range(1, num_frets + 1):
            x = self.x + margin_left + (i - 0.5) * fret_spacing - dp(10)
            y = self.y + self.height - margin_top + dp(10)
            label = Label(
                text=str(i),
                pos=(x, y),
                size=(dp(20), dp(20)),
                size_hint=(None, None),
                font_size='14sp',
                color=(1, 1, 1, 1)
            )
            self.add_widget(label)

        # Draw chord name at top
        if self.chord_name:
            label = Label(
                text=self.chord_name,
                pos=(self.x + self.width // 2 - dp(75), self.y + self.height - dp(35)),
                size=(dp(150), dp(30)),
                size_hint=(None, None),
                font_size='24sp',
                bold=True,
                color=(0.3, 1.0, 0.3, 1)
            )
            self.add_widget(label)

        # Redraw current chord if any
        if self.current_notes:
            self._draw_chord_positions(
                self.current_notes, margin_left, margin_bottom, string_spacing, fret_spacing, num_frets
            )

    def _draw_chord_positions(self, notes, margin_left, margin_bottom, string_spacing, fret_spacing, num_frets):
        """Draw finger positions for the current chord"""
        # Find optimal fingering positions for the given notes
        positions = self._find_chord_positions(notes, num_frets)

        with self.canvas:
            # Draw finger positions
            Color(0.3, 1.0, 0.3, 1)  # Green for active notes
            for string_idx, fret in positions:
                if fret >= 0:  # Valid position
                    x = self.x + margin_left + (fret + 0.5) * fret_spacing
                    y = self.y + margin_bottom + string_idx * string_spacing
                    Ellipse(pos=(x - dp(12), y - dp(12)), size=(dp(24), dp(24)))

    def _find_chord_positions(self, notes, num_frets):
        """Find finger positions on fretboard for given MIDI notes"""
        positions = []

        # Convert notes to pitch classes (0-11)
        note_pitch_classes = set(note % 12 for note in notes)

        # For each string, find the closest matching note
        for string_idx, open_note in enumerate(self.TUNING):
            best_fret = -1
            best_distance = 999

            for fret in range(num_frets + 1):
                fret_note = (open_note + fret) % 12
                if fret_note in note_pitch_classes:
                    # Check if this note is in the actual chord (not just pitch class)
                    actual_midi = open_note + fret
                    if any(abs(actual_midi - note) <= 12 for note in notes):
                        if abs(fret - 3) < best_distance:  # Prefer middle frets
                            best_fret = fret
                            best_distance = abs(fret - 3)

            if best_fret >= 0:
                positions.append((string_idx, best_fret))

        return positions

    def update_chord(self, notes, chord_name=""):
        """Update the displayed chord"""
        self.current_notes = notes
        self.chord_name = chord_name
        self._draw_fretboard()


class PianoWidget(RelativeLayout):
    """
    Piano keyboard visualization showing chord notes
    """

    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    BLACK_KEYS = [1, 3, 6, 8, 10]  # C#, D#, F#, G#, A#

    def __init__(self, start_note=48, num_octaves=2, **kwargs):
        """
        Initialize piano widget

        Args:
            start_note: MIDI note for leftmost key (default 48 = C3)
            num_octaves: Number of octaves to display (default 2)
        """
        super().__init__(**kwargs)
        self.start_note = start_note
        self.num_octaves = num_octaves
        self.num_keys = num_octaves * 12
        self.current_notes = []
        self.chord_name = ""
        self.bind(size=self._draw_piano, pos=self._draw_piano)

    def _draw_piano(self, *args):
        """Draw the piano keyboard"""
        self.canvas.clear()
        self.clear_widgets()

        with self.canvas:
            # Background
            Color(0.15, 0.15, 0.15, 1)
            Rectangle(pos=self.pos, size=self.size)

        # Calculate dimensions
        margin = dp(20)
        piano_width = self.width - 2 * margin
        piano_height = self.height - 2 * margin

        white_keys_per_octave = 7
        num_white_keys = self.num_octaves * white_keys_per_octave
        white_key_width = piano_width / num_white_keys
        white_key_height = piano_height

        black_key_width = white_key_width * 0.6
        black_key_height = white_key_height * 0.6

        # Draw white keys first
        white_key_index = 0
        for i in range(self.num_keys):
            note = (self.start_note + i) % 12
            midi_note = self.start_note + i

            if note not in self.BLACK_KEYS:
                x = self.x + margin + white_key_index * white_key_width
                y = self.y + margin

                # Check if this key should be highlighted
                is_active = midi_note in self.current_notes

                with self.canvas:
                    if is_active:
                        Color(0.2, 0.8, 0.3, 1)  # Green for active
                    else:
                        Color(0.95, 0.95, 0.95, 1)  # White
                    Rectangle(pos=(x, y), size=(white_key_width - 1, white_key_height))
                    Color(0, 0, 0, 1)
                    Line(rectangle=(x, y, white_key_width - 1, white_key_height), width=1)

                # Add note label at bottom of white keys
                note_name = self.NOTE_NAMES[note]
                octave = (self.start_note + i) // 12 - 1
                if note == 0:  # Only show octave on C notes
                    label_text = f"{note_name}{octave}"
                else:
                    label_text = note_name

                label = Label(
                    text=label_text,
                    pos=(x, y + dp(5)),
                    size=(white_key_width, dp(20)),
                    font_size='10sp',
                    color=(0.3, 0.3, 0.3, 1) if not is_active else (1, 1, 1, 1)
                )
                self.add_widget(label)

                white_key_index += 1

        # Draw black keys on top
        white_key_index = 0
        for i in range(self.num_keys):
            note = (self.start_note + i) % 12
            midi_note = self.start_note + i

            if note not in self.BLACK_KEYS:
                white_key_index += 1
            else:
                # Position black key between white keys
                x = self.x + margin + white_key_index * white_key_width - black_key_width / 2
                y = self.y + margin + white_key_height - black_key_height

                # Check if this key should be highlighted
                is_active = midi_note in self.current_notes

                with self.canvas:
                    if is_active:
                        Color(0.1, 0.6, 0.2, 1)  # Dark green for active
                    else:
                        Color(0.1, 0.1, 0.1, 1)  # Black
                    Rectangle(pos=(x, y), size=(black_key_width, black_key_height))
                    Color(0.3, 0.3, 0.3, 1)
                    Line(rectangle=(x, y, black_key_width, black_key_height), width=1)

        # Add chord name label
        if self.chord_name:
            label = Label(
                text=self.chord_name,
                pos=(self.x + self.width // 2 - dp(75), self.y + self.height - dp(40)),
                size=(dp(150), dp(30)),
                font_size='24sp',
                bold=True,
                color=(0.2, 0.8, 0.3, 1)
            )
            self.add_widget(label)

    def update_chord(self, notes, chord_name=""):
        """Update the displayed chord"""
        self.current_notes = notes
        self.chord_name = chord_name
        self._draw_piano()


if __name__ == '__main__':
    """Test the visualizers"""
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout

    class TestApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical')

            # Test fretboard
            fretboard = FretboardWidget(size_hint=(1, 0.5))
            fretboard.update_chord([60, 64, 67], "C Major")  # C major chord
            layout.add_widget(fretboard)

            # Test piano
            piano = PianoWidget(size_hint=(1, 0.5))
            piano.update_chord([60, 64, 67], "C Major")  # C major chord
            layout.add_widget(piano)

            return layout

    TestApp().run()
