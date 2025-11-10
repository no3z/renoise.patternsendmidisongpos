"""
Orchid-Pi - SIMPLIFIED Main Window
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.core.window import Window

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import (ChordEngine, get_all_genres, get_progressions_for_genre, ProgressionPlayer)
from midi import MIDIProcessor, MIDIRouter
from performance import StrumMode, ArpeggiatorMode, SlopMode, PatternMode, HarpMode
from gui.chord_visualizers import FretboardWidget, PianoWidget


class OrchidPiApp(App):

    def build(self):
        Window.fullscreen = 'auto'
        self.title = 'Orchid-Pi'

        # Init MIDI
        self.midi_processor = MIDIProcessor()
        self.midi_router = MIDIRouter(self.midi_processor)
        self.chord_engine = ChordEngine(default_chord_type='maj7')
        self.progression_player = ProgressionPlayer(key_root=60, scale='major')

        # Init modes
        self.modes = {
            'direct': None,
            'strum': StrumMode(self.midi_router),
            'arp': ArpeggiatorMode(self.midi_router),
            'slop': SlopMode(self.midi_router),
            'pattern': PatternMode(self.midi_router),
            'harp': HarpMode(self.midi_router)
        }
        self.current_mode = 'direct'

        # === ROOT ===
        root = BoxLayout(orientation='vertical', spacing=5, padding=5)

        # === TOP CONTROLS (Fixed height) ===
        top = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=5)

        top.add_widget(Label(text='KEY:', size_hint_x=0.1, color=(1,1,1,1)))

        self.note_spinner = Spinner(text='C', values=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'], size_hint_x=0.1)
        self.note_spinner.bind(text=self.on_key_changed)
        top.add_widget(self.note_spinner)

        self.octave_spinner = Spinner(text='4', values=[str(i) for i in range(9)], size_hint_x=0.08)
        self.octave_spinner.bind(text=self.on_key_changed)
        top.add_widget(self.octave_spinner)

        self.scale_spinner = Spinner(text='major', values=['major','minor'], size_hint_x=0.12)
        self.scale_spinner.bind(text=self.on_key_changed)
        top.add_widget(self.scale_spinner)

        genres = get_all_genres()
        self.genre_spinner = Spinner(text=genres[0] if genres else 'pop', values=genres, size_hint_x=0.25)
        self.genre_spinner.bind(text=self.on_genre_changed)
        top.add_widget(self.genre_spinner)

        self.prog_spinner = Spinner(text='Select...', values=[], size_hint_x=0.35)
        self.prog_spinner.bind(text=self.on_prog_changed)
        top.add_widget(self.prog_spinner)

        root.add_widget(top)

        # === CURRENT CHORD (Fixed height) ===
        self.chord_label = Label(
            text='- SELECT PROGRESSION -',
            size_hint_y=None,
            height=50,
            font_size='28sp',
            bold=True,
            color=(0.4, 1, 0.4, 1)
        )
        root.add_widget(self.chord_label)

        # === MAIN AREA ===
        main = BoxLayout(orientation='horizontal', spacing=5)

        # LEFT: Tabs (70%)
        tabs = TabbedPanel(do_default_tab=False, size_hint_x=0.7)

        # Tab 1: Chords
        tab_chords = TabbedPanelItem(text='CHORDS')
        chords_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.prog_title = Label(text='', size_hint_y=None, height=30, color=(1,1,1,1))
        chords_layout.add_widget(self.prog_title)

        scroll = ScrollView()
        self.chord_grid = GridLayout(cols=3, spacing=10, size_hint_y=None)
        self.chord_grid.bind(minimum_height=self.chord_grid.setter('height'))
        scroll.add_widget(self.chord_grid)
        chords_layout.add_widget(scroll)

        tab_chords.add_widget(chords_layout)
        tabs.add_widget(tab_chords)

        # Tab 2: Fretboard
        tab_fret = TabbedPanelItem(text='FRETBOARD')
        self.fretboard = FretboardWidget()
        tab_fret.add_widget(self.fretboard)
        tabs.add_widget(tab_fret)

        # Tab 3: Piano
        tab_piano = TabbedPanelItem(text='PIANO')
        self.piano = PianoWidget(start_note=48, num_octaves=3)
        tab_piano.add_widget(self.piano)
        tabs.add_widget(tab_piano)

        main.add_widget(tabs)

        # RIGHT: Controls (30%)
        right = BoxLayout(orientation='vertical', size_hint_x=0.3, spacing=5, padding=5)

        right.add_widget(Label(text='Performance', size_hint_y=None, height=25, color=(1,1,1,1), bold=True))

        self.mode_btns = {}
        for m in ['Direct', 'Strum', 'Arp', 'Slop', 'Pattern', 'Harp']:
            btn = ToggleButton(text=m, group='mode', size_hint_y=None, height=30)
            btn.bind(on_press=lambda x, mode=m.lower(): self.on_mode_changed(mode))
            right.add_widget(btn)
            self.mode_btns[m.lower()] = btn
        self.mode_btns['direct'].state = 'down'

        bass_box = BoxLayout(size_hint_y=None, height=35)
        bass_box.add_widget(Label(text='Bass:', color=(1,1,1,1)))
        self.bass_toggle = ToggleButton(text='ON', state='down')
        self.bass_toggle.bind(on_press=self.toggle_bass)
        bass_box.add_widget(self.bass_toggle)
        right.add_widget(bass_box)

        right.add_widget(Label(text='MIDI Out', size_hint_y=None, height=25, color=(1,1,1,1), bold=True))

        midi_box = BoxLayout(size_hint_y=None, height=35)
        self.midi_spinner = Spinner(text='Loading...', values=[])
        self.midi_spinner.bind(text=self.on_midi_changed)
        midi_box.add_widget(self.midi_spinner)
        refresh = Button(text='↻', size_hint_x=0.25)
        refresh.bind(on_press=self.refresh_midi)
        midi_box.add_widget(refresh)
        right.add_widget(midi_box)

        self.status = Label(text='Ready', size_hint_y=None, height=40, font_size='10sp', color=(0.7,0.7,0.7,1))
        right.add_widget(self.status)

        right.add_widget(Label())  # Spacer

        main.add_widget(right)
        root.add_widget(main)

        # Setup
        self.chord_buttons = []
        self.setup_midi()
        Clock.schedule_once(lambda dt: self.load_default(), 0.5)

        return root

    def setup_midi(self):
        outputs = self.midi_processor.get_available_output_ports()
        if outputs:
            self.midi_spinner.values = outputs + ["Virtual"]
            self.midi_spinner.text = outputs[0]
            self.midi_processor.open_output_port(0)
            self.status.text = f'Connected: {outputs[0]}'
        else:
            self.midi_processor.create_virtual_output("Orchid-Pi")
            self.midi_spinner.values = ["Virtual"]
            self.midi_spinner.text = "Virtual"
            self.status.text = 'Virtual port'

    def refresh_midi(self, *args):
        outputs = self.midi_processor.get_available_output_ports()
        self.midi_spinner.values = outputs + ["Virtual"] if outputs else ["Virtual"]
        self.status.text = f'{len(outputs)} port(s)'

    def on_midi_changed(self, spinner, text):
        if not text or text == 'Loading...':
            return
        if self.midi_processor.midi_out:
            try:
                self.midi_router.stop_all()
                self.midi_processor.midi_out.close_port()
            except:
                pass

        if text == "Virtual":
            self.midi_processor.create_virtual_output("Orchid-Pi")
            self.status.text = 'Virtual'
        else:
            outputs = self.midi_processor.get_available_output_ports()
            for i, port in enumerate(outputs):
                if port == text:
                    self.midi_processor.open_output_port(i)
                    self.status.text = f'OK: {text[:20]}'
                    break

    def load_default(self):
        self.on_genre_changed(None, self.genre_spinner.text)

    def on_genre_changed(self, spinner, genre):
        progs = get_progressions_for_genre(genre)
        names = [progs[k]['name'] for k in progs.keys()]
        self.prog_spinner.values = names
        if names:
            self.prog_spinner.text = names[0]

    def on_prog_changed(self, spinner, name):
        if name == 'Select...':
            return

        genre = self.genre_spinner.text
        progs = get_progressions_for_genre(genre)

        key = None
        for k, v in progs.items():
            if v['name'] == name:
                key = k
                break

        if key:
            self.progression_player.load_progression(genre, key)
            chords = self.progression_player.get_full_progression_chords()
            self.load_chords(name, chords)
            self.progression_player.reset()
            self.play_chord()

    def load_chords(self, name, chords):
        self.chord_grid.clear_widgets()
        self.chord_buttons = []
        self.prog_title.text = name

        for i, (notes, chord_name) in enumerate(chords):
            btn = Button(
                text=chord_name,
                size_hint=(None, None),
                size=(180, 80),
                font_size='20sp',
                bold=True,
                color=(1, 1, 1, 1),
                background_color=(0.2, 0.4, 0.7, 1)
            )
            btn.bind(on_press=lambda x, idx=i: self.chord_clicked(idx))
            self.chord_grid.add_widget(btn)
            self.chord_buttons.append(btn)

    def chord_clicked(self, index):
        self.progression_player.current_chord_index = index

        # Highlight
        for i, btn in enumerate(self.chord_buttons):
            if i == index:
                btn.background_color = (0.3, 0.7, 0.3, 1)
            else:
                btn.background_color = (0.2, 0.4, 0.7, 1)

        self.play_chord()

    def play_chord(self):
        data = self.progression_player.get_current_chord()
        if not data:
            return

        notes, name = data
        self.chord_label.text = name

        # Update visualizers
        self.fretboard.update_chord(notes, name)
        self.piano.update_chord(notes, name)

        # Play MIDI
        bass = self.chord_engine.theory.get_bass_note(notes) if self.bass_toggle.state == 'down' else None

        if self.current_mode == 'direct':
            self.midi_router.send_chord_with_bass(notes, bass, velocity=100)
        else:
            mode = self.modes[self.current_mode]
            if mode:
                mode.enable()
                mode.process(notes, velocity=100)
                if bass:
                    self.midi_router.send_bass(bass, velocity=100)

    def on_key_changed(self, *args):
        note = self.note_spinner.text
        octave = int(self.octave_spinner.text)
        scale = self.scale_spinner.text

        notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        midi = (octave + 1) * 12 + notes.index(note)

        self.progression_player.set_key(midi, scale)
        chords = self.progression_player.get_full_progression_chords()
        name = self.progression_player.current_progression_name

        if chords:
            self.load_chords(name, chords)
            self.play_chord()

    def on_mode_changed(self, mode):
        if self.current_mode != 'direct' and self.current_mode in self.modes:
            old = self.modes[self.current_mode]
            if old:
                old.disable()
        self.current_mode = mode

    def toggle_bass(self, instance):
        instance.text = 'ON' if instance.state == 'down' else 'OFF'

    def on_stop(self):
        for mode in self.modes.values():
            if mode:
                mode.disable()
        self.midi_router.stop_all()
        self.midi_processor.close()


if __name__ == '__main__':
    OrchidPiApp().run()
