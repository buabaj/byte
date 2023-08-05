import numpy as np    
from numpy.lib.stride_tricks import as_strided

def frame_ify(x,frame_length=None,hop_length=None,axis=-1):
    # Breaks an array into frames based on frame length and hop length 
    n_frames = 1 + (x.shape[axis] - frame_length) // hop_length
    strides = np.asarray(x.strides)
    new_stride = np.prod(strides[strides > 0] // x.itemsize) * x.itemsize
    shape = list(x.shape)[:-1] + [frame_length, n_frames]
    strides = list(strides) + [hop_length * new_stride]

    return as_strided(x, shape=shape, strides=strides)

def rms(x,frame_length=2048,hop_length=512):
    #Calculates loudness
    # By finding root mean squared of each frame in audio samples
    x = frame_ify(x,frame_length,hop_length)
    power = np.mean(np.abs(x) ** 2, axis=0, keepdims=True)
    return np.sqrt(power)

def frames_to_samples(frames,hop_length=512):
    #Converts frames to samples
    return (np.asanyarray(frames) * hop_length).astype(int)



