"""
MIDI Processor for Orchid-Pi
Handles MIDI input/output and message processing
"""

import time
from typing import Callable, Optional, List
try:
    import rtmidi
    RTMIDI_AVAILABLE = True
except ImportError:
    RTMIDI_AVAILABLE = False
    print("Warning: rtmidi not available. MIDI functionality will be limited.")


class MIDIProcessor:
    """
    Processes MIDI input and manages MIDI I/O
    """

    def __init__(self):
        self.midi_in = None
        self.midi_out = None
        self.input_port = None
        self.output_port = None

        # Callbacks
        self.note_on_callback = None
        self.note_off_callback = None
        self.cc_callback = None

        # State
        self.active_notes = {}  # Track currently held notes

        if RTMIDI_AVAILABLE:
            self._init_midi()

    def _init_midi(self):
        """Initialize MIDI I/O"""
        try:
            self.midi_in = rtmidi.MidiIn()
            self.midi_out = rtmidi.MidiOut()
        except Exception as e:
            print(f"Error initializing MIDI: {e}")
            self.midi_in = None
            self.midi_out = None

    def get_available_input_ports(self) -> List[str]:
        """Get list of available MIDI input ports"""
        if not self.midi_in:
            return []
        return self.midi_in.get_ports()

    def get_available_output_ports(self) -> List[str]:
        """Get list of available MIDI output ports"""
        if not self.midi_out:
            return []
        return self.midi_out.get_ports()

    def open_input_port(self, port_number: int = 0, port_name: Optional[str] = None):
        """
        Open MIDI input port

        Args:
            port_number: Port index (default 0 = first available)
            port_name: Optional specific port name to open
        """
        if not self.midi_in:
            print("MIDI In not available")
            return False

        try:
            ports = self.get_available_input_ports()

            if port_name:
                # Find port by name
                for i, name in enumerate(ports):
                    if port_name in name:
                        port_number = i
                        break

            if port_number < len(ports):
                self.midi_in.open_port(port_number)
                self.midi_in.set_callback(self._midi_callback)
                self.input_port = ports[port_number]
                print(f"Opened MIDI input: {self.input_port}")
                return True
            else:
                print(f"Invalid port number: {port_number}")
                return False

        except Exception as e:
            print(f"Error opening input port: {e}")
            return False

    def open_output_port(self, port_number: int = 0, port_name: Optional[str] = None):
        """
        Open MIDI output port

        Args:
            port_number: Port index (default 0 = first available)
            port_name: Optional specific port name to open
        """
        if not self.midi_out:
            print("MIDI Out not available")
            return False

        try:
            ports = self.get_available_output_ports()

            if port_name:
                # Find port by name
                for i, name in enumerate(ports):
                    if port_name in name:
                        port_number = i
                        break

            if port_number < len(ports):
                self.midi_out.open_port(port_number)
                self.output_port = ports[port_number]
                print(f"Opened MIDI output: {self.output_port}")
                return True
            else:
                print(f"Invalid port number: {port_number}")
                return False

        except Exception as e:
            print(f"Error opening output port: {e}")
            return False

    def create_virtual_output(self, name: str = "Orchid-Pi Out"):
        """Create a virtual MIDI output port"""
        if not self.midi_out:
            return False

        try:
            self.midi_out.open_virtual_port(name)
            self.output_port = name
            print(f"Created virtual MIDI output: {name}")
            return True
        except Exception as e:
            print(f"Error creating virtual output: {e}")
            return False

    def _midi_callback(self, event, data=None):
        """Internal MIDI input callback"""
        message, deltatime = event

        if not message:
            return

        # Parse MIDI message
        status = message[0]
        channel = (status & 0x0F) + 1
        msg_type = status & 0xF0

        # Note On
        if msg_type == 0x90 and len(message) >= 3:
            note = message[1]
            velocity = message[2]

            if velocity > 0:
                # Actual note on
                self.active_notes[note] = velocity
                if self.note_on_callback:
                    self.note_on_callback(note, velocity, channel)
            else:
                # Note on with velocity 0 = note off
                if note in self.active_notes:
                    del self.active_notes[note]
                if self.note_off_callback:
                    self.note_off_callback(note, channel)

        # Note Off
        elif msg_type == 0x80 and len(message) >= 3:
            note = message[1]
            if note in self.active_notes:
                del self.active_notes[note]
            if self.note_off_callback:
                self.note_off_callback(note, channel)

        # Control Change
        elif msg_type == 0xB0 and len(message) >= 3:
            cc_number = message[1]
            cc_value = message[2]
            if self.cc_callback:
                self.cc_callback(cc_number, cc_value, channel)

    def set_note_on_callback(self, callback: Callable):
        """
        Set callback for Note On messages

        Callback signature: callback(note: int, velocity: int, channel: int)
        """
        self.note_on_callback = callback

    def set_note_off_callback(self, callback: Callable):
        """
        Set callback for Note Off messages

        Callback signature: callback(note: int, channel: int)
        """
        self.note_off_callback = callback

    def set_cc_callback(self, callback: Callable):
        """
        Set callback for Control Change messages

        Callback signature: callback(cc_number: int, value: int, channel: int)
        """
        self.cc_callback = callback

    def send_note_on(self, note: int, velocity: int = 100, channel: int = 1):
        """Send Note On message"""
        if not self.midi_out:
            return

        status = 0x90 | ((channel - 1) & 0x0F)
        message = [status, note & 0x7F, velocity & 0x7F]

        try:
            self.midi_out.send_message(message)
        except Exception as e:
            print(f"Error sending note on: {e}")

    def send_note_off(self, note: int, channel: int = 1):
        """Send Note Off message"""
        if not self.midi_out:
            return

        status = 0x80 | ((channel - 1) & 0x0F)
        message = [status, note & 0x7F, 0]

        try:
            self.midi_out.send_message(message)
        except Exception as e:
            print(f"Error sending note off: {e}")

    def send_cc(self, cc_number: int, value: int, channel: int = 1):
        """Send Control Change message"""
        if not self.midi_out:
            return

        status = 0xB0 | ((channel - 1) & 0x0F)
        message = [status, cc_number & 0x7F, value & 0x7F]

        try:
            self.midi_out.send_message(message)
        except Exception as e:
            print(f"Error sending CC: {e}")

    def send_song_position(self, position: int):
        """
        Send Song Position Pointer (for Renoise sync)
        Compatible with existing com.renoise.no3zchanger.xrnx
        """
        if not self.midi_out:
            return

        # Song Position Pointer: 0xF2 + LSB + MSB
        lsb = position & 0x7F
        msb = (position >> 7) & 0x7F
        message = [0xF2, lsb, msb]

        try:
            self.midi_out.send_message(message)
        except Exception as e:
            print(f"Error sending song position: {e}")

    def all_notes_off(self, channel: int = 1):
        """Send All Notes Off CC message"""
        self.send_cc(123, 0, channel)

    def close(self):
        """Close MIDI ports"""
        if self.midi_in:
            try:
                self.midi_in.close_port()
            except:
                pass

        if self.midi_out:
            try:
                # Send all notes off before closing
                for ch in range(1, 4):
                    self.all_notes_off(ch)
                self.midi_out.close_port()
            except:
                pass

    def __del__(self):
        """Cleanup on destruction"""
        self.close()


if __name__ == '__main__':
    # Test MIDI processor
    print("Orchid-Pi MIDI Processor Test\n" + "=" * 50)

    processor = MIDIProcessor()

    print("\nAvailable MIDI Input Ports:")
    for i, port in enumerate(processor.get_available_input_ports()):
        print(f"  {i}: {port}")

    print("\nAvailable MIDI Output Ports:")
    for i, port in enumerate(processor.get_available_output_ports()):
        print(f"  {i}: {port}")

    # Test callbacks
    def on_note(note, vel, ch):
        print(f"Note On: {note} vel={vel} ch={ch}")

    def on_note_off(note, ch):
        print(f"Note Off: {note} ch={ch}")

    processor.set_note_on_callback(on_note)
    processor.set_note_off_callback(on_note_off)

    print("\nMIDI processor ready. Press Ctrl+C to exit.")

    try:
        # Try to open first available input
        if processor.get_available_input_ports():
            processor.open_input_port(0)
            print("Listening for MIDI input...")

            # Keep alive
            while True:
                time.sleep(0.1)
        else:
            print("No MIDI input ports available")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        processor.close()
