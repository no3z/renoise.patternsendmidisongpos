#!/bin/bash
# Orchid-Pi Installation Script
# For Raspberry Pi 3 running Raspberry Pi OS

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════╗"
echo "║      Orchid-Pi MIDI Brain - Installation        ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "⚠️  Warning: This script is designed for Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "📦 Updating system packages..."
sudo apt-get update

# Install system dependencies
echo "📦 Installing system dependencies..."
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

echo "📦 Installing Python packages..."
pip3 install --user \
    python-rtmidi \
    mido \
    kivy

# Make scripts executable
echo "🔧 Setting permissions..."
chmod +x "$(dirname "$0")/start_orchid.sh"
chmod +x "$(dirname "$0")/../src/main.py"

# Create desktop shortcut (if running desktop environment)
if [ -n "$DISPLAY" ]; then
    echo "🖥️  Creating desktop shortcut..."
    cat > ~/Desktop/orchid-pi.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Orchid-Pi MIDI Brain
Comment=Chord Generator and MIDI Processor
Exec=$(pwd)/scripts/start_orchid.sh
Icon=audio-midi
Terminal=false
Categories=Audio;Music;
EOF
    chmod +x ~/Desktop/orchid-pi.desktop
fi

# Setup auto-start (optional)
read -p "🚀 Enable auto-start on boot? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p ~/.config/autostart
    cat > ~/.config/autostart/orchid-pi.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Orchid-Pi MIDI Brain
Exec=$(pwd)/scripts/start_orchid.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF
    echo "✓ Auto-start enabled"
fi

# Test MIDI devices
echo ""
echo "🎹 Checking MIDI devices..."
python3 -c "
try:
    import rtmidi
    midi_in = rtmidi.MidiIn()
    midi_out = rtmidi.MidiOut()

    print('MIDI Input ports:')
    for i, port in enumerate(midi_in.get_ports()):
        print(f'  {i}: {port}')

    print('MIDI Output ports:')
    for i, port in enumerate(midi_out.get_ports()):
        print(f'  {i}: {port}')
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║           Installation Complete! ✓               ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "To start Orchid-Pi:"
echo "  ./scripts/start_orchid.sh"
echo ""
echo "Or run directly:"
echo "  python3 src/main.py"
echo ""
echo "For help:"
echo "  python3 src/main.py --help"
echo ""
