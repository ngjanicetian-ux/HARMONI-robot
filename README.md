# 🥁 HARMONI Robot - AI Drum Robot with Real-time MIDI Analysis

## 📋 Project Overview

**HARMONI** is an intelligent drum robot that listens to piano MIDI input and generates real-time drum accompaniment with **dynamic expressions** and **probabilistic improvisation**. The system combines Raspberry Pi 4 (rhythm analysis & servo control) with LEGO EV3 (visual feedback & LED effects).

### Key Features
- 🎹 **Real-time MIDI Input**: Analyzes piano melodies via USB MIDI
- 🥁 **8-Servo Drum System**: Independent control of 8 small servo motors for ultra-fast response
- 🎨 **Dynamic Expressions**: EV3 LCD shows 5 emotional states based on music tempo & pitch
- ✨ **Smart LED Effects**: WS2812B strip intensity correlates with MIDI velocity
- 🎼 **Music Style Recognition**: Detects tempo, pitch range, and adjusts drum patterns accordingly
- 🎲 **Probabilistic Improvisation**:
  - Ghost Notes (25%): Adds unexpected drum hits between beats for groove
  - Timing Offset: Subtle timing variations (laid-back or pushed) for human-like feel

---

## 🏗️ System Architecture

### Hardware
```
Piano (MIDI USB)
    ↓
[Raspberry Pi 4B]
├─ PCA9685 PWM Driver (I2C)
│  └─ 8× MG966R Servo Motors (via 4 dual-servo brackets)
├─ Serial USB
│  └─ [LEGO EV3]
│     ├─ WS2812B LED Strip (60 LEDs)
│     └─ LCD Display (178×128 px)
└─ python-rtmidi (MIDI listener)

[Drum Pads] ← Physical strike targets
```

### Software Architecture
```
Raspberry Pi:
Main Loop
├─ MIDI Listener (Thread 1)
├─ Rhythm Analyzer (Thread 2)
├─ Drum Pattern Generator (Thread 3)
├─ Servo Controller (Thread 4, 8 parallel servo threads)
└─ Serial Communicator (Thread 5)

EV3:
Serial Listener
├─ Expression Renderer (LCD)
└─ LED Controller (WS2812B)
```

---

## 📁 Project Structure

```
harmoni-robot/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── config/
│   └── constants.py                   # Hardware params, thresholds, servo mappings
├── raspberry_pi/
│   ├── main.py                        # Main orchestrator (entry point)
│   ├── midi_listener.py               # MIDI input via python-rtmidi
│   ├── rhythm_analyzer.py             # BPM detection, pitch analysis, style classification
│   ├── drum_pattern_generator.py      # Drum sequence generation + probabilistic improvisation
│   ├── servo_controller.py            # PCA9685 & 8-servo multi-threaded control
│   └── serial_communicator.py         # USB-Serial communication with EV3
├── ev3/
│   ├── expression_generator.py        # Generate pixel data for 5 expressions (178×128)
│   ├── expression_renderer.py         # Display expressions on EV3 LCD
│   ├── led_controller.py              # WS2812B animation & color mapping
│   └── ev3_listener.py                # Listen for commands from Raspberry Pi
└── assets/
    └── expressions/                   # Pre-generated expression numpy arrays
        ├── idle.npy
        ├── listening.npy
        ├── excited.npy
        ├── smile.npy
        └── enjoying.npy
```

---

## 🔧 Hardware Setup

### Raspberry Pi 4 (Main Controller)

#### I2C Configuration for PCA9685
```bash
# Enable I2C
sudo raspi-config
# → Interfacing Options → I2C → Enable

# Set high-speed I2C mode (optional, for lower latency)
sudo nano /boot/config.txt
# Add line: dtparam=i2c_arm_baudrate=400000

# Verify I2C device
i2cdetect -y 1
# Should show PCA9685 at address 0x40
```

#### Servo Motor Connections
- **PCA9685 I2C Pins**: RPi Pin 3 (SDA), Pin 5 (SCL)
- **Servo Power**: 12V from XL4015 DC-DC step-down
- **Servo Signal**: PCA9685 channels 0-7 (8 servos)
- **Servo GND**: Common ground with Pi

**Servo Mapping** (update in `config/constants.py`):
```python
SERVO_MAPPING = {
    # Left side (4 servos)
    "kick":     [0],        # Bass drum
    "snare":    [1],        # Snare drum
    "tom_high": [2],        # High tom
    "tom_mid":  [3],        # Mid tom
    
    # Right side (4 servos) - customize based on your drum pad layout
    "tom_floor": [4],       # Floor tom
    "crash":     [5],       # Crash cymbal
    "hihat":     [6],       # Hi-hat
    "ride":      [7],       # Ride cymbal
}
```

### EV3 (Visual Feedback)

#### USB Serial Configuration
```bash
# On Raspberry Pi
# Check USB device path
ls -la /dev/ttyACM*
# Usually /dev/ttyACM0

# On EV3 (via SSH or ev3dev console)
# Ensure ev3dev is installed with USB serial support
```

#### LED Strip Connection
- **WS2812B Data Pin**: EV3 GPIO (via level converter: 5V → 3.3V)
- **Power**: 5V from separate USB power bank (not EV3 battery)
- **GND**: Common ground

#### LCD Display
- Built-in EV3 LCD (no additional wiring needed)
- Resolution: 178 × 128 pixels

---

## 💾 Installation

### On Raspberry Pi 4

```bash
# 1. Clone repository
git clone https://github.com/ngjanicetian-ux/harmoni-robot.git
cd harmoni-robot

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Generate expression pixel data
cd assets/expressions
python ../../ev3/expression_generator.py
cd ../..

# 4. Configure hardware (edit config/constants.py)
nano config/constants.py
# → Update SERVO_MAPPING based on your drum pad layout
# → Update MIDI_DEVICE_NAME if different

# 5. Run the system
python raspberry_pi/main.py
```

### On EV3 (ev3dev)

```bash
# SSH into EV3
ssh robot@192.168.1.X

# Clone repository
git clone https://github.com/ngjanicetian-ux/harmoni-robot.git
cd harmoni-robot

# Install ev3dev dependencies
pip install -r requirements.txt

# Run EV3 listener
python ev3/ev3_listener.py
```

---

## 🎯 Usage

### Quick Start

1. **Start EV3 listener** (on EV3 device):
   ```bash
   python ev3/ev3_listener.py
   ```

2. **Start main robot controller** (on Raspberry Pi):
   ```bash
   python raspberry_pi/main.py
   ```

3. **Play piano**: Connect MIDI keyboard and start playing
   - System listens for 4-8 bars to detect tempo & style
   - Then joins in with drum accompaniment
   - EV3 displays emotional expressions based on music
   - After 2-3 seconds of silence → Solo mode (robot plays alone)

### Configuration

Edit `config/constants.py` to customize:
- **Servo angles**: `UP_POSITION`, `DOWN_POSITION`, `RECOVERY_STEPS`
- **Timing offsets**: `TIMING_OFFSET_RANGE`, `GHOST_NOTE_PROBABILITY`
- **Music thresholds**: `BPM_FAST`, `BPM_SLOW`, `PITCH_THRESHOLD`
- **Servo mapping**: `SERVO_MAPPING` (crucial for your drum pad layout)

---

## 🎼 Music Analysis & Drum Generation

### Rhythm Detection

The system analyzes:
1. **BPM** (Beats Per Minute): From MIDI timing intervals
2. **Pitch Range**: High notes vs low notes distribution
3. **Velocity**: MIDI note strength (correlates with intensity)
4. **Rest Duration**: Silence between notes

### Music Style Classification

| Condition | Style | Drum Pattern |
|-----------|-------|-------------|
| BPM ≥ 120 + High Pitch | **Light & Fast** | More Crash/Hi-hat, less kick |
| BPM ≤ 80 + Low Pitch | **Heavy** | More kick/floor tom, minimal crash |
| BPM 81-119 + Mixed | **Normal** | Standard snare & hi-hat |
| BPM ≥ 120 + Low Pitch | **Energetic** | Heavy tom usage |
| BPM ≤ 80 + High Pitch | **Ethereal** | Crash accents, sparse hits |

### Improvisation Mechanisms

#### 1. Ghost Notes (25% probability)
- Adds drum hits between main beats (at 1.5, 2.5, etc.)
- Uses **kick drum** or **snare** (80% kick, 20% snare)
- Creates "busy" feeling, mimics live drummer

**Example**:
```
Original:  Kick(1) ─── Snare(2) ─── Rest(3) ─── Rest(4)
With Ghost: Kick(1) ─ GhostKick(1.5) ─ Snare(2) ─ Rest(3) ─ Rest(4)
```

#### 2. Timing Offset (Groove)
- **Laid-back** (BPM < 100): +20 to +50ms delay → relaxed, groovy
- **Pushed** (BPM > 120): -20 to -50ms advance → tight, energetic
- **Normal** (BPM 80-120): ±10ms random variation → subtle human feel

**Implementation**: Each drum hit gets random offset within range

---

## 📊 Performance Targets

- ⏱️ **MIDI Latency**: < 50ms (from piano key to drum strike)
- 🎯 **Servo Response Time**: < 20ms (servo move from UP to DOWN)
- 🔊 **BPM Accuracy**: ±2% (tempo detection stability)
- 💡 **LED Update Rate**: 30 FPS (smooth animations)
- 🎨 **Expression Switch**: < 100ms (EV3 LCD refresh)

---

## 🐛 Troubleshooting

### MIDI Input Not Detected
```bash
# List available MIDI devices
python -c "import rtmidi; m = rtmidi.MidiIn(); print(m.get_ports())"

# Update config/constants.py with correct device name
```

### Servos Not Moving
```bash
# Check I2C communication
i2cdetect -y 1

# Verify PCA9685 power (should have stable 5-6V on pin 16)
# Check servo power supply (12V)
```

### EV3 Not Receiving Commands
```bash
# Check USB connection
lsusb

# Verify serial port
ls -la /dev/ttyACM*

# Test serial communication
python -c "import serial; s = serial.Serial('/dev/ttyACM0', 115200); print(s.is_open)"
```

---

## 📚 References

- [PCA9685 Datasheet](https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf)
- [MG966R Servo Specs](https://www.onsemi.com/)
- [python-rtmidi Documentation](https://python-rtmidi.readthedocs.io/)
- [ev3dev Documentation](https://ev3dev.org/)
- [WS2812B LED Strip Guide](https://github.com/jgarff/rpi_ws281x)

---

## 📝 License

MIT License - Feel free to modify and share!

---

## 👤 Author

**ngjanicetian-ux** - AI Drum Robot Project

---

**Last Updated**: 2026-04-26
