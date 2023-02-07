import time
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write


freq_carrier = 2000
freq_bitrate = 100
signal_amplitude = 1
sampling_freq = 10000
freq_deviation = 1000


def non_return_to_zero(data):
    '''
    converts binary to non-return-to-zero
    '''
    data = ""
    prev = 1
    while (len(data)):
        curr = data[:1]
        data = data[1:]
        if curr == "1":
            prev = (prev + 1) % 2
        data += str(prev)
    return data


def encode_data(message):
    '''
    converts characters to binary
    '''
    data = ' '.join(format(ord(i) if isinstance(i, str) else i, 'b')
                    for i in message)
    data = non_return_to_zero(data)
    data = "0000000011111111" + data + "0000000011111111"
    return data


def generate_waveform(data):
    '''
    generates waveform
    '''
    bin = " ".join(data)
    fmt = np.fromstring(bin, dtype=int, sep=' ')
    input_data = fmt
    n = len(input_data)  # length of the input signal
    # implement voltage control oscillator function generator for frequency synthesis
    top = np.arange(0, float(n)/float(freq_bitrate),
                    1/float(sampling_freq), dtype=float)
    mid = np.zeros(0).astype(float)

    for bit in input_data:
        if bit == 0:
            mid = np.hstack((mid, np.multiply(
                np.ones(int(sampling_freq/freq_bitrate)), freq_carrier + freq_deviation)))
        else:
            mid = np.hstack((mid, np.multiply(
                np.ones(int(sampling_freq/freq_bitrate)), freq_carrier - freq_deviation)))

    amp_val = np.zeros(0)
    amp_val = signal_amplitude * np.cos(2 * np.pi * np.multiply(mid, top))

    wav = np.int16(amp_val * 32767)
    write('encoded_audio.wav', sampling_freq, wav)
    return wav


def get_data():
    '''
    gets data from user
    '''
    message = input("Enter message to be encoded: ")
    if message == "":
        print("No message entered. Please try again.")
        time.sleep(2)
        get_data()
    else:
        data = encode_data(message)
        byte = generate_waveform(data)
        sd.play(byte, sampling_freq)
        time.sleep(10)
        print("Message successfully encoded to: encoded_audio.wav")


get_data()
