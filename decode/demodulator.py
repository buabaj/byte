import scipy.signal as signal
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile


freq_carrier = 2000
freq_bitrate = 50
signal_amplitude = 1
sampling_freq = 10000
freq_deviation = 500


def record_audio():
    '''
    records audio
    '''
    print("Recording...")
    recording = sd.rec(int(10 * sampling_freq), samplerate=sampling_freq,
                       channels=1, blocking=True)
    sd.wait()
    print("Recording complete")
    write("recording.wav", sampling_freq, recording)
    print("Recording saved as recording.wav")


def decode_non_return_to_zero(data):
    '''
    converts non-return-to-zero to binary
    '''
    data = ""
    prev = 1
    while (len(data)):
        curr = data[:1]
        data = data[1:]
        if curr != prev:
            data += "1"
        else:
            data += "0"
        prev = curr
    return data


def decode_data(data):
    '''
    converts binary to characters
    '''
    data = decode_non_return_to_zero(data)
    count = 0
    base = ""
    while (count < len(data)):
        base += '0'
        base += data[count:count+7]
        base += ' '
        count += 8
    ascii_sting_base = ""
    bin = base.split()
    for i in bin:
        int_val = int(i, 2)
        ascii_char = chr(int_val)
        ascii_sting_base += ascii_char
    return ascii_sting_base


def demodulator():
    sample_rate, data = wavfile.read("recording.wav")
    raw_data = data
    raw_data_diff = np.diff(raw_data, 1)
    raw_data_envelope = np.abs(signal.hilbert(raw_data_diff))
    sig = signal.firwin(numtaps=100, cutoff=freq_bitrate *
                        2, fs=sampling_freq)
    raw_data_filtered = signal.lfilter(sig, 1.0, raw_data_envelope)

    mean = np.mean(raw_data_filtered)
    sig_data = ""
    sampled_signal = raw_data_filtered[int(
        sampling_freq/freq_bitrate/2):len(raw_data_filtered):int(sampling_freq/freq_bitrate)]

    for bit in sampled_signal:
        if bit > mean:
            sig_data += "0"
        else:
            sig_data += "1"

    itr_1 = 0
    itr_2 = 0
    len_sig_data = len(sig_data)

    bin = ""

    app_str_data = "10101010101010101010"

    sig_list = []
    flag = 0
    for i in range(1, len_sig_data-20):
        x = sig_data[i:i+20]
        if x == app_str_data:
            itr_1 = i + 20
            flag = 1
            sig_list.append(x)
        else:
            if flag == 0:
                continue
    for i in range(0, len(sig_list)):
        if sig_list[i+1] - sig_list[i] != 2:
            continue
        else:
            itr_1 = sig_list[i]
            break
    added_str = "10101010101010101010"
    for i in reversed(range(len_sig_data)):
        x = sig_data[i-19:i+1]
        if x == added_str:
            itr_2 = i-19
            break
    bin = sig_data[itr_1:itr_2]

    data = decode_data(bin)
    if data == "":
        print("Message could not be decoded successfully. Please try again")
    else:
        print("Message decoded successfully: ", data)
    return data


record_audio()
demodulator()
