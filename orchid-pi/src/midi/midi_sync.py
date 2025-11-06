"""
MIDI Sync Module for Orchid-Pi
Provides MIDI clock and sync functionality for DAW integration
Compatible with Renoise com.renoise.no3zchanger.xrnx
"""

import time
from typing import Optional
from .midi_processor import MIDIProcessor


class MIDISync:
    """
    MIDI Clock and Song Position synchronization
    Compatible with existing Renoise script
    """

    def __init__(self, midi_processor: Optional[MIDIProcessor] = None):
        self.midi_processor = midi_processor or MIDIProcessor()

        # Sync state
        self.is_playing = False
        self.current_position = 0
        self.bpm = 120.0
        self.pattern_length = 64  # Default pattern length (lines)

        # Clock timing
        self.clock_running = False
        self.last_clock_time = 0
        self.ppqn = 24  # Pulses Per Quarter Note (standard MIDI)

    def set_bpm(self, bpm: float):
        """Set tempo in BPM"""
        self.bpm = max(20.0, min(999.0, bpm))

    def set_pattern_length(self, length: int):
        """Set pattern length in lines (for position calculation)"""
        self.pattern_length = max(1, length)

    def send_song_position(self, position: int):
        """
        Send Song Position Pointer
        Compatible with Renoise script format

        Args:
            position: Song position in measures/beats
        """
        self.current_position = position
        self.midi_processor.send_song_position(position)

    def calculate_position(self, sequence: int, line: int) -> int:
        """
        Calculate song position from Renoise sequence and line
        Matches calculation from com.renoise.no3zchanger.xrnx

        Args:
            sequence: Pattern sequence number (1-based)
            line: Line within pattern (1-based)

        Returns:
            Song position in measures
        """
        # Original formula: (((sequence-1) * 4) + (line/16)) + 1
        measure = (((sequence - 1) * 4) + (line / 16)) + 1
        return int(measure)

    def send_renoise_position(self, sequence: int, line: int):
        """
        Send position in Renoise format
        Compatible with existing script

        Args:
            sequence: Pattern sequence number (1-based)
            line: Line within pattern (1-based)
        """
        position = self.calculate_position(sequence, line)
        self.send_song_position(position)

    def send_start(self):
        """Send MIDI Start message (0xFA)"""
        try:
            self.midi_processor.midi_out.send_message([0xFA])
            self.is_playing = True
        except Exception as e:
            print(f"Error sending MIDI Start: {e}")

    def send_stop(self):
        """Send MIDI Stop message (0xFC)"""
        try:
            self.midi_processor.midi_out.send_message([0xFC])
            self.is_playing = False
            self.clock_running = False
        except Exception as e:
            print(f"Error sending MIDI Stop: {e}")

    def send_continue(self):
        """Send MIDI Continue message (0xFB)"""
        try:
            self.midi_processor.midi_out.send_message([0xFB])
            self.is_playing = True
        except Exception as e:
            print(f"Error sending MIDI Continue: {e}")

    def send_clock_tick(self):
        """Send MIDI Clock message (0xF8)"""
        try:
            self.midi_processor.midi_out.send_message([0xF8])
            self.last_clock_time = time.time()
        except Exception as e:
            print(f"Error sending MIDI Clock: {e}")

    def get_clock_interval(self) -> float:
        """
        Calculate time interval between clock ticks based on BPM

        Returns:
            Interval in seconds
        """
        # MIDI clock: 24 ticks per quarter note
        # BPM = beats (quarter notes) per minute
        # Time per beat = 60 / BPM seconds
        # Time per tick = (60 / BPM) / 24
        return (60.0 / self.bpm) / self.ppqn

    def start_clock(self):
        """Start sending MIDI clock"""
        self.clock_running = True
        self.send_start()

    def stop_clock(self):
        """Stop sending MIDI clock"""
        self.clock_running = False
        self.send_stop()

    def tick_clock(self):
        """
        Send clock tick if enough time has passed
        Call this in main loop

        Returns:
            True if tick was sent
        """
        if not self.clock_running:
            return False

        current_time = time.time()
        interval = self.get_clock_interval()

        if current_time - self.last_clock_time >= interval:
            self.send_clock_tick()
            return True

        return False


class RenoiseSync(MIDISync):
    """
    Extended sync class specifically for Renoise integration
    Implements same logic as com.renoise.no3zchanger.xrnx
    """

    def __init__(self, midi_processor: Optional[MIDIProcessor] = None):
        super().__init__(midi_processor)

        # Renoise-specific
        self.previous_position = 0
        self.pattern_length = 64  # Default from original script

    def update_position(self, sequence: int, line: int):
        """
        Update and send position (only if changed)
        Mimics idle_handler from original script

        Args:
            sequence: Current pattern sequence (1-based)
            line: Current line in pattern (1-based)
        """
        measure = self.calculate_position(sequence, line)

        # Only send if position changed
        if self.previous_position != measure:
            self.send_song_position(measure)
            self.previous_position = measure


if __name__ == '__main__':
    # Test MIDI sync
    print("Orchid-Pi MIDI Sync Test\n" + "=" * 50)

    processor = MIDIProcessor()
    sync = RenoiseSync(processor)

    # Try to create virtual output
    if processor.get_available_output_ports():
        processor.open_output_port(0)
    else:
        processor.create_virtual_output("Orchid-Pi Sync Test")

    print(f"\nMIDI Output: {processor.output_port}")

    # Test Renoise position calculation
    print("\nRenoise Position Calculation Test:")
    test_positions = [
        (1, 1),   # Start of first pattern
        (1, 16),  # One beat in
        (2, 1),   # Start of second pattern
        (2, 16),
        (3, 1),
    ]

    for seq, line in test_positions:
        pos = sync.calculate_position(seq, line)
        print(f"  Sequence {seq}, Line {line:2d} → Position {pos}")

    # Test sending position
    print("\nSending position updates...")
    for seq, line in test_positions:
        sync.update_position(seq, line)
        time.sleep(0.2)

    print("\nTest complete!")
    processor.close()
