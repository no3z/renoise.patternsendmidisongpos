"""
Main GUI Window for Orchid-Pi (Redesigned)
Full-screen Kivy interface optimized for chord progressions
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.core.window import Window

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import (ChordEngine, CHORD_FORMULAS, get_all_genres,
                  get_progressions_for_genre, ProgressionPlayer)
from midi import MIDIProcessor, MIDIRouter
from performance import StrumMode, ArpeggiatorMode, SlopMode, PatternMode, HarpMode


class ChordButton(Button):
    """Large, visual button for a chord"""
    def __init__(self, chord_name="", chord_notes=None, **kwargs):
        super().__init__(**kwargs)
        self.chord_name = chord_name
        self.chord_notes = chord_notes or []
        self.text = chord_name
        self.font_size = '28sp'
        self.bold = True
        self.size_hint_y = None
        self.height = 120
        self.background_color = (0.2, 0.4, 0.7, 1)

    def set_active(self, active):
        """Highlight when active"""
        if active:
            self.background_color = (0.3, 0.7, 0.3, 1)
        else:
            self.background_color = (0.2, 0.4, 0.7, 1)


class ProgressionView(BoxLayout):
    """Displays current progression with clickable chord buttons"""

    def __init__(self, on_chord_clicked=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.on_chord_clicked = on_chord_clicked

        # Title
        self.title_label = Label(
            text='Select a Progression',
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.title_label)

        # Scroll view for chords
        scroll = ScrollView(size_hint=(1, 1))
        self.chord_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chord_grid.bind(minimum_height=self.chord_grid.setter('height'))
        scroll.add_widget(self.chord_grid)
        self.add_widget(scroll)

        self.chord_buttons = []
        self.current_chord_index = -1

    def load_progression(self, progression_name, chords):
        """Load progression into view"""
        # Clear existing
        self.chord_grid.clear_widgets()
        self.chord_buttons = []

        # Update title
        self.title_label.text = progression_name

        # Create chord buttons
        for i, (notes, name) in enumerate(chords):
            btn = ChordButton(chord_name=name, chord_notes=notes)
            btn.bind(on_press=lambda x, idx=i: self._chord_clicked(idx))
            self.chord_grid.add_widget(btn)
            self.chord_buttons.append(btn)

    def _chord_clicked(self, index):
        """Handle chord button click"""
        for i, btn in enumerate(self.chord_buttons):
            btn.set_active(i == index)

        self.current_chord_index = index

        if self.on_chord_clicked:
            self.on_chord_clicked(index)

    def highlight_chord(self, index):
        """Highlight chord at index"""
        for i, btn in enumerate(self.chord_buttons):
            btn.set_active(i == index)
        self.current_chord_index = index


class OrchidPiApp(App):
    """Main Orchid-Pi Application - Redesigned"""

    def build(self):
        # Set fullscreen
        Window.fullscreen = 'auto'
        self.title = 'Orchid-Pi - Chord Progression Player'

        # Initialize MIDI
        self.midi_processor = MIDIProcessor()
        self.midi_router = MIDIRouter(self.midi_processor)

        # Initialize chord engine
        self.chord_engine = ChordEngine(default_chord_type='maj7')

        # Initialize progression player
        self.progression_player = ProgressionPlayer(key_root=60, scale='major')

        # Initialize performance modes
        self.modes = {
            'direct': None,
            'strum': StrumMode(self.midi_router),
            'arp': ArpeggiatorMode(self.midi_router),
            'slop': SlopMode(self.midi_router),
            'pattern': PatternMode(self.midi_router),
            'harp': HarpMode(self.midi_router)
        }
        self.current_mode = 'direct'

        # Setup MIDI
        self._setup_midi()

        # Build UI
        root = BoxLayout(orientation='horizontal', padding=5, spacing=5)

        # LEFT PANEL - Progression view (70%)
        left_panel = BoxLayout(orientation='vertical', size_hint_x=0.7, spacing=10)

        # Key selector
        key_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        key_box.add_widget(Label(text='Key:', size_hint_x=0.2))
        
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.note_spinner = Spinner(text='C', values=notes, size_hint_x=0.3)
        self.note_spinner.bind(text=lambda s, t: self.on_key_changed())
        key_box.add_widget(self.note_spinner)

        self.octave_spinner = Spinner(text='4', values=[str(i) for i in range(9)], size_hint_x=0.2)
        self.octave_spinner.bind(text=lambda s, t: self.on_key_changed())
        key_box.add_widget(self.octave_spinner)

        self.scale_spinner = Spinner(text='major', values=['major', 'minor'], size_hint_x=0.3)
        self.scale_spinner.bind(text=lambda s, t: self.on_key_changed())
        key_box.add_widget(self.scale_spinner)
        
        left_panel.add_widget(key_box)

        # Progression selector
        prog_box = BoxLayout(orientation='vertical', size_hint_y=None, height=130, spacing=10)
        
        genre_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        genre_box.add_widget(Label(text='Genre:', size_hint_x=0.3))
        
        genres = get_all_genres()
        self.genre_spinner = Spinner(text=genres[0] if genres else 'pop', values=genres, size_hint_x=0.7)
        self.genre_spinner.bind(text=self._on_genre_changed)
        genre_box.add_widget(self.genre_spinner)
        prog_box.add_widget(genre_box)
        
        prog_select_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        prog_select_box.add_widget(Label(text='Progression:', size_hint_x=0.3))
        
        self.progression_spinner = Spinner(text='Select...', values=[], size_hint_x=0.7)
        self.progression_spinner.bind(text=self._on_progression_changed)
        prog_select_box.add_widget(self.progression_spinner)
        prog_box.add_widget(prog_select_box)
        
        left_panel.add_widget(prog_box)

        # Current chord display
        self.current_chord_label = Label(
            text='---',
            font_size='60sp',
            bold=True,
            size_hint_y=None,
            height=100,
            color=(0.3, 1.0, 0.3, 1)
        )
        left_panel.add_widget(self.current_chord_label)

        # Progression view
        self.progression_view = ProgressionView(on_chord_clicked=self.on_chord_clicked)
        left_panel.add_widget(self.progression_view)

        # Navigation buttons
        nav_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=10)
        btn_prev = Button(text='◀ PREV', font_size='24sp', bold=True)
        btn_prev.bind(on_press=lambda x: self.prev_chord())
        btn_next = Button(text='NEXT ▶', font_size='24sp', bold=True)
        btn_next.bind(on_press=lambda x: self.next_chord())
        nav_box.add_widget(btn_prev)
        nav_box.add_widget(btn_next)
        left_panel.add_widget(nav_box)

        root.add_widget(left_panel)

        # RIGHT PANEL
        right_panel = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=10)

        # Performance mode selector
        perf_box = BoxLayout(orientation='vertical', size_hint_y=None, height=250, spacing=5)
        perf_box.add_widget(Label(text='Performance Mode', size_hint_y=0.2, bold=True))

        modes = ['Direct', 'Strum', 'Arp', 'Slop', 'Pattern', 'Harp']
        self.mode_buttons = {}

        for mode in modes:
            btn = ToggleButton(text=mode, group='perf_mode', size_hint_y=None, height=30)
            btn.bind(on_press=lambda x, m=mode.lower(): self.on_mode_changed(m))
            perf_box.add_widget(btn)
            self.mode_buttons[mode.lower()] = btn

        self.mode_buttons['direct'].state = 'down'
        right_panel.add_widget(perf_box)

        # Bass toggle
        bass_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        bass_box.add_widget(Label(text='Bass:', size_hint_x=0.4))
        self.bass_toggle = ToggleButton(text='ON', state='down', size_hint_x=0.6)
        self.bass_toggle.bind(on_press=self.toggle_bass)
        bass_box.add_widget(self.bass_toggle)
        right_panel.add_widget(bass_box)

        # Status
        self.status_label = Label(text='Ready', size_hint_y=None, height=100, font_size='14sp')
        right_panel.add_widget(self.status_label)

        root.add_widget(right_panel)

        # Load default progression
        Clock.schedule_once(lambda dt: self._load_default(), 0.5)

        return root

    def _setup_midi(self):
        """Setup MIDI I/O"""
        outputs = self.midi_processor.get_available_output_ports()
        if outputs:
            self.midi_processor.open_output_port(0)
            self.status_label.text = f'MIDI Out: {self.midi_processor.output_port}'
        else:
            self.midi_processor.create_virtual_output("Orchid-Pi Out")
            self.status_label.text = 'MIDI Out: Virtual'

    def _load_default(self):
        """Load default progression"""
        self._on_genre_changed(self.genre_spinner, self.genre_spinner.text)
        
    def _on_genre_changed(self, spinner, genre):
        """Handle genre change"""
        progs = get_progressions_for_genre(genre)
        prog_names = [progs[key]['name'] for key in progs.keys()]
        self.progression_spinner.values = prog_names
        if prog_names:
            self.progression_spinner.text = prog_names[0]

    def _on_progression_changed(self, spinner, prog_name):
        """Handle progression change"""
        if prog_name == 'Select...':
            return
            
        genre = self.genre_spinner.text
        progs = get_progressions_for_genre(genre)
        
        prog_key = None
        for key, data in progs.items():
            if data['name'] == prog_name:
                prog_key = key
                break

        if prog_key:
            self.progression_player.load_progression(genre, prog_key)
            chords = self.progression_player.get_full_progression_chords()
            self.progression_view.load_progression(prog_name, chords)
            self.progression_player.reset()
            self.play_current_chord()

    def on_chord_clicked(self, index):
        """Handle chord click"""
        self.progression_player.current_chord_index = index
        self.play_current_chord()

    def play_current_chord(self):
        """Play current chord"""
        chord_data = self.progression_player.get_current_chord()
        if not chord_data:
            return

        chord_notes, chord_name = chord_data
        self.current_chord_label.text = chord_name
        self.progression_view.highlight_chord(self.progression_player.current_chord_index)

        bass_enabled = self.bass_toggle.state == 'down'
        bass_note = self.chord_engine.theory.get_bass_note(chord_notes) if bass_enabled else None

        if self.current_mode == 'direct':
            self.midi_router.send_chord_with_bass(chord_notes, bass_note, velocity=100)
        else:
            mode = self.modes[self.current_mode]
            if mode:
                mode.enable()
                mode.process(chord_notes, velocity=100)
                if bass_note:
                    self.midi_router.send_bass(bass_note, velocity=100)

    def next_chord(self):
        """Next chord"""
        self.progression_player.next_chord()
        self.play_current_chord()

    def prev_chord(self):
        """Previous chord"""
        self.progression_player.previous_chord()
        self.play_current_chord()

    def on_key_changed(self):
        """Handle key change"""
        note = self.note_spinner.text
        octave = int(self.octave_spinner.text)
        scale = self.scale_spinner.text
        
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        midi_note = (octave + 1) * 12 + notes.index(note)
        
        self.progression_player.set_key(midi_note, scale)
        chords = self.progression_player.get_full_progression_chords()
        prog_name = self.progression_player.current_progression_name

        if chords:
            self.progression_view.load_progression(prog_name, chords)
            self.play_current_chord()

    def on_mode_changed(self, mode):
        """Handle mode change"""
        if self.current_mode != 'direct' and self.current_mode in self.modes:
            old_mode = self.modes[self.current_mode]
            if old_mode:
                old_mode.disable()
        self.current_mode = mode

    def toggle_bass(self, instance):
        """Toggle bass"""
        instance.text = 'ON' if instance.state == 'down' else 'OFF'

    def on_stop(self):
        """Cleanup"""
        for mode in self.modes.values():
            if mode:
                mode.disable()
        self.midi_router.stop_all()
        self.midi_processor.close()


if __name__ == '__main__':
    OrchidPiApp().run()
