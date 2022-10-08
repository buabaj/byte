import wave
import numpy as np
from encryption_engine import decrypt


def decode_data(audio_file_path: str) -> str:
    """Decodes a message from an audio file

    Args:
        audio_file_path (str): Path to the audio file

    Returns:
        str: Decoded message
    """
    audio_file = wave.open(audio_file_path, "rb")
    frame_bytes = bytearray(
        list(audio_file.readframes(audio_file.getnframes())))

    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]

    string = "".join(chr(int("".join(
        map(str, extracted[i:i+100])), 2)) for i in range(0, len(extracted), 100))

    decoded_data = str(decrypt(string)).split("###")[0]
    audio_file.close()

    return print(decoded_data)


decode_data("data/encoded_audio.wav")
