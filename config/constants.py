"""HARMONI Robot - Configuration & Constants

This file contains all hardware parameters, thresholds, and mappings.
Edit this file to customize servo positions, MIDI device, and drum patterns.
"""

import math

# ============================================================================
# HARDWARE CONFIGURATION
# ============================================================================

# PCA9685 PWM Driver (I2C)
PCA9685_ADDRESS = 0x40              # Default I2C address
PCA9685_FREQUENCY = 60              # PWM frequency (Hz) for servo control

# Servo Motor Specifications (MG966R)
SERVO_MIN_ANGLE = 0                 # Minimum angle (degrees)
SERVO_MAX_ANGLE = 180               # Maximum angle (degrees)
SERVO_HARD_LIMIT_MIN = 10           # Software safety limit (min)
SERVO_HARD_LIMIT_MAX = 95           # Software safety limit (max)

# Servo Positions for Drum Striking
UP_POSITION = 0                     # Resting position (degrees)
DOWN_POSITION = 20                  # Strike position (low amplitude for drum pad sensitivity)
RECOVERY_STEPS = 6                  # Number of interpolation steps for smooth return
RECOVERY_TIME_MS = 100              # Total recovery time (milliseconds)
IMPACT_HOLD_TIME_MS = 50            # Time to hold impact position (milliseconds)

# ============================================================================
# SERVO MAPPING (CRITICAL - CUSTOMIZE BASED ON YOUR DRUM PAD LAYOUT)
# ============================================================================

# Format: "drum_name": [servo_indices]
# servo_indices: List of servo channels (0-7) that control this drum
# Most drums use single servo; some might use dual servos for redundancy

SERVO_MAPPING = {
    # Left side (default config - adjust to your actual drum pad positions)
    "kick":      [0],           # Channel 0 → Bass drum / Kick pad
    "snare":     [1],           # Channel 1 → Snare drum / Snare pad
    "tom_high":  [2],           # Channel 2 → High tom / High tom pad
    "tom_mid":   [3],           # Channel 3 → Mid tom / Mid tom pad
    
    # Right side (default config - adjust to your actual drum pad positions)
    "tom_floor": [4],           # Channel 4 → Floor tom / Floor tom pad
    "crash":     [5],           # Channel 5 → Crash cymbal / Crash pad
    "hihat":     [6],           # Channel 6 → Hi-hat / Hi-hat pad
    "ride":      [7],           # Channel 7 → Ride cymbal / Ride pad
}

# Reverse mapping for quick lookup
DRUM_REVERSE_MAP = {servo: drum for drum, servos in SERVO_MAPPING.items() for servo in servos}

# ============================================================================
# MIDI CONFIGURATION
# ============================================================================

MIDI_DEVICE_NAME = "Digital Piano"  # Change to match your MIDI device name
                                     # Run: python -c "import rtmidi; m = rtmidi.MidiIn(); print(m.get_ports())"
MIDI_CHANNEL = 0                    # MIDI channel (0-15)
MIDI_NOTE_MIN = 36                  # Lowest note to listen (C1)
MIDI_NOTE_MAX = 96                  # Highest note to listen (C7)

# ============================================================================
# RHYTHM ANALYSIS & BPM DETECTION
# ============================================================================

# BPM Thresholds for music style classification
BPM_SLOW = 80                       # Threshold for slow music
BPM_MODERATE = 100                  # Threshold for moderate music
BPM_FAST = 120                      # Threshold for fast music

# Listening window for BPM detection
LISTEN_BAR_COUNT = 4                # Number of bars to listen before starting (4-8 bars)
MIN_NOTES_FOR_ANALYSIS = 8          # Minimum notes needed for tempo calculation

# Pitch range analysis
PITCH_LOW_THRESHOLD = 48            # Middle C (C3) - notes below = low register
PITCH_HIGH_THRESHOLD = 72           # C5 - notes above = high register

# ============================================================================
# DRUM PATTERN GENERATION
# ============================================================================

# Probability of improvisation features
GHOST_NOTE_PROBABILITY = 0.25       # 25% chance to add ghost notes between beats
TIMING_OFFSET_PROBABILITY = 0.40    # 40% chance to apply timing offset

# Timing offset ranges (milliseconds)
TIMING_OFFSET_RANGE_LAID_BACK = (20, 50)      # BPM < 80: delay (relaxed groove)
TIMING_OFFSET_RANGE_PUSHED = (-50, -20)       # BPM > 120: advance (tight groove)
TIMING_OFFSET_RANGE_NORMAL = (-10, 10)        # BPM 80-120: subtle variation

# Ghost note distribution
GHOST_NOTE_KICK_PROB = 0.8         # 80% chance ghost note uses kick
GHOST_NOTE_SNARE_PROB = 0.2        # 20% chance ghost note uses snare

# ============================================================================
# MUSIC STYLE SPECIFIC PATTERNS
# ============================================================================

# Light & Fast: BPM >= 120 + High Pitch
STYLE_LIGHT_FAST = {
    "primary_drums": ["crash", "hihat"],
    "secondary_drums": ["kick", "snare"],
    "crash_frequency": 0.6,         # Crash appears in 60% of patterns
    "hihat_density": 1.0,            # Hi-hat on every beat
    "kick_density": 0.5,             # Kick on 50% of beats
}

# Heavy: BPM <= 80 + Low Pitch
STYLE_HEAVY = {
    "primary_drums": ["kick", "tom_floor"],
    "secondary_drums": ["snare", "tom_mid"],
    "crash_frequency": 0.1,         # Minimal crash
    "hihat_density": 0.3,            # Sparse hi-hat
    "kick_density": 0.8,             # Heavy kick presence
}

# Normal: BPM 81-119 + Mixed Pitch
STYLE_NORMAL = {
    "primary_drums": ["snare", "hihat"],
    "secondary_drums": ["kick", "tom_mid"],
    "crash_frequency": 0.25,        # Crash on 1st beat occasionally
    "hihat_density": 0.8,            # Regular hi-hat
    "kick_density": 0.6,             # Standard kick pattern
}

# Energetic: BPM >= 120 + Low Pitch
STYLE_ENERGETIC = {
    "primary_drums": ["tom_high", "tom_mid", "tom_floor"],
    "secondary_drums": ["kick", "snare"],
    "crash_frequency": 0.2,         # Occasional crash
    "hihat_density": 0.5,            # Less hi-hat, more toms
    "kick_density": 0.7,             # Strong kick presence
}

# Ethereal: BPM <= 80 + High Pitch
STYLE_ETHEREAL = {
    "primary_drums": ["crash", "ride"],
    "secondary_drums": ["hihat"],
    "crash_frequency": 0.4,         # More crash accents
    "hihat_density": 0.2,            # Sparse hi-hat
    "kick_density": 0.1,             # Minimal kick
}

# ============================================================================
# EV3 VISUAL FEEDBACK
# ============================================================================

# Expression states
EXPRESSION_STATES = {
    "idle": 0,                      # Looking around (no music)
    "listening": 1,                 # Thinking (analyzing music)
    "excited": 2,                   # Happy (fast music)
    "smile": 3,                     # Smiling (moderate music)
    "enjoying": 4,                  # Enjoying (slow music)
}

# LED strip mapping (WS2812B with 60 LEDs)
LED_STRIP_LENGTH = 60               # Total number of LEDs
LED_BRIGHTNESS_MAX = 255            # Maximum brightness (0-255)
LED_BRIGHTNESS_MIN = 50             # Minimum brightness when off

# LED color mapping for drum intensity
LED_COLOR_VELOCITY_MIN = (50, 100, 200)    # Blue (soft hit)
LED_COLOR_VELOCITY_MID = (100, 200, 50)    # Green (medium hit)
LED_COLOR_VELOCITY_MAX = (255, 50, 50)     # Red (hard hit)

# LED animation parameters
LED_ANIMATION_DURATION_MS = 200     # Flash duration when drum is hit
LED_ANIMATION_FADE_STEPS = 10       # Smoothness of fade effect

# ============================================================================
# SERIAL COMMUNICATION (Pi ↔ EV3)
# ============================================================================

SERIAL_PORT = "/dev/ttyACM0"       # USB serial port (auto-detect if not found)
SERIAL_BAUDRATE = 115200           # Baud rate
SERIAL_TIMEOUT = 1.0               # Read timeout (seconds)

# Communication protocol
COMMAND_SEPARATOR = "\n"            # Line separator for commands

# Command format: H0-H7 (drum hit), S0-S4 (expression), OFF (emergency stop)
COMMAND_DRUM_HIT = "H{servo}"      # H0, H1, ..., H7
COMMAND_EXPRESSION = "S{state}"    # S0=idle, S1=listening, S2=excited, S3=smile, S4=enjoying
COMMAND_LED_INTENSITY = "L{intensity}"  # L0-L255 (global LED brightness)
COMMAND_EMERGENCY_STOP = "OFF"     # Kill all outputs

# ============================================================================
# SAFETY & SYSTEM PARAMETERS
# ============================================================================

# Watchdog timers
MIDI_TIMEOUT_MS = 3000             # Stop playing if no MIDI for 3 seconds
SOLO_MODE_TIMEOUT_MS = 2000        # Enter solo mode after 2 seconds of silence

# Servo safety
SERVO_MAX_CURRENT_MA = 1000        # Maximum servo current (for monitoring)
SERVO_STALL_DETECTION_ENABLED = True

# System logging
DEBUG_MODE = True                  # Set to False to reduce console output
LOG_LEVEL = "INFO"                 # DEBUG, INFO, WARNING, ERROR

# ============================================================================
# PERFORMANCE TARGETS (for reference)
# ============================================================================

# Target latencies (milliseconds)
TARGET_MIDI_LATENCY = 50           # MIDI → Drum strike
TARGET_SERVO_RESPONSE = 20         # Servo move time (UP → DOWN)
TARGET_BPM_ACCURACY = 0.02         # ±2% tolerance
TARGET_LED_FRAME_RATE = 30         # FPS
TARGET_EXPRESSION_SWITCH = 100     # LCD refresh time

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_music_style(bpm, has_high_notes, has_low_notes):
    """Classify music style based on BPM and pitch distribution.
    
    Args:
        bpm (float): Detected beats per minute
        has_high_notes (bool): True if melody contains high notes
        has_low_notes (bool): True if melody contains low notes
    
    Returns:
        str: Style name (light_fast, heavy, normal, energetic, ethereal)
    """
    if bpm >= BPM_FAST and has_high_notes and not has_low_notes:
        return "light_fast"
    elif bpm <= BPM_SLOW and has_low_notes and not has_high_notes:
        return "heavy"
    elif BPM_SLOW < bpm < BPM_FAST and has_high_notes and has_low_notes:
        return "normal"
    elif bpm >= BPM_FAST and has_low_notes:
        return "energetic"
    elif bpm <= BPM_SLOW and has_high_notes:
        return "ethereal"
    else:
        return "normal"

def get_timing_offset_range(bpm):
    """Get timing offset range based on BPM.
    
    Args:
        bpm (float): Beats per minute
    
    Returns:
        tuple: (min_offset_ms, max_offset_ms)
    """
    if bpm <= BPM_SLOW:
        return TIMING_OFFSET_RANGE_LAID_BACK  # Relaxed groove
    elif bpm >= BPM_FAST:
        return TIMING_OFFSET_RANGE_PUSHED     # Tight groove
    else:
        return TIMING_OFFSET_RANGE_NORMAL     # Subtle variation

def get_style_config(style_name):
    """Get drum pattern config for a given style.
    
    Args:
        style_name (str): Style identifier
    
    Returns:
        dict: Style configuration
    """
    style_map = {
        "light_fast": STYLE_LIGHT_FAST,
        "heavy": STYLE_HEAVY,
        "normal": STYLE_NORMAL,
        "energetic": STYLE_ENERGETIC,
        "ethereal": STYLE_ETHEREAL,
    }
    return style_map.get(style_name, STYLE_NORMAL)
