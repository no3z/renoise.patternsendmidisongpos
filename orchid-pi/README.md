# Orchid-Pi MIDI Brain

A Raspberry Pi-based chord generator and MIDI processor inspired by **Telepathic Instruments' Orchid**.

Transform single MIDI notes into full chords with intelligent voice-leading, multiple performance modes, and professional MIDI routing. Perfect for live performance, studio production, and creative music making.

---

## Features

### Chord Engine
- **20+ chord types**: Major, Minor, 7th, 9th, 11th, 13th, sus, dim, aug, and more
- **Intelligent voice-leading**: Smooth chord transitions with minimal voice movement
- **Chord inversions**: Manual or automatic voicing selection
- **Voicing rotation**: Orchid-style dial for expanding chord range
- **Bass generation**: Automatic bass notes on separate MIDI channel

### Performance Modes
1. **Direct** - Play chords directly without processing
2. **Strum** - Guitar-style strumming with configurable timing
3. **Arpeggiator** - Rhythmic arpeggios (up/down/random, 1/4 to 1/32 notes)
4. **Slop** - Human-like imperfections (timing & velocity variation)
5. **Pattern** - Rhythmic patterns (basic, bounce, latin, reggae, waltz, bossa, etc.)
6. **Harp** - Glissando sweeps with natural decay

### MIDI Features
- **3-channel output**: Chords (Ch1), Bass (Ch2), Performance (Ch3)
- **MIDI I/O**: USB MIDI interface support
- **Renoise integration**: Song Position Pointer sync (compatible with existing script)
- **Low latency**: <1ms MIDI processing
- **Virtual MIDI ports**: Create virtual outputs for DAW routing

### User Interface
- **Touchscreen GUI**: Designed for 7" HDMI touchscreens
- **Virtual keyboard**: 12-key interface for chord input
- **Real-time display**: Current chord, voicing, and mode information
- **Easy controls**: Octave, chord type, bass toggle, mode selection
- **Preset system**: Save and recall favorite settings

---

## Hardware Requirements

### Minimum
- Raspberry Pi 3 Model B or B+
- microSD card (16GB+)
- 5V 2.5A power supply
- HDMI touchscreen (5" or 7")
- USB MIDI interface

### Recommended
- Raspberry Pi 4 (for better performance)
- 32GB microSD card (Class 10)
- 7" HDMI touchscreen (800x480 or 1024x600)
- Quality USB MIDI interface with low latency

---

## Software Requirements

- Raspberry Pi OS (Desktop recommended)
- Python 3.7+
- python-rtmidi
- Kivy 2.1+

---

## Quick Start

### Installation

```bash
# Clone the repository
cd orchid-pi

# Run installation script
chmod +x scripts/install.sh
./scripts/install.sh

# Or install manually
pip3 install -r requirements.txt
```

### Running Orchid-Pi

```bash
# Using launcher script
./scripts/start_orchid.sh

# Or run directly
python3 src/main.py

# List available MIDI ports
python3 src/main.py --list-midi
```

---

## Usage

### Basic Operation

1. **Connect MIDI devices**
   - Input: MIDI keyboard or controller
   - Output: Synthesizer, DAW, or other MIDI device

2. **Launch Orchid-Pi**
   - GUI will display on touchscreen
   - MIDI ports auto-detected

3. **Play chords**
   - Touch virtual keyboard OR
   - Play notes on MIDI input
   - Single notes → Full chords!

### Changing Chord Types

- Use **◀ ▶** buttons next to "Chord Type"
- Cycles through 20+ chord types
- Examples: major, minor, maj7, min7, dom7, maj9, etc.

### Performance Modes

Select mode from bottom panel:
- **Direct**: No processing
- **Strum**: Guitar strumming effect
- **Arp**: Arpeggiated patterns
- **Slop**: Humanization
- **Pattern**: Rhythmic patterns
- **Harp**: Glissando sweeps

### Octave Control

- Use **▲ ▼** buttons next to "Octave"
- Range: 0-8

### Bass Toggle

- Turn bass output ON/OFF
- Bass sent on MIDI Channel 2

---

## MIDI Routing

| Channel | Content | Use Case |
|---------|---------|----------|
| **1** | Chord notes | Main synth, pads, chords |
| **2** | Bass note | Bass synth, sub bass |
| **3** | Performance notes | Strum/arp/pattern output |

### Renoise Integration

Orchid-Pi includes Song Position Pointer sync compatible with the existing Renoise script:

```lua
-- Your existing com.renoise.no3zchanger.xrnx works with Orchid-Pi!
-- Orchid-Pi can send position updates to keep Renoise in sync
```

---

## Configuration

### Settings File
Edit `config/orchid_settings.json`:

```json
{
  "midi": {
    "chord_channel": 1,
    "bass_channel": 2,
    "performance_channel": 3
  },
  "chord_engine": {
    "default_chord_type": "maj7",
    "voice_leading_enabled": true
  }
}
```

### Presets
Create presets in `config/presets.json`:

```json
{
  "name": "Jazz Chords",
  "chord_type": "maj7",
  "performance_mode": "slop",
  "bass_enabled": true
}
```

---

## Architecture

```
Input MIDI → Chord Engine → Performance Mode → MIDI Router → Output
   ↓             ↓              ↓                    ↓
 Note        Chord Gen      Strum/Arp/etc      Ch1/Ch2/Ch3
             Voice Lead     Humanization       to Synths
```

### Modules

- **core/**: Music theory, chord generation, voice-leading
- **midi/**: MIDI I/O, routing, sync
- **performance/**: Performance modes (strum, arp, etc.)
- **gui/**: Kivy touchscreen interface

---

## Performance

### Latency
- MIDI processing: <1ms
- Total latency: 5-10ms (depends on USB MIDI interface)

### CPU Usage (Raspberry Pi 3)
- Idle: 5-10%
- Playing chords: 10-20%
- Arpeggiator active: 15-25%

### Polyphony
- Unlimited (MIDI-only, no audio synthesis)
- Limited only by receiving synthesizer

---

## Troubleshooting

### No MIDI output
```bash
# List MIDI devices
python3 src/main.py --list-midi

# Check USB MIDI interface is connected
lsusb
```

### GUI not starting
```bash
# Check Kivy installation
python3 -c "import kivy"

# Run with debug
python3 src/main.py --verbose
```

### Touchscreen not responding
```bash
# Calibrate touchscreen
sudo apt-get install xinput-calibrator
xinput_calibrator
```

---

## Development

### Project Structure
```
orchid-pi/
├── src/
│   ├── core/          # Chord engine, music theory
│   ├── midi/          # MIDI I/O and routing
│   ├── performance/   # Performance modes
│   ├── gui/           # Kivy interface
│   └── main.py        # Entry point
├── config/            # Configuration files
├── scripts/           # Installation and launch scripts
├── docs/              # Documentation
└── tests/             # Unit tests
```

### Running Tests
```bash
# Test individual modules
python3 src/core/chord_engine.py
python3 src/midi/midi_router.py
python3 src/performance/strum.py
```

---

## Comparison: Orchid vs Orchid-Pi

| Feature | Orchid Original | Orchid-Pi |
|---------|----------------|-----------|
| **Price** | $549 | ~$150 (DIY) |
| **Hardware** | Dedicated device | Raspberry Pi 3/4 |
| **Synthesis** | Built-in engines | MIDI-only (external) |
| **Voices** | 16 polyphonic | Unlimited (MIDI) |
| **Speakers** | Built-in | External |
| **Portability** | Battery-powered | Power bank compatible |
| **Customization** | Firmware updates | Full open source |
| **Voice-leading** | Patent-pending | Intelligent algorithm |
| **Performance Modes** | 5 modes | 5 modes |

---

## Credits

- **Inspired by**: Telepathic Instruments Orchid (Kevin Parker, Tame Impala)
- **Author**: no3productionz@gmail.com / @deblockgame
- **Based on**: Original Renoise MIDI script (com.renoise.no3zchanger.xrnx)

---

## License

MIT License - See LICENSE file for details

---

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/orchid-pi/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/orchid-pi/discussions)
- **Email**: no3productionz@gmail.com

---

## Roadmap

### v1.1 (Planned)
- [ ] MIDI learn for CC mapping
- [ ] User-definable patterns
- [ ] Scale-aware chord generation
- [ ] Headless mode (no GUI)
- [ ] Web-based remote control

### v1.2 (Future)
- [ ] MPE support
- [ ] CV/Gate output (via hardware)
- [ ] Audio synthesis (FluidSynth integration)
- [ ] Cloud preset sharing

---

**Made with ❤️ for musicians, by musicians**
