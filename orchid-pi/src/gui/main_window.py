"""
Main GUI Window for Orchid-Pi
Kivy-based touchscreen interface
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window

import sys
import os
# Add parent directories to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import ChordEngine, CHORD_FORMULAS
from midi import MIDIProcessor, MIDIRouter
from performance import StrumMode, ArpeggiatorMode, SlopMode, PatternMode, HarpMode


class ChordDisplay(BoxLayout):
    """Widget to display current chord info"""

    chord_name = StringProperty("---")
    voicing_info = StringProperty("Root Position")
    root_note = StringProperty("---")
    bass_note = StringProperty("---")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = 0.15
        self.padding = 10

        # Chord name label (large)
        self.chord_label = Label(
            text=self.chord_name,
            font_size='40sp',
            bold=True,
            size_hint_y=0.6
        )
        self.add_widget(self.chord_label)

        # Info grid
        info_grid = GridLayout(cols=3, size_hint_y=0.4)
        info_grid.add_widget(Label(text='Voicing:', size_hint_x=0.3))
        self.voicing_label = Label(text=self.voicing_info)
        info_grid.add_widget(self.voicing_label)
        info_grid.add_widget(Label(text='', size_hint_x=0.3))

        self.add_widget(info_grid)

    def update_display(self, chord_info):
        """Update display with chord info dict"""
        self.chord_name = chord_info.get('chord_name', '---')
        self.chord_label.text = self.chord_name

        # Voicing info
        inv = chord_info.get('inversion', 0)
        inv_names = ['Root', '1st Inv', '2nd Inv', '3rd Inv']
        self.voicing_info = inv_names[min(inv, 3)]
        self.voicing_label.text = self.voicing_info


class VirtualKeyboard(GridLayout):
    """12-key virtual keyboard"""

    def __init__(self, on_note_pressed=None, **kwargs):
        super().__init__(**kwargs)
        self.cols = 12
        self.size_hint_y = 0.2
        self.spacing = 2
        self.padding = 10

        self.on_note_pressed = on_note_pressed
        self.base_octave = 4

        # Note names for 12 keys
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        # Create buttons
        self.key_buttons = []
        for i, note_name in enumerate(self.note_names):
            btn = Button(
                text=note_name,
                font_size='20sp',
                bold=True
            )

            # Color white/black keys differently
            is_black_key = '#' in note_name
            if is_black_key:
                btn.background_color = (0.2, 0.2, 0.2, 1)
            else:
                btn.background_color = (0.9, 0.9, 0.9, 1)

            btn.bind(on_press=lambda x, idx=i: self._key_pressed(idx))
            self.add_widget(btn)
            self.key_buttons.append(btn)

    def _key_pressed(self, note_index):
        """Handle key press"""
        midi_note = (self.base_octave + 1) * 12 + note_index

        if self.on_note_pressed:
            self.on_note_pressed(midi_note, 100)

    def set_octave(self, octave):
        """Set base octave (0-8)"""
        self.base_octave = max(0, min(8, octave))


class PerformanceModeSelector(GridLayout):
    """Selector for performance modes"""

    def __init__(self, on_mode_changed=None, **kwargs):
        super().__init__(**kwargs)
        self.cols = 5
        self.size_hint_y = 0.1
        self.spacing = 5
        self.padding = 10

        self.on_mode_changed = on_mode_changed
        self.current_mode = 'direct'

        # Mode buttons
        self.mode_buttons = {}
        modes = ['Direct', 'Strum', 'Arp', 'Slop', 'Pattern', 'Harp']

        for mode in modes:
            btn = ToggleButton(
                text=mode,
                group='performance_mode',
                state='normal',
                font_size='16sp'
            )
            btn.bind(on_press=lambda x, m=mode.lower(): self._mode_selected(m))
            self.add_widget(btn)
            self.mode_buttons[mode.lower()] = btn

        # Set Direct as default
        self.mode_buttons['direct'].state = 'down'

    def _mode_selected(self, mode):
        """Handle mode selection"""
        self.current_mode = mode
        if self.on_mode_changed:
            self.on_mode_changed(mode)


class ControlPanel(BoxLayout):
    """Control panel with various settings"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.15
        self.spacing = 10
        self.padding = 10

        # Octave control
        octave_box = BoxLayout(orientation='vertical')
        octave_box.add_widget(Label(text='Octave', size_hint_y=0.3))
        self.octave_label = Label(text='4', size_hint_y=0.4, font_size='24sp')
        octave_box.add_widget(self.octave_label)

        octave_btns = BoxLayout(size_hint_y=0.3)
        btn_down = Button(text='▼')
        btn_up = Button(text='▲')
        btn_down.bind(on_press=lambda x: self.change_octave(-1))
        btn_up.bind(on_press=lambda x: self.change_octave(1))
        octave_btns.add_widget(btn_down)
        octave_btns.add_widget(btn_up)
        octave_box.add_widget(octave_btns)

        self.add_widget(octave_box)

        # Chord type selector
        chord_box = BoxLayout(orientation='vertical')
        chord_box.add_widget(Label(text='Chord Type', size_hint_y=0.3))
        self.chord_type_label = Label(text='maj7', size_hint_y=0.4, font_size='20sp')
        chord_box.add_widget(self.chord_type_label)

        chord_btns = BoxLayout(size_hint_y=0.3)
        btn_prev = Button(text='◀')
        btn_next = Button(text='▶')
        btn_prev.bind(on_press=lambda x: self.change_chord_type(-1))
        btn_next.bind(on_press=lambda x: self.change_chord_type(1))
        chord_btns.add_widget(btn_prev)
        chord_btns.add_widget(btn_next)
        chord_box.add_widget(chord_btns)

        self.add_widget(chord_box)

        # Bass toggle
        bass_box = BoxLayout(orientation='vertical')
        bass_box.add_widget(Label(text='Bass', size_hint_y=0.5))
        self.bass_toggle = ToggleButton(text='ON', state='down', size_hint_y=0.5)
        self.bass_toggle.bind(on_press=self.toggle_bass)
        bass_box.add_widget(self.bass_toggle)
        self.add_widget(bass_box)

        # Settings
        self.octave = 4
        self.chord_types = sorted(CHORD_FORMULAS.keys())
        self.chord_type_index = self.chord_types.index('maj7')
        self.bass_enabled = True

    def change_octave(self, delta):
        """Change octave up/down"""
        self.octave = max(0, min(8, self.octave + delta))
        self.octave_label.text = str(self.octave)

    def change_chord_type(self, delta):
        """Change chord type"""
        self.chord_type_index = (self.chord_type_index + delta) % len(self.chord_types)
        self.chord_type_label.text = self.chord_types[self.chord_type_index]

    def toggle_bass(self, instance):
        """Toggle bass on/off"""
        self.bass_enabled = instance.state == 'down'
        instance.text = 'ON' if self.bass_enabled else 'OFF'


class OrchidPiApp(App):
    """Main Orchid-Pi application"""

    def build(self):
        # Set window title
        self.title = 'Orchid-Pi MIDI Brain'

        # Initialize MIDI
        self.midi_processor = MIDIProcessor()
        self.midi_router = MIDIRouter(self.midi_processor)

        # Initialize chord engine
        self.chord_engine = ChordEngine(default_chord_type='maj7')

        # Initialize performance modes
        self.modes = {
            'direct': None,  # Direct mode = no performance processing
            'strum': StrumMode(self.midi_router),
            'arp': ArpeggiatorMode(self.midi_router),
            'slop': SlopMode(self.midi_router),
            'pattern': PatternMode(self.midi_router),
            'harp': HarpMode(self.midi_router)
        }

        self.current_mode = 'direct'

        # Setup MIDI I/O
        self._setup_midi()

        # Build UI
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title bar
        title = Label(
            text='ORCHID-PI MIDI BRAIN',
            size_hint_y=0.08,
            font_size='28sp',
            bold=True
        )
        root.add_widget(title)

        # Chord display
        self.chord_display = ChordDisplay()
        root.add_widget(self.chord_display)

        # Virtual keyboard
        self.keyboard = VirtualKeyboard(on_note_pressed=self.on_note_pressed)
        root.add_widget(self.keyboard)

        # Control panel
        self.control_panel = ControlPanel()
        root.add_widget(self.control_panel)

        # Performance mode selector
        self.mode_selector = PerformanceModeSelector(on_mode_changed=self.on_mode_changed)
        root.add_widget(self.mode_selector)

        # Status bar
        self.status_label = Label(
            text='Ready | MIDI: Not connected',
            size_hint_y=0.05,
            font_size='14sp'
        )
        root.add_widget(self.status_label)

        # Update display periodically
        Clock.schedule_interval(self.update_display, 0.1)

        return root

    def _setup_midi(self):
        """Setup MIDI I/O"""
        # Try to open MIDI output
        outputs = self.midi_processor.get_available_output_ports()
        if outputs:
            self.midi_processor.open_output_port(0)
            self.status_label.text = f'MIDI Out: {self.midi_processor.output_port}'
        else:
            self.midi_processor.create_virtual_output("Orchid-Pi Out")
            self.status_label.text = 'MIDI Out: Orchid-Pi Out (Virtual)'

        # Try to open MIDI input
        inputs = self.midi_processor.get_available_input_ports()
        if inputs:
            self.midi_processor.open_input_port(0)
            self.midi_processor.set_note_on_callback(self.on_midi_note)
            self.status_label.text += f' | MIDI In: {self.midi_processor.input_port}'

    def on_note_pressed(self, midi_note, velocity):
        """Handle note press (from virtual keyboard or MIDI input)"""
        # Update chord engine settings
        self.chord_engine.set_octave(self.control_panel.octave)
        self.chord_engine.set_chord_type(self.control_panel.chord_types[self.control_panel.chord_type_index])
        self.chord_engine.enable_bass(self.control_panel.bass_enabled)

        # Process note through chord engine
        chord_notes, bass_note = self.chord_engine.process_note(midi_note, velocity)

        # Apply performance mode or send direct
        if self.current_mode == 'direct':
            # Send directly via router
            self.midi_router.send_chord_with_bass(chord_notes, bass_note, velocity)
        else:
            # Process through performance mode
            mode = self.modes[self.current_mode]
            if mode:
                mode.enable()
                mode.process(chord_notes, velocity)
                # Send bass separately
                if bass_note:
                    self.midi_router.send_bass(bass_note, velocity)

    def on_midi_note(self, note, velocity, channel):
        """Handle MIDI input note"""
        self.on_note_pressed(note, velocity)

    def on_mode_changed(self, mode):
        """Handle performance mode change"""
        # Disable previous mode
        if self.current_mode != 'direct' and self.current_mode in self.modes:
            old_mode = self.modes[self.current_mode]
            if old_mode:
                old_mode.disable()

        # Set new mode
        self.current_mode = mode

    def update_display(self, dt):
        """Update chord display"""
        info = self.chord_engine.get_current_voicing_info()
        self.chord_display.update_display(info)

    def on_stop(self):
        """Cleanup on app close"""
        # Stop all modes
        for mode in self.modes.values():
            if mode:
                mode.disable()

        # Close MIDI
        self.midi_router.stop_all()
        self.midi_processor.close()


if __name__ == '__main__':
    OrchidPiApp().run()
