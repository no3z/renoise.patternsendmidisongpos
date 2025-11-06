# Orchid-Pi User Guide

Complete guide to using Orchid-Pi for music creation.

---

## Getting Started

### First Launch

1. **Start Orchid-Pi**:
   ```bash
   cd ~/orchid-pi
   ./scripts/start_orchid.sh
   ```

2. **GUI appears** on touchscreen
3. **MIDI automatically detected** and connected
4. **Ready to play!**

### Interface Overview

```
┌─────────────────────────────────────────────┐
│      ORCHID-PI MIDI BRAIN           [≡]    │
├─────────────────────────────────────────────┤
│  Current Chord: Cmaj7                       │
│  Voicing: 1st Inversion                     │
├─────────────────────────────────────────────┤
│  [C][C#][D][D#][E][F][F#][G][G#][A][A#][B] │ Virtual Keyboard
├─────────────────────────────────────────────┤
│  Octave  │ Chord Type  │  Bass              │ Controls
│   ▲ 4 ▼  │  ◀ maj7 ▶   │  [ON]              │
├─────────────────────────────────────────────┤
│ [Direct][Strum][Arp][Slop][Pattern][Harp]  │ Performance Modes
├─────────────────────────────────────────────┤
│ Ready | MIDI: USB-MIDI-1                    │ Status
└─────────────────────────────────────────────┘
```

---

## Basic Usage

### Playing Chords

**Option 1: Virtual Keyboard**
- Touch any key on screen
- Chord plays immediately
- Note becomes root of chord

**Option 2: MIDI Keyboard**
- Connect USB MIDI keyboard
- Play any note
- Orchid-Pi generates full chord

**Result:**
- **Channel 1**: Full chord (3-7 notes)
- **Channel 2**: Bass note (optional)
- **Channel 3**: Performance mode output (if active)

---

## Chord Types

Orchid-Pi supports 20+ chord types:

### Triads
- **major** - Happy, bright (C-E-G)
- **minor** - Sad, dark (C-Eb-G)
- **diminished** - Tense (C-Eb-Gb)
- **augmented** - Dreamy (C-E-G#)
- **sus2** - Open, floating (C-D-G)
- **sus4** - Suspended (C-F-G)

### Seventh Chords
- **maj7** - Jazz, sophisticated (C-E-G-B)
- **min7** - Smooth, jazzy (C-Eb-G-Bb)
- **dom7** - Blues, funk (C-E-G-Bb)
- **dim7** - Very tense (C-Eb-Gb-Bbb)
- **min7b5** - Half-diminished (C-Eb-Gb-Bb)
- **aug7** - Altered, exotic (C-E-G#-Bb)

### Extended Chords
- **maj9, min9, dom9** - Rich, complex
- **maj11, min11, dom11** - Very lush
- **maj13, min13, dom13** - Maximum richness

### Add Chords
- **add9, madd9** - Add 9th without 7th
- **6, min6** - Vintage jazz sound
- **6/9** - Classic jazz chord

### Changing Chord Type

1. Look at **"Chord Type"** display
2. Press **◀** (previous) or **▶** (next)
3. Cycles through all available types
4. Current chord updates immediately

---

## Octave Control

### Changing Octave

1. Look at **"Octave"** display (shows 0-8)
2. Press **▲** (up) or **▼** (down)
3. Affects virtual keyboard range
4. Also affects MIDI input transposition

**Example:**
- Octave 3: Low chords
- Octave 4: Middle (default)
- Octave 5: High chords

---

## Bass Control

### Bass Toggle

The **Bass** button enables/disables bass note generation:

- **ON** (green): Bass note sent on Channel 2
- **OFF** (gray): No bass note

### Bass Note

- Always the root note of chord
- Transposed 1 octave down (default)
- Sent on separate MIDI channel (Ch 2)

**Use cases:**
- Route to bass synthesizer
- Create bass + chords simultaneously
- Disable for chordal pads only

---

## Performance Modes

Orchid-Pi includes 5 performance modes inspired by Orchid hardware:

### 1. Direct Mode (Default)

**Description:** No processing, chords play immediately

**Use cases:**
- Pads and sustained chords
- Direct input to synthesizers
- Maximum control

**Settings:** None

---

### 2. Strum Mode

**Description:** Guitar-style strumming with delay between notes

**Settings:**
- **Delay**: 5-100ms between notes (default: 15ms)
- **Direction**: Up / Down / Random

**Use cases:**
- Guitar-like chord textures
- Acoustic simulation
- Rhythmic interest

**Example:**
```
Without strum: C-E-G-B (all at once)
With strum:    C...E...G...B (cascade)
```

**Tips:**
- Slow delay (30-50ms) = slow strum
- Fast delay (5-15ms) = fast strum
- Down direction = high to low notes

---

### 3. Arpeggiator Mode

**Description:** Play chord notes in rhythmic sequence

**Settings:**
- **Pattern**: Up / Down / Up-Down / Down-Up / Random / As-Played
- **Rate**: 1/4, 1/8, 1/16, 1/32 notes
- **Octaves**: 1-4 octave range
- **Gate**: Note length (0.1-1.0, where 1.0 = legato)
- **BPM**: 20-300 (default: 120)

**Use cases:**
- Rhythmic patterns
- Sequencer-style lines
- Moving textures

**Example:**
```
Pattern: Up
Rate: 1/8
Chord: Cmaj7 (C-E-G-B)
Result: C..E..G..B..C..E..G..B.. (repeating)
```

**Tips:**
- Up-Down pattern = smooth motion
- Fast rates (1/16, 1/32) = rapid fire
- Multiple octaves = wider range
- Gate < 1.0 = staccato feel

---

### 4. Slop Mode

**Description:** Human imperfections (timing & velocity variation)

**Settings:**
- **Timing Variation**: 0-50ms (default: 10ms)
- **Velocity Variation**: 0-30% (default: 10%)
- **Pitch Detune**: 0-50 cents (experimental)

**Use cases:**
- Organic, human feel
- Loose, sloppy playing
- Vintage vibe

**Example:**
```
Perfect:    C-E-G (all exactly on time, velocity 100)
With slop:  C-E--G (slightly off time, velocities 95, 105, 92)
```

**Tips:**
- Subtle slop (5-10ms) = natural
- Heavy slop (20-30ms) = drunk piano
- Combine with strum for ultra-loose feel

---

### 5. Pattern Mode

**Description:** Rhythmic patterns (8 built-in patterns)

**Patterns:**
1. **Basic** - Simple quarter note pattern
2. **Bounce** - Alternating root and upper notes
3. **Latin** - Syncopated Latin rhythm
4. **Reggae** - Off-beat emphasis
5. **Waltz** - 3/4 time feel
6. **Broken** - Broken chord pattern
7. **Arpeggio** - Flowing arpeggio
8. **Bossa** - Bossa nova rhythm

**Settings:**
- **BPM**: 40-240 (default: 120)
- **Pattern**: Select from 8 patterns

**Use cases:**
- Rhythmic accompaniment
- Genre-specific patterns
- Automatic grooves

**Example:**
```
Pattern: Reggae
Result: ..X...X...X...X (off-beats emphasized)
```

**Tips:**
- Match BPM to your DAW/track
- Reggae pattern = classic skank
- Bossa pattern = smooth jazz
- Experiment with different chord types

---

### 6. Harp Mode

**Description:** Glissando sweeps like harp

**Settings:**
- **Sweep Time**: 50-500ms (default: 100ms)
- **Direction**: Up / Down
- **Velocity Decay**: Enable/Disable
- **Note Length**: 100-2000ms (how long notes ring)

**Use cases:**
- Harp glissandos
- Dramatic transitions
- Intro/outro flourishes

**Example:**
```
Direction: Up
Sweep: 100ms
Chord: Cmaj9 (C-E-G-B-D)
Result: C.E.G.B.D (sweep over 100ms, all ring together)
```

**Tips:**
- Slow sweep = dramatic
- Fast sweep = quick flourish
- Velocity decay = natural harp sound
- Try on chord changes

---

## Voice-Leading

Orchid-Pi includes intelligent voice-leading inspired by Orchid's patent-pending system.

### What is Voice-Leading?

Voice-leading minimizes finger/voice movement between chords:

**Without voice-leading:**
```
Cmaj → Fmaj
C-E-G → F-A-C  (all notes jump)
```

**With voice-leading:**
```
Cmaj → Fmaj
C-E-G → C-F-A  (smoother, only 2 notes move)
```

### How It Works

1. Analyzes previous chord
2. Finds smoothest voicing for new chord
3. Minimizes total semitone movement
4. Results in professional-sounding progressions

### When To Use

- **Enable**: Jazz, ballads, smooth progressions
- **Disable**: Electronic music, parallel motion wanted

---

## Chord Inversions

### What Are Inversions?

Different ways to voice the same chord:

**Cmaj (C-E-G):**
- Root position: C-E-G
- 1st inversion: E-G-C
- 2nd inversion: G-C-E

### Manual Inversions

Currently automatic via voice-leading.

Future update will add manual inversion control.

---

## MIDI Routing

### Understanding Channels

Orchid-Pi sends MIDI on 3 channels simultaneously:

#### Channel 1: Chords
- **Content**: Full chord notes (2-7 notes)
- **Route to**: Main synthesizer, pad sounds, chords
- **Example**: Cmaj7 = C, E, G, B

#### Channel 2: Bass
- **Content**: Root note, 1 octave down
- **Route to**: Bass synthesizer, sub bass
- **Example**: Cmaj7 bass = C (one octave low)
- **Toggle**: Can be disabled

#### Channel 3: Performance
- **Content**: Performance mode output
- **Route to**: Secondary synth, effects
- **Used by**: Strum, Arp, Slop, Pattern, Harp modes

### Routing Examples

**Example 1: Full Band**
```
Ch 1 → Electric Piano (chords)
Ch 2 → Bass Synth (bass)
Ch 3 → Not used (Direct mode)
```

**Example 2: Arpeggiated Texture**
```
Ch 1 → Pad Synth (held chord)
Ch 2 → Bass Synth (bass)
Ch 3 → Pluck Synth (arpeggiated notes)
```

**Example 3: Renoise DAW**
```
Ch 1 → Track 1 (chords instrument)
Ch 2 → Track 2 (bass instrument)
Ch 3 → Track 3 (performance instrument)
```

---

## Tips & Tricks

### Creating Smooth Progressions

1. Enable voice-leading
2. Use maj7 or min7 chords
3. Move by 4ths/5ths
4. Result: Pro-sounding jazz progressions

### Rhythmic Interest

1. Select Pattern or Arp mode
2. Match BPM to your track
3. Play simple chords
4. Result: Automatic groove

### Humanization

1. Enable Slop mode
2. Set timing variation to 10-15ms
3. Set velocity variation to 10-15%
4. Result: Less robotic, more human

### Bass Lines

1. Enable Bass toggle
2. Route Ch 2 to bass synth
3. Play chords on Ch 1
4. Result: Instant bass + chords

### Harp Sweeps on Chord Changes

1. Enable Harp mode
2. Set sweep time to 100-200ms
3. Play chord progression
4. Result: Dramatic glissandos

---

## Presets (Future Feature)

Coming in v1.1:
- Save favorite settings
- Recall instantly
- Share with community

---

## Renoise Integration

Orchid-Pi is compatible with your existing Renoise script!

### Setup

1. **In Renoise**: Keep your com.renoise.no3zchanger.xrnx active
2. **In Orchid-Pi**: MIDI output goes to Renoise input
3. **Result**: Orchid-Pi sends position sync to Renoise

### Workflow

1. Create pattern in Renoise
2. Orchid-Pi sends song position
3. Renoise stays in sync
4. Both tools work together

---

## Keyboard Shortcuts (Future Feature)

Coming soon:
- Space: Play/Stop
- Number keys: Change chord type
- Arrow keys: Octave/voicing
- Esc: Settings

---

## Troubleshooting

### Chords sound wrong

- Check chord type setting
- Verify MIDI channel on synth
- Try different voicing

### Arpeggiator not in time

- Match BPM to your DAW/track
- Check MIDI clock sync
- Verify performance mode is active

### Bass too high/low

- Adjust bass_octaves_down in config
- Default is 1 octave down
- Can set 1-3 octaves

### Performance mode not working

- Verify mode is selected (button highlighted)
- Check Channel 3 is routed correctly
- Try different mode

---

## Next Steps

- Explore all performance modes
- Try different chord types
- Route MIDI to your favorite synths
- Create music!

---

## Support

Questions? Issues?
- GitHub: https://github.com/yourusername/orchid-pi
- Email: no3productionz@gmail.com
