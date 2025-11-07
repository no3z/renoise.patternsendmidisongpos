"""
MIDI module for Orchid-Pi
Handles MIDI I/O and routing
"""

from .midi_processor import MIDIProcessor
from .midi_router import MIDIRouter

__all__ = [
    'MIDIProcessor',
    'MIDIRouter'
]
