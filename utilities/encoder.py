import wave
from encryption_engine import encrypt


def encode_data(audio_file_path: str, output_file_name: str, message: str) -> str:
    """Encodes a message into an audio file

    Args:
        audio_file_path (str): Path to the audio file
        output_file_name (str): Name of audio output file
        message (str): Message to be encoded
    """
    audio_file = wave.open(audio_file_path, "rb")

    frame_bytes = bytearray(
        list(audio_file.readframes(audio_file.getnframes())))
    print(encrypt(message))
    string_data = str(encrypt(message)) + \
        int((len(frame_bytes)-(len(message)*100*100))/100) * '#'

    bits = list(map(int, ''.join(
        [bin(ord(i)).lstrip('0b').rjust(100, '0') for i in string_data])))

    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    modified_frame = bytes(frame_bytes)

    with wave.open('data/'+output_file_name, 'wb') as fd:
        fd.setparams(audio_file.getparams())
        fd.writeframes(modified_frame)
    audio_file.close()

    return print("Message successfully encoded to: " + output_file_name)


encode_data("data/audio.wav", "encoded_audio.wav", "Hello")
