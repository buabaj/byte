import scipy.signal as signal
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from scipy import signal
from matplotlib import pyplot as plot
import librosa.display
from utils.utils import rms,frames_to_samples

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

def demodulator(x):

    amplified = normalize(x)
    filtered = filter_freqs(amplified)
    data = signal_envelope(filtered)

    sig_data = ""
    sampled_signal = data[int(
    sampling_freq/freq_bitrate/2):len(data):int(sampling_freq/freq_bitrate)]
    
    #Finding peaks that can be adjusted to be ones
    peaks,d = signal.find_peaks(sampled_signal,height=0.1,threshold=0)
    for i in peaks:
        sampled_signal[i] = max(sampled_signal)
    ##
    mean = np.mean(sampled_signal)
    for bit in sampled_signal:
        if bit > mean:
            sig_data += "0"
        else:
            sig_data += "1"

    data_bin = find_head_tail(sig_data)
    
#DECODING MESSAGE
    data = decode_data(data_bin)

    if data == "":
        print("Message could not be decoded successfully. Please try again", 'data =',data)
        data = "Sorry, no decoded data :("
    else:
        print("Message decoded successfully: ",'\n', data)

    return data

def signal_envelope(filtered):
    raw_data = filtered
    raw_data_diff = np.diff(raw_data, 1)
    raw_data_envelope = np.abs(signal.hilbert(raw_data_diff))
    sig = signal.firwin(numtaps=100, cutoff=freq_bitrate *
                        2, fs=sampling_freq)

    raw_data_filtered = signal.lfilter(sig, 1.0, raw_data_envelope)
    return raw_data_filtered

def find_head_tail(sig_data):
#FINDING HEAD AND TAIL IN ORDER TO IDENTIFY MESSAGE
    pad_head = '1111111111111'
    pad_tail='1111111111111'
    sig_data = pad_head+sig_data+pad_tail

    itr_1 = 0
    itr_2 = 0
    len_sig_data = len(sig_data)

    bin = ""
    app_str_data = "1111111111111010101010101010101010"

    sig_list = []
   
    if app_str_data in sig_data:
        print(True)
    else:
        print(False)

    for i in range(len_sig_data-29):

        x = sig_data[i:i+len(app_str_data)]
        if x == app_str_data:
            itr_1 = i + len(app_str_data)
            sig_list.append(x)
            break


    added_str = "10101010101010101010111111"
    for i in reversed(range(len_sig_data)):
        x = sig_data[i-len(added_str):i]
        if x == added_str:
            itr_2 = i-len(added_str)
            break
    bin = sig_data[itr_1:itr_2]

    return bin

    
def remove_silent(x):
    loudess = rms(x*1.0)
    loud = []
    for dig,i in enumerate(loudess.flatten()):
        if i > 0.05:
            loud.append(dig)
    Min = frames_to_samples(min(loud))
    Max = frames_to_samples(max(loud))
    return x[Min:Max]*1.0

def filter_freqs(x):
    x = remove_silent(x)
    X,y,stf = signal.stft(x,nfft=2048,nperseg=2048,noverlap=1536)
    librosa.display.specshow(stf)
    plot.show()
    for c in range(len(stf)):
        if c < 480 or c > 550:
            stf[c] = stf[c]*0
    librosa.display.specshow(stf)
    plot.show()
    sample = signal.istft(stf,nfft=2048,nperseg=2048,noverlap=1536)
    return sample[1]

def normalize(x):
    Max = np.max(x)
    X = x*(1/Max)

    return X
    
def decode_non_return_to_zero(data):

    '''
    converts non-return-to-zero to binary
    '''
    Data = ""
    prev = 1
    while (len(data)):
        curr = data[:1]
        data = data[1:]
        if curr != prev:
            Data += "1"
        else:
            Data += "0"
        prev = curr
    return Data


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


record_audio()
demodulator("recording.wav")