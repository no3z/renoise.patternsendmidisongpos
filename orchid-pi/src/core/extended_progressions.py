"""
Extended Chord Progressions Library for Orchid-Pi
Includes progressions from popular songs and databases
"""

# Adding more progressions from Hooktheory, Billboard charts, and popular songs

EXTENDED_PROGRESSIONS = {
    # ===== FAMOUS SONGS =====
    "famous_songs": {
        "let-it-be": {
            "name": "Let It Be (Beatles)",
            "description": "One of the most iconic progressions ever.",
            "progression": [
                ("I", "major"),
                ("V", "major"),
                ("vi", "minor"),
                ("IV", "major")
            ],
            "examples": ["Let It Be, No Woman No Cry, With or Without You"]
        },
        "dont-stop-believing": {
            "name": "Don't Stop Believin' (Journey)",
            "description": "Stadium rock anthem progression.",
            "progression": [
                ("I", "major"),
                ("V", "major"),
                ("vi", "minor"),
                ("IV", "major")
            ],
            "examples": ["Don't Stop Believin', Someone Like You"]
        },
        "wonderwall": {
            "name": "Wonderwall (Oasis)",
            "description": "Iconic 90s britpop progression.",
            "progression": [
                ("IV", "major"),
                ("V", "major"),
                ("I", "major"),
                ("vi", "minor")
            ],
            "examples": ["Wonderwall, Jar of Hearts"]
        },
        "hallelujah": {
            "name": "Hallelujah (Leonard Cohen)",
            "description": "Emotional, spiritual progression.",
            "progression": [
                ("I", "major"),
                ("IV", "major"),
                ("V", "major"),
                ("vi", "minor"),
                ("IV", "major")
            ],
            "examples": ["Hallelujah (many versions)"]
        },
        "someone-like-you": {
            "name": "Someone Like You (Adele)",
            "description": "Modern ballad progression.",
            "progression": [
                ("I", "major"),
                ("V", "major"),
                ("vi", "minor"),
                ("IV", "major")
            ],
            "examples": ["Someone Like You, Let Her Go"]
        },
        "hotel-california": {
            "name": "Hotel California (Eagles)",
            "description": "Minor key classic rock.",
            "progression": [
                ("i", "minor"),
                ("V", "major"),
                ("bVII", "major"),
                ("IV", "major"),
                ("bVI", "major"),
                ("bIII", "major"),
                ("bVII", "major"),
                ("i", "minor")
            ],
            "examples": ["Hotel California"]
        },
        "creep": {
            "name": "Creep (Radiohead)",
            "description": "Grunge/alternative classic.",
            "progression": [
                ("I", "major"),
                ("III", "major"),
                ("IV", "major"),
                ("iv", "minor")
            ],
            "examples": ["Creep, Air That I Breathe"]
        },
    },

    # ===== BILLBOARD HITS =====
    "billboard": {
        "shape-of-you": {
            "name": "Shape of You (Ed Sheeran)",
            "description": "Modern pop minimalism.",
            "progression": [
                ("vi", "minor"),
                ("IV", "major"),
                ("I", "major"),
                ("V", "major")
            ],
            "examples": ["Shape of You, Cheap Thrills"]
        },
        "despacito": {
            "name": "Despacito (Luis Fonsi)",
            "description": "Latin pop reggaeton.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("bVI", "major"),
                ("V", "major")
            ],
            "examples": ["Despacito, Havana"]
        },
        "counting-stars": {
            "name": "Counting Stars (OneRepublic)",
            "description": "Upbeat pop/rock.",
            "progression": [
                ("vi", "minor"),
                ("IV", "major"),
                ("I", "major"),
                ("V", "major")
            ],
            "examples": ["Counting Stars, Apologize"]
        },
    },

    # ===== MOVIE/TV THEMES =====
    "soundtrack": {
        "pirates-caribbean": {
            "name": "Pirates of the Caribbean",
            "description": "Epic adventure theme.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("bVI", "major"),
                ("V", "major")
            ],
            "examples": ["He's a Pirate"]
        },
        "game-of-thrones": {
            "name": "Game of Thrones Theme",
            "description": "Dark, medieval progression.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("i", "minor"),
                ("bVI", "major")
            ],
            "examples": ["GoT Theme, The Witcher"]
        },
    },

    # ===== COUNTRY =====
    "country": {
        "country-classic": {
            "name": "Country Classic",
            "description": "Traditional country sound.",
            "progression": [
                ("I", "major"),
                ("IV", "major"),
                ("I", "major"),
                ("V", "major")
            ],
            "examples": ["Ring of Fire, Folsom Prison Blues"]
        },
        "country-modern": {
            "name": "Modern Country Pop",
            "description": "Contemporary country-pop hybrid.",
            "progression": [
                ("I", "major"),
                ("V", "major"),
                ("vi", "minor"),
                ("IV", "major")
            ],
            "examples": ["Need You Now, Cruise"]
        },
    },

    # ===== REGGAE / SKA =====
    "reggae": {
        "reggae-classic": {
            "name": "Reggae Classic",
            "description": "Classic reggae offbeat.",
            "progression": [
                ("I", "major"),
                ("IV", "major"),
                ("I", "major"),
                ("V", "major")
            ],
            "examples": ["Three Little Birds, One Love"]
        },
        "reggae-minor": {
            "name": "Minor Reggae",
            "description": "Minor key reggae vibes.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("bVI", "major"),
                ("V", "major")
            ],
            "examples": ["Redemption Song"]
        },
    },

    # ===== CLASSICAL-INSPIRED =====
    "classical": {
        "pachelbel-canon": {
            "name": "Pachelbel's Canon",
            "description": "One of the most reused progressions.",
            "progression": [
                ("I", "major"),
                ("V", "major"),
                ("vi", "minor"),
                ("iii", "minor"),
                ("IV", "major"),
                ("I", "major"),
                ("IV", "major"),
                ("V", "major")
            ],
            "examples": ["Canon in D, Graduation Song"]
        },
        "circle-of-fifths": {
            "name": "Circle of Fifths",
            "description": "Moving through the circle.",
            "progression": [
                ("I", "maj7"),
                ("IV", "maj7"),
                ("vii", "min7b5"),
                ("iii", "min7"),
                ("vi", "min7"),
                ("ii", "min7"),
                ("V", "dom7")
            ],
            "examples": ["Autumn Leaves, Fly Me to the Moon"]
        },
    },

    # ===== FUNK / SOUL =====
    "funk": {
        "funk-vamp": {
            "name": "Funk Vamp",
            "description": "Groove-based funk loop.",
            "progression": [
                ("i", "min7"),
                ("IV", "dom7")
            ],
            "examples": ["Superstition, Cissy Strut"]
        },
        "funk-extended": {
            "name": "Extended Funk",
            "description": "Complex funk with passing chords.",
            "progression": [
                ("i", "min9"),
                ("iv", "min9"),
                ("i", "min9"),
                ("bVII", "dom9")
            ],
            "examples": ["Chameleon, Cantaloupe Island"]
        },
    },

    # ===== METAL =====
    "metal": {
        "metal-power": {
            "name": "Power Metal",
            "description": "Epic power metal progression.",
            "progression": [
                ("i", "minor"),
                ("bVI", "major"),
                ("bVII", "major"),
                ("i", "minor")
            ],
            "examples": ["Thrash/Power metal"]
        },
        "metal-doom": {
            "name": "Doom Metal",
            "description": "Heavy, crushing progression.",
            "progression": [
                ("i", "minor"),
                ("bVI", "major"),
                ("bIII", "major"),
                ("bVII", "major")
            ],
            "examples": ["Black Sabbath style"]
        },
    },
}


def merge_progressions():
    """Merge extended progressions with base progressions"""
    from .chord_progressions import PROGRESSIONS

    merged = dict(PROGRESSIONS)

    for genre, progs in EXTENDED_PROGRESSIONS.items():
        if genre in merged:
            merged[genre].update(progs)
        else:
            merged[genre] = progs

    return merged


if __name__ == '__main__':
    # Test
    merged = merge_progressions()

    print(f"Total genres: {len(merged)}")
    for genre, progs in merged.items():
        print(f"{genre}: {len(progs)} progressions")

    total = sum(len(progs) for progs in merged.values())
    print(f"\nTotal progressions: {total}")
