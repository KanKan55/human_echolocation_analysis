import numpy as np 
from scipy.fftpack import fft, ifft
from scipy.signal import hilbert

## 相互相関処理
def Xcor_func(Txwv, Rxwv):
    txspc = fft(Txwv)
    crwv = ifft(fft(Rxwv) * np.conj(txspc)).real
    hlbwv = hilbert(crwv)
    env = np.abs(hlbwv)
    return env

## High-Pass-Filter　設計
def high_pass_filter(data, cutfreq, fs=1000000):
    f_array = np.linspace(0.0, fs, len(data))
    spc = fft(data)
    spc_filter = np.zeros(len(data), dtype=complex)
    for i in range(len(data)):
        if (f_array[i] < cutfreq) or (f_array[i] > fs - cutfreq):
            spc_filter[i] = 0
        else:
            spc_filter[i] = spc[i]

    wav = np.real(ifft(spc_filter))
    return wav

## Low-Pass-Filter 設計
def low_pass_filter(data, cutfreq, fs=1000000):
    f_array = np.linspace(0.0, fs, len(data))
    spc = fft(data)
    spc_filter = np.zeros(len(data), dtype=complex)
    for i in range(len(data)):
        if (f_array[i] > cutfreq) and (f_array[i] < fs - cutfreq):
            spc_filter[i] = 0
        else:
            spc_filter[i] = spc[i]

    wav = np.real(ifft(spc_filter))
    return wav

## Band-Pass-Filter 設計
def band_pass_filter(data, highcutfreq, lowcutfreq, fs= 1000000):
    f_array = np.linspace(0.0, fs, len(data))
    spc = fft(data)
    spc_filter  = np.zeros(len(data), dtype=complex)
    for i in range(len(data)):
        if ((f_array[i] > lowcutfreq) and (f_array[i] < fs - lowcutfreq)) or (f_array[i] < highcutfreq) or (f_array[i] > fs - highcutfreq):
            spc_filter[i] = 0
        else :
            spc_filter[i] = spc[i]
    
    wav = np.real(ifft(spc_filter))
    return wav

## downsampling　設計　(エイリアスも考慮）
def downsampling(data, input_fs, output_fs):
    n = input_fs / np.gcd(int(output_fs), int(input_fs))
    input_len = len(data)
    arr = np.concatenate([data - data.mean(), np.zeros(int(n - input_len % n))])
    wav_len = int(len(arr) / input_fs * output_fs)
    spc = fft(arr)
    wav_spc = np.concatenate([spc[: wav_len // 2], spc[-wav_len // 2 :]])
    wav_data = ifft(wav_spc * wav_len / len(arr)).real
    m = 2 ** (np.ceil(np.log2(wav_len))).astype(int)
    wav_data = np.concatenate([wav_data, np.zeros(m - len(wav_data))])
    return wav_data
