"""
Core module for Orchid-Pi
Contains music theory, chord generation, voice-leading, and progressions
"""

from .music_theory import MusicTheory, CHORD_FORMULAS, SCALE_FORMULAS, NOTES
from .voice_leading import VoiceLeading
from .chord_engine import ChordEngine
from .chord_progressions import PROGRESSIONS, get_all_genres, get_progressions_for_genre
from .progression_player import ProgressionPlayer
from .extended_progressions import merge_progressions

# Merge extended progressions with base progressions
PROGRESSIONS = merge_progressions()

__all__ = [
    'MusicTheory',
    'VoiceLeading',
    'ChordEngine',
    'ProgressionPlayer',
    'CHORD_FORMULAS',
    'SCALE_FORMULAS',
    'NOTES',
    'PROGRESSIONS',
    'get_all_genres',
    'get_progressions_for_genre'
]
