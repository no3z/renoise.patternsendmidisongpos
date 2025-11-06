#!/usr/bin/env python3
"""
Orchid-Pi MIDI Brain
Main entry point

A Raspberry Pi-based MIDI chord generator and processor
inspired by Telepathic Instruments' Orchid

Author: no3productionz@gmail.com
"""

import sys
import os
import argparse

# Add src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import OrchidPiApp


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Orchid-Pi MIDI Brain - Chord Generator & Processor'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run in headless mode (no GUI, MIDI only)'
    )

    parser.add_argument(
        '--list-midi',
        action='store_true',
        help='List available MIDI ports and exit'
    )

    parser.add_argument(
        '--midi-in',
        type=str,
        help='MIDI input port number or name'
    )

    parser.add_argument(
        '--midi-out',
        type=str,
        help='MIDI output port number or name'
    )

    args = parser.parse_args()

    # List MIDI ports
    if args.list_midi:
        from midi import MIDIProcessor

        processor = MIDIProcessor()

        print("Available MIDI Input Ports:")
        for i, port in enumerate(processor.get_available_input_ports()):
            print(f"  {i}: {port}")

        print("\nAvailable MIDI Output Ports:")
        for i, port in enumerate(processor.get_available_output_ports()):
            print(f"  {i}: {port}")

        return 0

    # Run in headless mode
    if args.headless:
        print("Headless mode not yet implemented")
        print("Use GUI mode or wait for future updates")
        return 1

    # Run GUI app
    try:
        app = OrchidPiApp()
        app.run()
        return 0

    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
