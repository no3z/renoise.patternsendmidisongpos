"""
Base Performance Mode for Orchid-Pi
Abstract base class for all performance modes
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from midi.midi_router import MIDIRouter


class PerformanceMode(ABC):
    """
    Abstract base class for performance modes
    All performance modes inherit from this
    """

    def __init__(self, name: str, midi_router: Optional[MIDIRouter] = None):
        self.name = name
        self.midi_router = midi_router
        self.enabled = False

    @abstractmethod
    def process(self, notes: List[int], velocity: int = 100):
        """
        Process and send notes according to performance mode

        Args:
            notes: List of MIDI note numbers
            velocity: Note velocity (0-127)
        """
        pass

    @abstractmethod
    def stop(self):
        """Stop any active notes or ongoing processes"""
        pass

    def enable(self):
        """Enable this performance mode"""
        self.enabled = True

    def disable(self):
        """Disable this performance mode"""
        self.enabled = False
        self.stop()

    def set_midi_router(self, midi_router: MIDIRouter):
        """Set MIDI router for output"""
        self.midi_router = midi_router

    def __str__(self):
        return f"{self.name} ({'ON' if self.enabled else 'OFF'})"
