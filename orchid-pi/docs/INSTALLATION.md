# Orchid-Pi Installation Guide

Complete installation instructions for Raspberry Pi 3/4.

---

## Table of Contents

1. [Hardware Setup](#hardware-setup)
2. [OS Installation](#os-installation)
3. [Software Installation](#software-installation)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## Hardware Setup

### Required Components

1. **Raspberry Pi 3 Model B/B+** (or Raspberry Pi 4)
2. **microSD card** - 16GB minimum, 32GB recommended (Class 10)
3. **Power supply** - 5V 2.5A for Pi 3, 5V 3A for Pi 4
4. **HDMI touchscreen** - 5" or 7" (800x480 or 1024x600 recommended)
5. **USB MIDI interface** - Any class-compliant USB MIDI interface
6. **Optional**: USB MIDI keyboard for input

### Assembly

1. **Insert microSD card** into Raspberry Pi
2. **Connect touchscreen**:
   - Connect HDMI cable
   - Connect USB cable for touch input (if required)
   - Some displays use GPIO pins for touch
3. **Connect USB MIDI interface**
4. **Connect power** (do this last)

---

## OS Installation

### Option 1: Raspberry Pi Imager (Recommended)

1. **Download Raspberry Pi Imager**:
   - Visit: https://www.raspberrypi.com/software/
   - Install for your OS

2. **Flash OS to microSD**:
   ```
   - Insert microSD card into computer
   - Open Raspberry Pi Imager
   - Choose OS: Raspberry Pi OS (32-bit) with Desktop
   - Choose Storage: Your microSD card
   - Click Write
   ```

3. **Boot Raspberry Pi**:
   - Insert microSD into Pi
   - Connect peripherals
   - Power on

4. **Complete setup wizard**:
   - Set country, language, timezone
   - Set password
   - Connect to WiFi (optional)
   - Update software

### Option 2: Manual Installation

1. Download Raspberry Pi OS:
   ```bash
   https://www.raspberrypi.com/software/operating-systems/
   ```

2. Flash to microSD using dd or Etcher

3. Boot and configure manually

---

## Software Installation

### Automated Installation (Recommended)

```bash
# 1. Clone repository
cd ~
git clone https://github.com/yourusername/orchid-pi.git
cd orchid-pi

# 2. Run installation script
chmod +x scripts/install.sh
./scripts/install.sh

# 3. Follow prompts
# - System will update packages
# - Install dependencies
# - Install Python packages
# - Setup desktop shortcuts
# - (Optional) Enable auto-start
```

### Manual Installation

```bash
# 1. Update system
sudo apt-get update
sudo apt-get upgrade -y

# 2. Install system dependencies
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    libasound2-dev \
    libjack-dev \
    libportmidi-dev \
    python3-kivy \
    libmtdev1 \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    git

# 3. Install Python packages
pip3 install --user python-rtmidi mido kivy

# 4. Clone repository
cd ~
git clone https://github.com/yourusername/orchid-pi.git
cd orchid-pi

# 5. Make scripts executable
chmod +x scripts/*.sh
chmod +x src/main.py
```

---

## Configuration

### Touchscreen Calibration

If touchscreen is not accurate:

```bash
# Install calibration tool
sudo apt-get install xinput-calibrator

# Run calibration
xinput_calibrator

# Follow on-screen instructions
# Save configuration when complete
```

### MIDI Device Setup

```bash
# Check connected MIDI devices
python3 src/main.py --list-midi

# Output will show:
# Available MIDI Input Ports:
#   0: USB MIDI Interface
# Available MIDI Output Ports:
#   0: USB MIDI Interface
```

### Auto-start Configuration

To start Orchid-Pi on boot:

```bash
# Create autostart entry
mkdir -p ~/.config/autostart
nano ~/.config/autostart/orchid-pi.desktop
```

Add:
```ini
[Desktop Entry]
Type=Application
Name=Orchid-Pi MIDI Brain
Exec=/home/pi/orchid-pi/scripts/start_orchid.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

Save and exit (Ctrl+X, Y, Enter)

### Display Rotation

If touchscreen is upside-down:

```bash
# Edit boot config
sudo nano /boot/config.txt

# Add at end:
display_rotate=2

# Save and reboot
sudo reboot
```

Values:
- 0 = normal
- 1 = 90 degrees
- 2 = 180 degrees
- 3 = 270 degrees

---

## Testing

### Test MIDI

```bash
# List MIDI devices
python3 src/main.py --list-midi

# Should show your USB MIDI interface
```

### Test GUI

```bash
# Start Orchid-Pi
cd ~/orchid-pi
python3 src/main.py

# GUI should appear on touchscreen
# Try touching virtual keyboard
```

### Test MIDI Output

1. Connect MIDI cable from Orchid-Pi output to synthesizer
2. Start Orchid-Pi
3. Touch virtual keyboard or play MIDI keyboard
4. Synthesizer should play chords

---

## Performance Optimization

### Disable Unnecessary Services

```bash
# Disable Bluetooth (if not needed)
sudo systemctl disable bluetooth
sudo systemctl stop bluetooth

# Disable WiFi (if using ethernet)
sudo systemctl disable wpa_supplicant
sudo systemctl stop wpa_supplicant
```

### CPU Governor

Set CPU to performance mode:

```bash
# Install cpufrequtils
sudo apt-get install cpufrequtils

# Set to performance
sudo cpufreq-set -g performance

# Make permanent
echo "GOVERNOR=\"performance\"" | sudo tee /etc/default/cpufrequtils
```

### Disable Screen Blanking

```bash
# Edit lightdm config
sudo nano /etc/lightdm/lightdm.conf

# In [Seat:*] section, add:
xserver-command=X -s 0 -dpms

# Save and reboot
```

---

## Troubleshooting

### Orchid-Pi won't start

```bash
# Check Python installation
python3 --version
# Should be 3.7 or higher

# Check dependencies
pip3 list | grep rtmidi
pip3 list | grep kivy

# Reinstall if missing
pip3 install --user python-rtmidi kivy
```

### No MIDI devices detected

```bash
# Check USB MIDI is connected
lsusb
# Should show MIDI interface

# Check ALSA sees it
aconnect -l

# Reload ALSA
sudo alsa force-reload
```

### Touchscreen not working

```bash
# Check USB touch device
lsusb
# Should show touchscreen controller

# Check input devices
ls -l /dev/input/
# Should show event* devices

# Test touch events
sudo evtest
# Select touchscreen device
# Touch screen - should show events
```

### GUI is slow

```bash
# Use lighter window manager
sudo apt-get install openbox
# Set as default in raspi-config

# Reduce GUI resolution in config
# Edit config/orchid_settings.json
{
  "gui": {
    "window_width": 640,
    "window_height": 480
  }
}
```

### Audio crackling (if using FluidSynth later)

```bash
# Increase audio buffer
# Edit /boot/config.txt
audio_pwm_mode=2

# Or use USB audio interface instead
```

---

## Updating

```bash
# Update Orchid-Pi
cd ~/orchid-pi
git pull

# Update dependencies
pip3 install --user --upgrade python-rtmidi mido kivy
```

---

## Uninstalling

```bash
# Remove Orchid-Pi
rm -rf ~/orchid-pi

# Remove autostart
rm ~/.config/autostart/orchid-pi.desktop
rm ~/Desktop/orchid-pi.desktop

# Remove Python packages (optional)
pip3 uninstall python-rtmidi mido kivy
```

---

## Support

If you encounter issues:

1. Check this troubleshooting guide
2. Search GitHub issues
3. Create new issue with:
   - Raspberry Pi model
   - OS version (`cat /etc/os-release`)
   - Error messages
   - Steps to reproduce

---

## Next Steps

- Read [USER_GUIDE.md](USER_GUIDE.md) for usage instructions
- Check [MIDI_SPEC.md](MIDI_SPEC.md) for MIDI implementation details
- Join community discussions on GitHub
