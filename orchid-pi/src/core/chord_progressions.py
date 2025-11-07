"""
Chord Progressions Library for Orchid-Pi
Comprehensive collection of chord progressions from various genres
"""

# Chord progressions are defined using Roman numeral notation
# Format: (numeral, chord_quality)
# Numeral: I, II, III, IV, V, VI, VII (uppercase = major root, lowercase = minor root)
# Qualities: see CHORD_FORMULAS in music_theory.py

PROGRESSIONS = {
    # ===== POP / ROCK =====
    "pop": {
        "I-V-vi-IV": {
            "name": "Pop Hits (Axis of Awesome)",
            "description": "The most popular pop progression. Used in thousands of hits.",
            "progression": [
                ("I", "major"),
                ("V", "major"),
                ("vi", "minor"),
                ("IV", "major")
            ],
            "examples": ["Let It Be, With or Without You, No Woman No Cry"]
        },
        "I-IV-V-I": {
            "name": "Classic Rock",
            "description": "The foundation of rock music. Simple and powerful.",
            "progression": [
                ("I", "major"),
                ("IV", "major"),
                ("V", "major"),
                ("I", "major")
            ],
            "examples": ["Louie Louie, La Bamba, Wild Thing"]
        },
        "vi-IV-I-V": {
            "name": "Sensitive/Emo",
            "description": "Emotional and melancholic. Common in ballads and emo.",
            "progression": [
                ("vi", "minor"),
                ("IV", "major"),
                ("I", "major"),
                ("V", "major")
            ],
            "examples": ["Grenade, Apologize"]
        },
        "I-vi-IV-V": {
            "name": "50s Progression (Doo-Wop)",
            "description": "Classic 1950s progression. Nostalgic sound.",
            "progression": [
                ("I", "major"),
                ("vi", "minor"),
                ("IV", "major"),
                ("V", "major")
            ],
            "examples": ["Stand By Me, Every Breath You Take"]
        },
        "I-V-vi-iii-IV-I-IV-V": {
            "name": "Canon in D",
            "description": "Pachelbel's Canon progression. Very popular in pop.",
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
            "examples": ["Canon in D, numerous pop songs"]
        },
    },

    # ===== JAZZ =====
    "jazz": {
        "ii-V-I": {
            "name": "Jazz Turnaround",
            "description": "The most important progression in jazz. Foundation of improvisation.",
            "progression": [
                ("ii", "min7"),
                ("V", "dom7"),
                ("I", "maj7")
            ],
            "examples": ["Countless jazz standards"]
        },
        "I-vi-ii-V": {
            "name": "Rhythm Changes (A section)",
            "description": "From 'I Got Rhythm'. Very common in bebop.",
            "progression": [
                ("I", "maj7"),
                ("vi", "min7"),
                ("ii", "min7"),
                ("V", "dom7")
            ],
            "examples": ["I Got Rhythm, Anthropology"]
        },
        "iii-vi-ii-V-I": {
            "name": "Extended Jazz Turnaround",
            "description": "Extended version with smooth voice leading.",
            "progression": [
                ("iii", "min7"),
                ("vi", "min7"),
                ("ii", "min7"),
                ("V", "dom7"),
                ("I", "maj7")
            ],
            "examples": ["Autumn Leaves, All The Things You Are"]
        },
        "I-IV-bVII-IV": {
            "name": "Modal Jazz",
            "description": "Mixolydian modal progression. Miles Davis style.",
            "progression": [
                ("I", "dom7"),
                ("IV", "dom7"),
                ("bVII", "dom7"),
                ("IV", "dom7")
            ],
            "examples": ["So What (Miles Davis)"]
        },
        "Im-bIIImaj7-bVImaj7-bVIImaj7": {
            "name": "Minor Jazz Ballad",
            "description": "Beautiful minor jazz ballad progression.",
            "progression": [
                ("i", "min7"),
                ("bIII", "maj7"),
                ("bVI", "maj7"),
                ("bVII", "dom7")
            ],
            "examples": ["Round Midnight"]
        },
        "Imaj7-bIIImaj7-IVmaj7": {
            "name": "Coltrane Changes",
            "description": "Giant Steps progression. Advanced harmonic movement.",
            "progression": [
                ("I", "maj7"),
                ("bIII", "maj7"),
                ("bVI", "maj7"),
                ("II", "maj7"),
                ("IV", "maj7"),
                ("bVII", "maj7")
            ],
            "examples": ["Giant Steps"]
        },
    },

    # ===== BLUES =====
    "blues": {
        "12-bar-blues": {
            "name": "12-Bar Blues",
            "description": "The classic 12-bar blues progression.",
            "progression": [
                ("I", "dom7"),  # bars 1-4
                ("I", "dom7"),
                ("I", "dom7"),
                ("I", "dom7"),
                ("IV", "dom7"),  # bars 5-6
                ("IV", "dom7"),
                ("I", "dom7"),  # bars 7-8
                ("I", "dom7"),
                ("V", "dom7"),  # bars 9-10
                ("IV", "dom7"),
                ("I", "dom7"),  # bars 11-12
                ("V", "dom7")
            ],
            "examples": ["Sweet Home Chicago, The Thrill Is Gone"]
        },
        "minor-blues": {
            "name": "Minor Blues",
            "description": "12-bar blues in minor key.",
            "progression": [
                ("i", "min7"),
                ("i", "min7"),
                ("i", "min7"),
                ("i", "min7"),
                ("iv", "min7"),
                ("iv", "min7"),
                ("i", "min7"),
                ("i", "min7"),
                ("v", "min7"),
                ("iv", "min7"),
                ("i", "min7"),
                ("v", "min7")
            ],
            "examples": ["Black Magic Woman"]
        },
        "quick-change-blues": {
            "name": "Quick Change Blues",
            "description": "Variation with IV chord in bar 2.",
            "progression": [
                ("I", "dom7"),
                ("IV", "dom7"),  # Quick change!
                ("I", "dom7"),
                ("I", "dom7"),
                ("IV", "dom7"),
                ("IV", "dom7"),
                ("I", "dom7"),
                ("I", "dom7"),
                ("V", "dom7"),
                ("IV", "dom7"),
                ("I", "dom7"),
                ("V", "dom7")
            ],
            "examples": ["Route 66"]
        },
    },

    # ===== ELECTRONIC / EDM =====
    "edm": {
        "i-bVII-bVI-bVII": {
            "name": "EDM Minor",
            "description": "Dark and driving. Common in progressive house.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("bVI", "major"),
                ("bVII", "major")
            ],
            "examples": ["Many progressive house tracks"]
        },
        "I-bVII-IV": {
            "name": "Mixolydian EDM",
            "description": "Bright and energetic. Festival anthems.",
            "progression": [
                ("I", "major"),
                ("bVII", "major"),
                ("IV", "major")
            ],
            "examples": ["Swedish House Mafia style"]
        },
        "vi-IV-I-V-repeat": {
            "name": "EDM Pop Crossover",
            "description": "Pop-influenced EDM. Vocal friendly.",
            "progression": [
                ("vi", "minor"),
                ("IV", "major"),
                ("I", "major"),
                ("V", "major")
            ],
            "examples": ["Avicii, The Chainsmokers style"]
        },
    },

    # ===== R&B / SOUL =====
    "rnb": {
        "I-iii-IV-iv": {
            "name": "Soul Progression",
            "description": "Smooth R&B with chromatic iv chord.",
            "progression": [
                ("I", "maj7"),
                ("iii", "min7"),
                ("IV", "maj7"),
                ("iv", "min7")  # Chromatic descent
            ],
            "examples": ["Isn't She Lovely"]
        },
        "I-V-vi-iii-IV-I-ii-V": {
            "name": "Neo-Soul Extended",
            "description": "Complex neo-soul progression.",
            "progression": [
                ("I", "maj9"),
                ("V", "dom9"),
                ("vi", "min9"),
                ("iii", "min7"),
                ("IV", "maj9"),
                ("I", "maj9"),
                ("ii", "min9"),
                ("V", "dom9")
            ],
            "examples": ["D'Angelo, Erykah Badu style"]
        },
    },

    # ===== LATIN / BOSSA NOVA =====
    "latin": {
        "iim7-V7-Imaj7": {
            "name": "Bossa Nova",
            "description": "Classic bossa nova turnaround.",
            "progression": [
                ("ii", "min7"),
                ("V", "dom7"),
                ("I", "maj7"),
                ("I", "maj7")
            ],
            "examples": ["Girl From Ipanema"]
        },
        "Im-IVm-V7-Im": {
            "name": "Andalusian Cadence",
            "description": "Spanish/Flamenco sound.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("bVI", "major"),
                ("V", "major")
            ],
            "examples": ["Hit The Road Jack"]
        },
    },

    # ===== AMBIENT / ATMOSPHERIC =====
    "ambient": {
        "I-bVII-bVI": {
            "name": "Ambient Descending",
            "description": "Dreamy descending progression.",
            "progression": [
                ("I", "maj7"),
                ("bVII", "maj7"),
                ("bVI", "maj7")
            ],
            "examples": ["Brian Eno style"]
        },
        "Im-bVImaj7-bIIImaj7-bVIImaj7": {
            "name": "Minor Ambient",
            "description": "Dark and atmospheric.",
            "progression": [
                ("i", "min9"),
                ("bVI", "maj9"),
                ("bIII", "maj9"),
                ("bVII", "maj7")
            ],
            "examples": ["Post-rock, ambient"]
        },
    },

    # ===== INDIE / ALTERNATIVE =====
    "indie": {
        "I-III-vi-IV": {
            "name": "Indie Rock",
            "description": "Alternative progression with major III.",
            "progression": [
                ("I", "major"),
                ("III", "major"),  # Major instead of minor
                ("vi", "minor"),
                ("IV", "major")
            ],
            "examples": ["Indie bands"]
        },
        "vi-V-IV-V": {
            "name": "Sad Indie",
            "description": "Melancholic indie progression.",
            "progression": [
                ("vi", "minor"),
                ("V", "major"),
                ("IV", "major"),
                ("V", "major")
            ],
            "examples": ["Radiohead style"]
        },
    },

    # ===== GOSPEL / CHRISTIAN =====
    "gospel": {
        "I-IV-I-V-IV-I": {
            "name": "Gospel Progression",
            "description": "Uplifting gospel sound.",
            "progression": [
                ("I", "maj7"),
                ("IV", "maj7"),
                ("I", "maj7"),
                ("V", "dom7"),
                ("IV", "maj7"),
                ("I", "maj7")
            ],
            "examples": ["Gospel music"]
        },
        "IV-I-IV-V": {
            "name": "Contemporary Christian",
            "description": "Modern worship progression.",
            "progression": [
                ("IV", "major"),
                ("I", "major"),
                ("IV", "major"),
                ("V", "major")
            ],
            "examples": ["Hillsong style"]
        },
    },

    # ===== HIP-HOP / TRAP =====
    "hiphop": {
        "i-bIII-bVII-bVI": {
            "name": "Dark Trap",
            "description": "Menacing trap progression.",
            "progression": [
                ("i", "minor"),
                ("bIII", "major"),
                ("bVII", "major"),
                ("bVI", "major")
            ],
            "examples": ["Modern trap"]
        },
        "i-iv-bVII-bVI": {
            "name": "Boom Bap",
            "description": "Classic hip-hop sound.",
            "progression": [
                ("i", "min7"),
                ("iv", "min7"),
                ("bVII", "dom7"),
                ("bVI", "maj7")
            ],
            "examples": ["90s hip-hop"]
        },
    },
}


def get_all_genres():
    """Get list of all genre categories"""
    return list(PROGRESSIONS.keys())


def get_progressions_for_genre(genre):
    """Get all progressions for a specific genre"""
    return PROGRESSIONS.get(genre, {})


def get_all_progressions_flat():
    """Get all progressions as flat list with genre tags"""
    flat = []
    for genre, progs in PROGRESSIONS.items():
        for prog_id, prog_data in progs.items():
            flat.append({
                'id': f"{genre}_{prog_id}",
                'genre': genre,
                'key': prog_id,
                **prog_data
            })
    return flat


def search_progressions(query):
    """Search progressions by name or description"""
    query = query.lower()
    results = []

    for prog in get_all_progressions_flat():
        if (query in prog['name'].lower() or
            query in prog['description'].lower() or
            query in ' '.join(prog['examples']).lower()):
            results.append(prog)

    return results


if __name__ == '__main__':
    # Demo
    print("Orchid-Pi Chord Progressions Library")
    print("=" * 60)

    print(f"\nTotal genres: {len(get_all_genres())}")
    print(f"Total progressions: {len(get_all_progressions_flat())}")

    print("\n\nGenres available:")
    for genre in get_all_genres():
        progs = get_progressions_for_genre(genre)
        print(f"  {genre.upper()}: {len(progs)} progressions")

    print("\n\nSample progression (ii-V-I):")
    jazz_progs = get_progressions_for_genre('jazz')
    ii_v_i = jazz_progs['ii-V-I']
    print(f"  Name: {ii_v_i['name']}")
    print(f"  Description: {ii_v_i['description']}")
    print(f"  Chords: {ii_v_i['progression']}")

    print("\n\nSearch 'blues':")
    results = search_progressions('blues')
    for r in results:
        print(f"  - {r['name']} ({r['genre']})")
