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

    # ===== JAZZ - PAT METHENY STYLE =====
    "jazz": {
        "metheny-bright": {
            "name": "Metheny Bright Sound",
            "description": "Lush major extensions, Pat Metheny signature.",
            "progression": [
                ("I", "maj9"),
                ("II", "maj9"),
                ("iii", "min11"),
                ("vi", "min9"),
                ("ii", "min11"),
                ("V", "dom9"),
                ("I", "maj13")
            ],
            "examples": ["Phase Dance, James"]
        },
        "metheny-modal": {
            "name": "Modal Jazz (Lydian)",
            "description": "Floating modal harmony.",
            "progression": [
                ("I", "maj7#11"),
                ("II", "maj7"),
                ("I", "maj9#11"),
                ("bVII", "maj9")
            ],
            "examples": ["Better Days Ahead"]
        },
        "metheny-suspended": {
            "name": "Suspended Progressions",
            "description": "Sus chords with rich extensions.",
            "progression": [
                ("I", "sus2"),
                ("IV", "add9"),
                ("V", "sus4"),
                ("I", "maj9")
            ],
            "examples": ["So May It Secretly Begin"]
        },
        "jazz-251-extended": {
            "name": "II-V-I Extended",
            "description": "Classic jazz with extensions.",
            "progression": [
                ("ii", "min9"),
                ("V", "dom13"),
                ("I", "maj9#11"),
                ("vi", "min11")
            ],
            "examples": ["Standard jazz progression"]
        },
        "jazz-251-altered": {
            "name": "II-V-I Altered",
            "description": "II-V-I with altered dominants.",
            "progression": [
                ("ii", "min11"),
                ("V", "dom7#5"),
                ("I", "maj9"),
                ("IV", "dom7#11")
            ],
            "examples": ["Modern jazz standards"]
        },
        "coltrane-changes": {
            "name": "Coltrane Changes",
            "description": "Giant Steps style key centers.",
            "progression": [
                ("I", "maj7"),
                ("bIII", "dom7"),
                ("bVI", "maj7"),
                ("II", "dom7"),
                ("IV", "maj7"),
                ("V", "dom7")
            ],
            "examples": ["Giant Steps, Countdown"]
        },
        "jazz-minor-modal": {
            "name": "Minor Modal Jazz",
            "description": "Dorian/Aeolian modal minor.",
            "progression": [
                ("i", "min9"),
                ("iv", "min11"),
                ("bVII", "dom9"),
                ("bIII", "maj9")
            ],
            "examples": ["So What, Impressions"]
        },
        "jazz-ballad": {
            "name": "Jazz Ballad",
            "description": "Lush ballad with rich harmonies.",
            "progression": [
                ("I", "maj9"),
                ("vi", "min9"),
                ("ii", "min11"),
                ("V", "dom13"),
                ("iii", "min9"),
                ("vi", "min7"),
                ("ii", "min9"),
                ("V", "dom7b9")
            ],
            "examples": ["Body and Soul, Misty"]
        },
        "jazz-quartal": {
            "name": "Quartal Harmony",
            "description": "Chords built in perfect fourths.",
            "progression": [
                ("I", "sus4"),
                ("bVII", "sus4"),
                ("IV", "sus4"),
                ("V", "sus4")
            ],
            "examples": ["McCoy Tyner style voicings"]
        },
        "jazz-turnaround": {
            "name": "Jazz Turnaround",
            "description": "Classic I-VI-II-V.",
            "progression": [
                ("I", "maj9"),
                ("vi", "min7"),
                ("ii", "min9"),
                ("V", "dom13")
            ],
            "examples": ["Rhythm Changes, Blue Bossa"]
        },
        "metheny-chromatic": {
            "name": "Metheny Chromatic",
            "description": "Chromatic voice leading, rich textures.",
            "progression": [
                ("I", "maj9"),
                ("bII", "maj9"),
                ("I", "maj13#11"),
                ("bVII", "maj9"),
                ("IV", "maj9"),
                ("bIII", "maj7#11")
            ],
            "examples": ["Letter From Home"]
        },
        "jazz-blues-extended": {
            "name": "Jazz Blues",
            "description": "12-bar blues with jazz extensions.",
            "progression": [
                ("I", "dom9"),
                ("IV", "dom9"),
                ("I", "dom13"),
                ("I", "dom7"),
                ("IV", "dom9"),
                ("IV", "dom13"),
                ("I", "dom9"),
                ("vi", "min9"),
                ("ii", "min9"),
                ("V", "dom7#9"),
                ("I", "dom9"),
                ("V", "dom13")
            ],
            "examples": ["Tenor Madness, Freddie Freeloader"]
        },
        "metheny-parallel": {
            "name": "Parallel Harmony",
            "description": "Parallel chord movement, Metheny style.",
            "progression": [
                ("I", "maj9"),
                ("bVII", "maj9"),
                ("bVI", "maj9"),
                ("V", "maj9")
            ],
            "examples": ["Are You Going With Me?"]
        },
        "jazz-bossa": {
            "name": "Bossa Nova Jazz",
            "description": "Brazilian jazz with extensions.",
            "progression": [
                ("I", "maj9"),
                ("II", "min7"),
                ("ii", "min9"),
                ("V", "dom7b9"),
                ("I", "maj13")
            ],
            "examples": ["Girl from Ipanema, Desafinado"]
        },
        "jazz-tritone-sub": {
            "name": "Tritone Substitution",
            "description": "II-V with tritone subs.",
            "progression": [
                ("ii", "min11"),
                ("bII", "dom13"),
                ("I", "maj9#11"),
                ("bVI", "dom9")
            ],
            "examples": ["Advanced jazz harmony"]
        },
        "bill-evans-waltz": {
            "name": "Bill Evans Waltz",
            "description": "Romantic jazz waltz harmonies.",
            "progression": [
                ("I", "maj9"),
                ("IV", "maj9#11"),
                ("iii", "min9"),
                ("vi", "min11"),
                ("ii", "min11"),
                ("V", "dom13"),
                ("I", "maj13")
            ],
            "examples": ["Waltz for Debby, My Foolish Heart"]
        },
        "keith-jarrett-modal": {
            "name": "Keith Jarrett Modal",
            "description": "Expansive modal explorations.",
            "progression": [
                ("I", "maj9"),
                ("bVII", "maj9"),
                ("I", "sus2"),
                ("bVII", "sus4"),
                ("I", "maj13#11")
            ],
            "examples": ["The Köln Concert style"]
        },
        "herbie-maiden-voyage": {
            "name": "Maiden Voyage",
            "description": "Herbie Hancock suspended fourths.",
            "progression": [
                ("I", "sus4"),
                ("II", "sus4"),
                ("iii", "sus4"),
                ("IV", "sus4")
            ],
            "examples": ["Maiden Voyage"]
        },
        "chick-corea-spanish": {
            "name": "Chick Corea Spanish",
            "description": "Spanish-influenced jazz harmony.",
            "progression": [
                ("i", "min9"),
                ("bVI", "maj7"),
                ("bVII", "dom9"),
                ("i", "min11"),
                ("bII", "maj7#11")
            ],
            "examples": ["Spain, Armando's Rhumba"]
        },
        "wayne-shorter-pentatonic": {
            "name": "Wayne Shorter Pentatonic",
            "description": "Ambiguous pentatonic harmony.",
            "progression": [
                ("I", "sus2"),
                ("bVII", "sus2"),
                ("bIII", "maj7"),
                ("bVI", "maj9")
            ],
            "examples": ["Footprints, Speak No Evil"]
        },
        "brad-mehldau-altered": {
            "name": "Brad Mehldau Altered",
            "description": "Contemporary altered harmony.",
            "progression": [
                ("I", "maj9#11"),
                ("bVII", "dom13"),
                ("bVI", "maj9"),
                ("ii", "min11"),
                ("V", "dom7#5")
            ],
            "examples": ["Modern jazz standards reharmonization"]
        },
        "jazz-pedal-point": {
            "name": "Pedal Point Harmony",
            "description": "Static bass with moving harmony.",
            "progression": [
                ("I", "maj9"),
                ("I", "maj9#11"),
                ("I", "maj13"),
                ("I", "maj7")
            ],
            "examples": ["Naima, So What"]
        },
        "jazz-descending-cycle": {
            "name": "Descending Cycle",
            "description": "Descending harmonic movement.",
            "progression": [
                ("I", "maj9"),
                ("bVII", "maj7"),
                ("bVI", "maj9"),
                ("V", "dom13"),
                ("IV", "maj9#11"),
                ("bIII", "maj7")
            ],
            "examples": ["Sophisticated harmonic descent"]
        },
    },

    # ===== GOSPEL =====
    "gospel": {
        "gospel-251": {
            "name": "Gospel II-V-I",
            "description": "Classic gospel with passing chords.",
            "progression": [
                ("ii", "min9"),
                ("V", "dom13"),
                ("I", "maj9"),
                ("vi", "min7")
            ],
            "examples": ["Traditional gospel sound"]
        },
        "gospel-chromatic-walkdown": {
            "name": "Gospel Chromatic Walkdown",
            "description": "Chromatic bass movement.",
            "progression": [
                ("I", "maj9"),
                ("I", "maj7"),
                ("bVII", "dom7"),
                ("vi", "min9"),
                ("bVI", "maj7"),
                ("V", "dom13")
            ],
            "examples": ["Kirk Franklin style"]
        },
        "gospel-extended": {
            "name": "Extended Gospel",
            "description": "Rich extended harmonies.",
            "progression": [
                ("I", "maj13"),
                ("IV", "maj9"),
                ("iii", "min11"),
                ("vi", "min9"),
                ("ii", "min11"),
                ("V", "dom13"),
                ("I", "maj9")
            ],
            "examples": ["Contemporary gospel"]
        },
        "gospel-pentecostal": {
            "name": "Pentecostal Gospel",
            "description": "Energetic pentecostal progression.",
            "progression": [
                ("I", "maj7"),
                ("IV", "maj9"),
                ("I", "maj7"),
                ("V", "dom9"),
                ("IV", "maj9"),
                ("I", "maj13")
            ],
            "examples": ["Uplifting church music"]
        },
        "gospel-turnaround-extended": {
            "name": "Gospel Turnaround",
            "description": "Extended gospel turnaround.",
            "progression": [
                ("I", "maj9"),
                ("vi", "min9"),
                ("IV", "maj9"),
                ("iii", "min7"),
                ("ii", "min11"),
                ("V", "dom13")
            ],
            "examples": ["Gospel ending progression"]
        },
    },

    # ===== NEO-SOUL =====
    "neo_soul": {
        "neo-soul-basic": {
            "name": "Neo-Soul Basic",
            "description": "Smooth neo-soul vibe.",
            "progression": [
                ("i", "min9"),
                ("iv", "min11"),
                ("bVII", "maj9"),
                ("bIII", "maj7")
            ],
            "examples": ["D'Angelo, Erykah Badu"]
        },
        "neo-soul-extended": {
            "name": "Neo-Soul Extended",
            "description": "Lush extended neo-soul harmonies.",
            "progression": [
                ("i", "min11"),
                ("bVII", "maj9"),
                ("bVI", "maj13"),
                ("V", "dom7#9")
            ],
            "examples": ["Robert Glasper, BBNG"]
        },
        "neo-soul-fusion": {
            "name": "Neo-Soul Jazz Fusion",
            "description": "Jazz-influenced neo-soul.",
            "progression": [
                ("i", "min9"),
                ("ii", "min11"),
                ("bIII", "maj9#11"),
                ("bVII", "dom13")
            ],
            "examples": ["Hiatus Kaiyote, Tom Misch"]
        },
        "neo-soul-rnb": {
            "name": "Neo-Soul R&B",
            "description": "Modern R&B with jazz chords.",
            "progression": [
                ("I", "maj9"),
                ("iii", "min11"),
                ("vi", "min9"),
                ("ii", "min11"),
                ("V", "dom9")
            ],
            "examples": ["H.E.R., Daniel Caesar"]
        },
        "neo-soul-modal": {
            "name": "Modal Neo-Soul",
            "description": "Modal harmony in neo-soul context.",
            "progression": [
                ("i", "min11"),
                ("i", "min9"),
                ("bVII", "maj9"),
                ("bVII", "sus4")
            ],
            "examples": ["Floating modal soul"]
        },
        "neo-soul-chromatic": {
            "name": "Chromatic Neo-Soul",
            "description": "Chromatic passing chords.",
            "progression": [
                ("i", "min9"),
                ("bVII", "maj9"),
                ("bVI", "maj7"),
                ("bV", "maj7"),
                ("iv", "min11")
            ],
            "examples": ["Anderson .Paak style"]
        },
    },

    # ===== FUSION =====
    "fusion": {
        "fusion-mahavishnu": {
            "name": "Mahavishnu Orchestra",
            "description": "Complex fusion harmony.",
            "progression": [
                ("I", "maj7#5"),
                ("bVII", "dom7#9"),
                ("bVI", "maj9"),
                ("V", "dom7#11")
            ],
            "examples": ["Birds of Fire"]
        },
        "fusion-weather-report": {
            "name": "Weather Report",
            "description": "Atmospheric fusion.",
            "progression": [
                ("I", "sus4"),
                ("bVII", "maj9"),
                ("bIII", "maj7#11"),
                ("V", "sus4")
            ],
            "examples": ["Birdland, Teen Town"]
        },
        "fusion-return-to-forever": {
            "name": "Return to Forever",
            "description": "Latin-fusion harmony.",
            "progression": [
                ("i", "min9"),
                ("iv", "min11"),
                ("bVII", "dom9"),
                ("bIII", "maj13")
            ],
            "examples": ["Romantic Warrior"]
        },
        "fusion-miles-electric": {
            "name": "Miles Electric Period",
            "description": "Electric Miles Davis sound.",
            "progression": [
                ("I", "sus4"),
                ("bVII", "dom9"),
                ("I", "sus2"),
                ("bVII", "sus4")
            ],
            "examples": ["In a Silent Way, Bitches Brew"]
        },
        "fusion-snarky-puppy": {
            "name": "Snarky Puppy",
            "description": "Modern fusion harmonies.",
            "progression": [
                ("I", "maj9#11"),
                ("bVII", "maj9"),
                ("bVI", "maj7"),
                ("V", "sus4"),
                ("V", "dom13")
            ],
            "examples": ["Lingus, What About Me?"]
        },
        "fusion-quartal": {
            "name": "Fusion Quartal",
            "description": "Fourth-based fusion voicings.",
            "progression": [
                ("I", "sus4"),
                ("IV", "sus4"),
                ("bVII", "sus4"),
                ("bIII", "sus4")
            ],
            "examples": ["Modern jazz fusion"]
        },
    },

    # ===== LATIN JAZZ =====
    "latin_jazz": {
        "afro-cuban-montuno": {
            "name": "Afro-Cuban Montuno",
            "description": "Traditional Afro-Cuban jazz.",
            "progression": [
                ("i", "min9"),
                ("iv", "min9"),
                ("i", "min9"),
                ("V", "dom9")
            ],
            "examples": ["Manteca, Afro Blue"]
        },
        "bossa-jobim": {
            "name": "Jobim Bossa Nova",
            "description": "Antonio Carlos Jobim style.",
            "progression": [
                ("I", "maj9"),
                ("ii", "min9"),
                ("V", "dom7b9"),
                ("I", "maj13"),
                ("IV", "maj9")
            ],
            "examples": ["Wave, One Note Samba"]
        },
        "samba-jazz": {
            "name": "Samba Jazz",
            "description": "Brazilian samba with jazz harmony.",
            "progression": [
                ("I", "maj9"),
                ("bVII", "dom9"),
                ("bVI", "maj7"),
                ("ii", "min9"),
                ("V", "dom13")
            ],
            "examples": ["Black Orpheus, Mas Que Nada"]
        },
        "latin-minor": {
            "name": "Latin Minor",
            "description": "Minor key latin jazz.",
            "progression": [
                ("i", "min9"),
                ("bVI", "maj9"),
                ("bVII", "dom9"),
                ("i", "min11")
            ],
            "examples": ["Oye Como Va, Evil Ways"]
        },
        "tumbao-progression": {
            "name": "Tumbao",
            "description": "Cuban tumbao pattern.",
            "progression": [
                ("I", "maj9"),
                ("IV", "maj9"),
                ("I", "maj7"),
                ("V", "dom9")
            ],
            "examples": ["Salsa, Timba"]
        },
    },

    # ===== R&B / CONTEMPORARY =====
    "rnb": {
        "rnb-90s": {
            "name": "90s R&B",
            "description": "Classic 90s R&B sound.",
            "progression": [
                ("I", "maj9"),
                ("iii", "min7"),
                ("vi", "min9"),
                ("ii", "min7"),
                ("V", "dom9")
            ],
            "examples": ["Boyz II Men, Jodeci"]
        },
        "rnb-contemporary": {
            "name": "Contemporary R&B",
            "description": "Modern R&B with jazz chords.",
            "progression": [
                ("I", "maj13"),
                ("vi", "min11"),
                ("IV", "maj9"),
                ("iii", "min9"),
                ("ii", "min11"),
                ("V", "dom13")
            ],
            "examples": ["The Weeknd, SZA"]
        },
        "rnb-trap-soul": {
            "name": "Trap Soul",
            "description": "Trap-influenced R&B.",
            "progression": [
                ("i", "min9"),
                ("bVI", "maj7"),
                ("bVII", "maj9"),
                ("i", "min11")
            ],
            "examples": ["Bryson Tiller, 6lack"]
        },
        "rnb-ballad": {
            "name": "R&B Ballad",
            "description": "Emotional R&B ballad.",
            "progression": [
                ("I", "maj9"),
                ("vi", "min9"),
                ("IV", "maj9"),
                ("V", "dom13"),
                ("I", "maj13")
            ],
            "examples": ["Alicia Keys, John Legend"]
        },
        "rnb-alternative": {
            "name": "Alternative R&B",
            "description": "Experimental alt-R&B harmonies.",
            "progression": [
                ("i", "min11"),
                ("bVII", "maj9#11"),
                ("bVI", "maj13"),
                ("V", "dom7#9")
            ],
            "examples": ["FKA twigs, Frank Ocean"]
        },
    },

    # ===== PROGRESSIVE / EXPERIMENTAL =====
    "progressive": {
        "prog-rock-jazz": {
            "name": "Progressive Rock Jazz",
            "description": "Complex time signatures and harmony.",
            "progression": [
                ("I", "maj9"),
                ("bVII", "maj7"),
                ("bVI", "maj9#11"),
                ("bII", "maj7"),
                ("V", "dom13")
            ],
            "examples": ["Steely Dan, King Crimson"]
        },
        "modal-interchange": {
            "name": "Modal Interchange",
            "description": "Borrowed chords from parallel modes.",
            "progression": [
                ("I", "maj9"),
                ("bVII", "maj9"),
                ("IV", "min11"),
                ("bVI", "maj7"),
                ("V", "dom9")
            ],
            "examples": ["Advanced modal harmony"]
        },
        "polytonal": {
            "name": "Polytonal Harmony",
            "description": "Multiple key centers.",
            "progression": [
                ("I", "maj9"),
                ("bIII", "maj9"),
                ("bVI", "maj9"),
                ("I", "maj13#11")
            ],
            "examples": ["Modern classical jazz"]
        },
        "upper-structure": {
            "name": "Upper Structure Triads",
            "description": "Complex voicings with upper structures.",
            "progression": [
                ("ii", "min11"),
                ("V", "dom13"),
                ("I", "maj13#11"),
                ("IV", "maj9#11")
            ],
            "examples": ["Advanced jazz piano"]
        },
    },

    # ===== LOFI / CHILL =====
    "lofi": {
        "lofi-hiphop": {
            "name": "Lofi Hip-Hop",
            "description": "Relaxing lofi beats harmony.",
            "progression": [
                ("I", "maj9"),
                ("vi", "min9"),
                ("IV", "maj9"),
                ("V", "dom9")
            ],
            "examples": ["Nujabes, J Dilla"]
        },
        "lofi-jazz": {
            "name": "Lofi Jazz",
            "description": "Jazz-influenced lofi.",
            "progression": [
                ("ii", "min11"),
                ("V", "dom9"),
                ("I", "maj9"),
                ("vi", "min11")
            ],
            "examples": ["Chillhop, study beats"]
        },
        "lofi-ambient": {
            "name": "Ambient Lofi",
            "description": "Atmospheric lofi progressions.",
            "progression": [
                ("I", "maj9"),
                ("bVII", "maj9"),
                ("IV", "maj9"),
                ("I", "maj13")
            ],
            "examples": ["Ambient hip-hop"]
        },
    },

    # ===== FLAMENCO =====
    "flamenco": {
        "flamenco-phrygian": {
            "name": "Flamenco Phrygian",
            "description": "Classic flamenco Phrygian cadence.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("bVI", "major"),
                ("V", "major")
            ],
            "examples": ["Traditional flamenco, Paco de Lucía"]
        },
        "flamenco-solea": {
            "name": "Soleá",
            "description": "Soleá flamenco progression.",
            "progression": [
                ("i", "minor"),
                ("bII", "major"),
                ("i", "minor"),
                ("V", "major")
            ],
            "examples": ["Soleá por Bulerías"]
        },
        "flamenco-bulerias": {
            "name": "Bulerías",
            "description": "Upbeat bulerías progression.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("bVI", "major"),
                ("bII", "major"),
                ("i", "minor")
            ],
            "examples": ["Bulerías de Cádiz"]
        },
        "flamenco-rumba": {
            "name": "Rumba Flamenca",
            "description": "Rumba flamenco fusion.",
            "progression": [
                ("i", "min7"),
                ("bVII", "dom7"),
                ("bVI", "maj7"),
                ("V", "dom7")
            ],
            "examples": ["Gipsy Kings style"]
        },
        "flamenco-tangos": {
            "name": "Tangos Flamencos",
            "description": "Flamenco tangos progression.",
            "progression": [
                ("I", "major"),
                ("bIII", "major"),
                ("bVII", "major"),
                ("I", "major")
            ],
            "examples": ["Tangos de Málaga"]
        },
        "flamenco-alegrias": {
            "name": "Alegrías",
            "description": "Joyful alegrías in major.",
            "progression": [
                ("I", "major"),
                ("IV", "major"),
                ("V", "major"),
                ("I", "major"),
                ("vi", "minor")
            ],
            "examples": ["Alegrías de Cádiz"]
        },
    },

    # ===== INDIAN / RAGA =====
    "indian": {
        "raga-bhairav": {
            "name": "Raga Bhairav",
            "description": "Morning raga with b2 and b6.",
            "progression": [
                ("I", "major"),
                ("bII", "major"),
                ("IV", "major"),
                ("bVI", "major")
            ],
            "examples": ["Classical Hindustani morning raga"]
        },
        "raga-yaman": {
            "name": "Raga Yaman",
            "description": "Evening raga, Lydian mode.",
            "progression": [
                ("I", "maj7"),
                ("II", "maj7"),
                ("V", "dom7"),
                ("I", "maj7")
            ],
            "examples": ["Classical evening raga"]
        },
        "raga-bhupali": {
            "name": "Raga Bhupali",
            "description": "Pentatonic major raga.",
            "progression": [
                ("I", "major"),
                ("II", "sus2"),
                ("V", "sus4"),
                ("I", "major")
            ],
            "examples": ["Pentatonic evening raga"]
        },
        "raga-darbari": {
            "name": "Raga Darbari Kanada",
            "description": "Serious night raga, minor with b2.",
            "progression": [
                ("i", "minor"),
                ("bII", "major"),
                ("iv", "minor"),
                ("i", "minor")
            ],
            "examples": ["Night raga, contemplative"]
        },
        "carnatic-ragam": {
            "name": "Carnatic Ragam",
            "description": "South Indian classical progression.",
            "progression": [
                ("I", "major"),
                ("iii", "minor"),
                ("V", "major"),
                ("I", "major")
            ],
            "examples": ["Carnatic music, South India"]
        },
        "bollywood-romantic": {
            "name": "Bollywood Romantic",
            "description": "Modern Bollywood romantic sound.",
            "progression": [
                ("I", "maj9"),
                ("vi", "min7"),
                ("IV", "maj9"),
                ("V", "dom7")
            ],
            "examples": ["A.R. Rahman style"]
        },
    },

    # ===== ARABIC / MIDDLE EASTERN =====
    "arabic": {
        "maqam-hijaz": {
            "name": "Maqam Hijaz",
            "description": "Hijaz maqam with augmented 2nd.",
            "progression": [
                ("i", "minor"),
                ("bII", "major"),
                ("V", "major"),
                ("i", "minor")
            ],
            "examples": ["Traditional Arabic, Turkish music"]
        },
        "maqam-rast": {
            "name": "Maqam Rast",
            "description": "Rast maqam, joyful and bright.",
            "progression": [
                ("I", "major"),
                ("IV", "major"),
                ("V", "major"),
                ("I", "major")
            ],
            "examples": ["Classical Arabic music"]
        },
        "maqam-bayati": {
            "name": "Maqam Bayati",
            "description": "Bayati maqam, minor with raised 6th.",
            "progression": [
                ("i", "minor"),
                ("iv", "minor"),
                ("V", "major"),
                ("i", "minor")
            ],
            "examples": ["Popular in Arabic pop"]
        },
        "maqam-saba": {
            "name": "Maqam Saba",
            "description": "Saba maqam, melancholic.",
            "progression": [
                ("i", "min7b5"),
                ("bII", "maj7"),
                ("bVI", "major"),
                ("i", "min7b5")
            ],
            "examples": ["Emotional Arabic music"]
        },
        "arabic-pop": {
            "name": "Arabic Pop",
            "description": "Modern Arabic pop progression.",
            "progression": [
                ("i", "min9"),
                ("bVI", "maj7"),
                ("bVII", "dom7"),
                ("i", "min9")
            ],
            "examples": ["Amr Diab, Nancy Ajram"]
        },
        "oud-progression": {
            "name": "Oud Taqsim",
            "description": "Oud improvisation pattern.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("bVI", "major"),
                ("V", "major"),
                ("i", "minor")
            ],
            "examples": ["Traditional oud music"]
        },
    },

    # ===== AFRICAN =====
    "african": {
        "afrobeat": {
            "name": "Afrobeat",
            "description": "Fela Kuti style Afrobeat.",
            "progression": [
                ("i", "min7"),
                ("iv", "min7"),
                ("i", "min7"),
                ("bVII", "dom7")
            ],
            "examples": ["Fela Kuti, Tony Allen"]
        },
        "highlife": {
            "name": "Highlife",
            "description": "West African highlife.",
            "progression": [
                ("I", "maj7"),
                ("IV", "maj7"),
                ("V", "dom7"),
                ("I", "maj7")
            ],
            "examples": ["Ghana, Nigeria highlife"]
        },
        "soukous": {
            "name": "Soukous",
            "description": "Congolese soukous rumba.",
            "progression": [
                ("I", "major"),
                ("IV", "major"),
                ("I", "major"),
                ("V", "major")
            ],
            "examples": ["Papa Wemba, Koffi Olomide"]
        },
        "mbira": {
            "name": "Mbira Progression",
            "description": "Zimbabwean mbira pattern.",
            "progression": [
                ("I", "major"),
                ("bVII", "major"),
                ("IV", "major"),
                ("I", "major")
            ],
            "examples": ["Shona music, Thomas Mapfumo"]
        },
        "afro-jazz": {
            "name": "Afro-Jazz",
            "description": "African jazz fusion.",
            "progression": [
                ("i", "min9"),
                ("iv", "min9"),
                ("bVII", "maj9"),
                ("i", "min11")
            ],
            "examples": ["Hugh Masekela, Abdullah Ibrahim"]
        },
    },

    # ===== LATIN EXPANDED =====
    "latin_extended": {
        "tango-argentino": {
            "name": "Tango Argentino",
            "description": "Traditional Argentine tango.",
            "progression": [
                ("i", "minor"),
                ("V", "dom7"),
                ("i", "minor"),
                ("bVI", "major"),
                ("V", "dom7")
            ],
            "examples": ["Astor Piazzolla, Carlos Gardel"]
        },
        "tango-nuevo": {
            "name": "Tango Nuevo",
            "description": "Modern tango with jazz harmony.",
            "progression": [
                ("i", "min9"),
                ("bVI", "maj7"),
                ("ii", "min7b5"),
                ("V", "dom7b9")
            ],
            "examples": ["Astor Piazzolla nuevo tango"]
        },
        "salsa-son": {
            "name": "Salsa/Son",
            "description": "Cuban son progression.",
            "progression": [
                ("I", "maj7"),
                ("vi", "min7"),
                ("ii", "min7"),
                ("V", "dom7")
            ],
            "examples": ["Celia Cruz, Buena Vista Social Club"]
        },
        "mambo": {
            "name": "Mambo",
            "description": "Classic mambo progression.",
            "progression": [
                ("I", "dom7"),
                ("IV", "dom7"),
                ("I", "dom7"),
                ("V", "dom7")
            ],
            "examples": ["Pérez Prado, Tito Puente"]
        },
        "cha-cha-cha": {
            "name": "Cha-Cha-Chá",
            "description": "Cuban cha-cha-chá rhythm.",
            "progression": [
                ("I", "maj7"),
                ("IV", "maj7"),
                ("V", "dom7"),
                ("I", "maj7")
            ],
            "examples": ["Traditional cha-cha-chá"]
        },
        "bolero": {
            "name": "Bolero",
            "description": "Romantic Latin bolero.",
            "progression": [
                ("I", "maj9"),
                ("vi", "min9"),
                ("ii", "min9"),
                ("V", "dom9")
            ],
            "examples": ["Bésame Mucho, Contigo en la Distancia"]
        },
        "cumbia": {
            "name": "Cumbia",
            "description": "Colombian cumbia progression.",
            "progression": [
                ("I", "major"),
                ("V", "major"),
                ("I", "major"),
                ("IV", "major")
            ],
            "examples": ["Colombian cumbia"]
        },
        "merengue": {
            "name": "Merengue",
            "description": "Dominican merengue.",
            "progression": [
                ("I", "maj7"),
                ("IV", "maj7"),
                ("I", "maj7"),
                ("V", "dom7")
            ],
            "examples": ["Juan Luis Guerra"]
        },
    },

    # ===== GYPSY JAZZ =====
    "gypsy_jazz": {
        "django-minor": {
            "name": "Django Minor Swing",
            "description": "Gypsy jazz minor progression.",
            "progression": [
                ("i", "min6"),
                ("i", "min6"),
                ("iv", "min6"),
                ("iv", "min6"),
                ("i", "min6"),
                ("V", "dom7"),
                ("i", "min6")
            ],
            "examples": ["Minor Swing, Dark Eyes"]
        },
        "django-major": {
            "name": "Django Major Swing",
            "description": "Gypsy jazz major progression.",
            "progression": [
                ("I", "6"),
                ("vi", "min7"),
                ("ii", "min7"),
                ("V", "dom7")
            ],
            "examples": ["Djangology, Swing 42"]
        },
        "manouche-waltz": {
            "name": "Manouche Waltz",
            "description": "Gypsy waltz progression.",
            "progression": [
                ("I", "maj7"),
                ("iii", "min7"),
                ("vi", "min7"),
                ("ii", "min7"),
                ("V", "dom7")
            ],
            "examples": ["Indifférence, Nuages"]
        },
        "gypsy-blues": {
            "name": "Gypsy Blues",
            "description": "Gypsy jazz blues.",
            "progression": [
                ("i", "min6"),
                ("iv", "min6"),
                ("i", "min6"),
                ("ii", "min7b5"),
                ("V", "dom7b9")
            ],
            "examples": ["Blues Clair"]
        },
    },

    # ===== MEDITERRANEAN =====
    "mediterranean": {
        "greek-rembetiko": {
            "name": "Greek Rembetiko",
            "description": "Greek blues/rembetiko.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("i", "minor"),
                ("V", "major")
            ],
            "examples": ["Markos Vamvakaris"]
        },
        "greek-laiko": {
            "name": "Greek Laïko",
            "description": "Modern Greek laïko pop.",
            "progression": [
                ("i", "min7"),
                ("bVI", "maj7"),
                ("bVII", "dom7"),
                ("i", "min7")
            ],
            "examples": ["Contemporary Greek music"]
        },
        "turkish-hicaz": {
            "name": "Turkish Hicaz",
            "description": "Turkish hicaz makam.",
            "progression": [
                ("i", "minor"),
                ("bII", "major"),
                ("i", "minor"),
                ("bVI", "major")
            ],
            "examples": ["Traditional Turkish music"]
        },
        "balkan-oro": {
            "name": "Balkan Oro",
            "description": "Balkan dance progression.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("bVI", "major"),
                ("V", "major")
            ],
            "examples": ["Balkan brass bands"]
        },
        "sephardic": {
            "name": "Sephardic",
            "description": "Sephardic Jewish progression.",
            "progression": [
                ("i", "minor"),
                ("iv", "minor"),
                ("V", "major"),
                ("i", "minor")
            ],
            "examples": ["Ladino songs"]
        },
    },

    # ===== CELTIC =====
    "celtic": {
        "irish-jig": {
            "name": "Irish Jig",
            "description": "Traditional Irish jig.",
            "progression": [
                ("I", "major"),
                ("IV", "major"),
                ("I", "major"),
                ("V", "major")
            ],
            "examples": ["Traditional Irish dance"]
        },
        "irish-reel": {
            "name": "Irish Reel",
            "description": "Irish reel progression.",
            "progression": [
                ("I", "major"),
                ("bVII", "major"),
                ("I", "major"),
                ("bVII", "major")
            ],
            "examples": ["Irish fiddle tunes"]
        },
        "scottish-strathspey": {
            "name": "Scottish Strathspey",
            "description": "Scottish dance tune.",
            "progression": [
                ("I", "major"),
                ("IV", "major"),
                ("V", "major"),
                ("I", "major")
            ],
            "examples": ["Highland bagpipe music"]
        },
        "celtic-modal": {
            "name": "Celtic Modal",
            "description": "Dorian mode Celtic sound.",
            "progression": [
                ("i", "min7"),
                ("bVII", "maj7"),
                ("i", "min7"),
                ("IV", "maj7")
            ],
            "examples": ["Enya, Clannad"]
        },
        "gaelic-ballad": {
            "name": "Gaelic Ballad",
            "description": "Slow Gaelic ballad.",
            "progression": [
                ("i", "minor"),
                ("bVII", "major"),
                ("bVI", "major"),
                ("V", "major")
            ],
            "examples": ["Irish ballads, laments"]
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
