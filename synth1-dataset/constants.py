NOTE_DURATION = 3
WAV_FOLDER = "wavs"

SOUND_DEVICE_NAME = "Stereo Mix (Realtek(R) Audio)"
SOUND_DEVICE_HOSTAPI = 0

DEFAULT_VALUES = {
    51: 74,
    67: 0,
    68: 0,
    69: 0,
    70: 0,
    71: 0,
    72: 64,
    73: 0,
    74: 0,
    75: 70,
    76: 0,
    77: 0,
    78: 0,
    79: 64,
    80: 64,
    81: 64,
    82: 0,
    83: 66,
    84: 64,
    85: 24,
    86: 45057,
    87: 44,
    88: 45057,
    89: 43,
    90: 64,
    91: 0,
    92: 0,
    93: 2,
    94: 16,
    95: 0,
    96: 1,
    97: 1,
    98: 64,
}

META_COLS = [
    "name",
    "ver",
    "color",
    "bankname",
]

PARAMETER_NAMES = {
    0: "Osc1 Shape",
    1: "Osc2 Shape",
    2: "Osc2 Pitch",
    3: "Osc2 Fine Tune",
    4: "Osc2 KDB Track",
    5: "Osc Mix",
    6: "Osc2 Sync",
    7: "Osc2 Ring modulation",
    8: "Osc2 Pulse Width",
    9: "Osc Key Shift",
    10: "Osc Mod Env On/Off",
    11: "Osc Mod Env Amount",
    12: "Osc Mod Env Attack",
    13: "Osc Mod Env Decay",
    14: "Filter Type",
    15: "Filter Attack",
    16: "Filter Decay",
    17: "Filter Sustain",
    18: "Filter Release",
    19: "Filter Freq",
    20: "Filter Resonance",
    21: "Filter Amount",
    22: "Filter Kdb Track",
    23: "Filter Saturation",
    24: "Filter Velocity Switch",
    25: "Amp Attack",
    26: "Amp Decay",
    27: "Amp Sustain",
    28: "Amp Release",
    29: "Amp Gain",
    30: "Amp Velocity Sensitivity",
    31: "Arpeggiator type",
    32: "Arpeggiator Oct Range",
    33: "Arpeggiator Beat",
    34: "Arpeggiator Gate",
    35: "Delay Time",
    36: "Delay Feedback",
    37: "Delay Dry/Wet",
    38: "Play Mode Type",
    39: "Portament Time",
    40: "Pitch Bend Range",
    41: "Lfo1 Destination",
    42: "LFO1 Type",
    43: "LFO1 Speed",
    44: "LFO1 Depth",
    45: "Osc1 FM",
    46: "Lfo2 Destination",
    47: "Lfo2 Type",
    48: "Lfo2 Speed",
    49: "Lfo2 Depth",
    50: "Midi Ctrl Sens1",
    51: "Midi Ctrl Sens2",
    52: "Chorus Delay Time",
    53: "Chorus Depth",
    54: "Chorus Rate",
    55: "Chorus Feedback",
    56: "Chorus Level",
    57: "Lfo1 On/Off",
    58: "Lfo2 On/Off",
    59: "Arpeggiator On/Off",
    60: "Eq Tone",
    61: "Eq Freq",
    62: "Eq Level",
    63: "Eq Q",
    64: "Chorus Type",
    65: "Delay On/Off",
    66: "Chorus On/Off",
    67: "Lfo1 Tempo Sync",
    68: "Lfo1 Key Sync",
    69: "Lfo2 Tempo Sync",
    70: "Lfo2 Key Sync",
    71: "Osc Mod Dest",
    72: "Osc1,2 Fine Tune",
    73: "Unison Mode",
    74: "Portament Auto Mode",
    75: "Unison Detune",
    76: "Osc1 Detune",
    77: "Effect On/Off",
    78: "Effect Type",
    79: "Effect Control1",
    80: "Effect Control2",
    81: "Effect Level/Mix",
    82: "Delay Type",
    83: "Delay Time Spread",
    84: "Unison Pan Spread",
    85: "Unison Pitch",
    86: "Midi Ctrl Src1",
    87: "Midi Ctrl Assign1",
    88: "Midi Ctrl Src2",
    89: "Midi Ctrl Assign2",
    90: "Pan",
    91: "Osc Phase Shift",
    92: "Unison Phase Shift",
    93: "Unison Voice Num",
    94: "Polyphonic",
    95: "Osc1 Sub Gain",
    96: "Osc1 Sub Shape",
    97: "Osc1 Sub Octave",
    98: "Delay Tone",
}


SKIPPED_PARAMETERS = [
    "86",
    "87",
    "88",
    "89",
    "50",
    "51",
    "94",
] + META_COLS
