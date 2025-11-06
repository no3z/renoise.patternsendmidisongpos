"""
Core module for Orchid-Pi
Contains music theory, chord generation, and voice-leading
"""

from .music_theory import MusicTheory, CHORD_FORMULAS, SCALE_FORMULAS, NOTES
from .voice_leading import VoiceLeading
from .chord_engine import ChordEngine

__all__ = [
    'MusicTheory',
    'VoiceLeading',
    'ChordEngine',
    'CHORD_FORMULAS',
    'SCALE_FORMULAS',
    'NOTES'
]
