import math
import threading
import time
import wave
from pathlib import Path
from typing import Dict, List

import mido
import pandas as pd
import pyaudio
from tqdm import trange

from .constants import NOTE_DURATION, SKIPPED_PARAMETERS, WAV_FOLDER

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100


def find_device(p):
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev["name"] == "Stereo Mix (Realtek(R) Audio)" and dev["hostApi"] == 0:
            dev_index = dev["index"]
            return dev_index


def save_to_wav(frames: List, filename: str):
    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()


def play_note(outport):
    """Plays one midi note for a specific number of seconds"""
    time.sleep(0.2)
    msg = mido.Message("note_on", note=60)
    outport.send(msg)
    time.sleep(NOTE_DURATION)
    msg = mido.Message("note_off", note=60)
    outport.send(msg)


def get_cc(x):
    """Gets the CC that corresponds to a parameter number"""
    # CC 7 somehow stops all sound, might be specific to my setup
    # Has been remapped to 120
    if x == "7":
        return 120
    return int(x)


def get_midi_value(code, value):
    """Fixes some bad values that are read from the banks"""
    if code in ["1", "31", "64", "41", "46"] and value != 0:
        return int(value) - 1
    if code == "9":
        return int(value) + 24
    if code == "93":
        return int(value) - 2
    if code in ["2", "21"] and int(value) > 127:
        return 127
    return int(value)


def send_params(params: Dict[str, str], outport):
    """Sends all midi messages in dict[CC,Value]"""
    for p in params:
        if p in SKIPPED_PARAMETERS or math.isnan(float(params[p])):
            continue
        msg = mido.Message(
            "control_change", control=get_cc(p), value=get_midi_value(p, params[p])
        )
        outport.send(msg)


def flush_stream(stream):
    """Flushes audiostream to prevent previous sound from bleeding into the next"""
    for _ in range(40):
        stream.read(CHUNK)


def play_record_note(outport, stream, out_path: str):
    """Sends a midi note and records the audio"""
    t = threading.Thread(target=play_note, args=(outport,))
    t.start()
    frames = []
    record_duration = NOTE_DURATION + 2
    for _ in range(0, int(RATE / CHUNK * record_duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    save_to_wav(frames, out_path)


def collect_wav(
    input_file: Path,
    output_folder: Path,
    midi_port_name="loopMIDI Port 1",
    start: int = 0,
):
    """Generates a sound for all entries in the CSV file"""
    paudio = pyaudio.PyAudio()
    stream = paudio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        input_device_index=find_device(paudio),
        frames_per_buffer=1024,
    )

    df = pd.read_csv(input_file, index_col=False, header=0)
    wav_out = output_folder / WAV_FOLDER
    wav_out.mkdir(exist_ok=True)

    with mido.open_output(midi_port_name) as outport:
        for i in trange(start, len(df), initial=start, total=len(df)):
            try:
                params = df.iloc[i].to_dict()
                send_params(params, outport)
                play_record_note(outport, stream, str(wav_out / f"{i}.wav"))

                # Silence output by setting gain and decay to 0
                # This prevents the sample from ringing for too long
                send_params({26: 0, 27: 0, 28: 0, 29: 0, 65: 0}, outport)
                flush_stream(stream)
                time.sleep(0.05)
            except KeyboardInterrupt:
                print("")
                print("Stopping threads...")
                break

    stream.stop_stream()
    stream.close()
    paudio.terminate()
