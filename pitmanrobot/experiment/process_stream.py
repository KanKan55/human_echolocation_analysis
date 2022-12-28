import soundfile as sf
import numpy as np
## 左右のwavデータを引数にとって転置してからsoundfileモジュールで書き出し。
def mono2stereo(L_wav_data, R_wav_data, output_fs, output_name, output_path):
    wave = np.array([L_wav_data, R_wav_data])
    wave = wave.T
    sf.write(output_path + "/" + output_name, wave, output_fs)

## 直達音をゼロ詰し、エコー部分に重みを畳み込む（立ち上がりを抑える)
def process_soundwav(data, direct_pulse_time, output_fs):
    for i in range(int(direct_pulse_time * output_fs) + 1):
        data[i] = 0.0 
    w = np.hamming(len(data[int(direct_pulse_time*output_fs):]))
    for i in range(int(direct_pulse_time*output_fs), len(data), 1):
        data[i] = data[i]*w[i-int(direct_pulse_time*output_fs)]
    
    return data
