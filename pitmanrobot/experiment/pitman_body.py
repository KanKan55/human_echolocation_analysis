import numpy as np

## 窓関数を作成
def genWinFunc(winsize):
    radian = np.pi
    if winsize & (winsize - 1) != 0:
        print("error")
        exit

    # 8???
    oct = winsize / 8
    winFunc = np.zeros(winsize)

    for i in range(winsize):
        if i < oct or i >= oct * 7:
            winFunc[i] = 0
        elif i < oct * 3:
            winFunc[i] = np.sin(radian * (i - oct) / (oct * 4))
        elif i < oct * 5:
            winFunc[i] = 1
        else:
            winFunc[i] = np.sin(radian * (i - oct * 3) / (oct * 4))

    return winFunc

## 時変FIRフィルター設計
def genFir(pitch, tap):
    if pitch == 0:
        filtersize = tap
        downfilter = np.zeros(filtersize)
        for i in range(tap):
            if i == 0 or i == tap / 2:
                downfilter[i] = np.inf

        return downfilter
    else:
        semi = np.power(2, 1 / 12)
        ratio = np.power(semi, -(pitch))
        rate = 1.0 / (1 - ratio)
        sub = int(np.round(tap / 2.0 * rate))
        filtersize = tap * sub
        downfilter = np.zeros((sub, tap))
        amp = (64 * 1024 - 1.0) / tap
        cutoff = int(tap / (2.0 * ratio))

        spc_cmpl = np.zeros((sub, tap), dtype=np.complex128)
        cmpl = np.zeros((sub, tap), dtype=np.complex128)
        winFunc = genWinFunc(tap)
        for i in range(sub):
            for j in range(tap // 2):
                phase = float(i * j) * np.pi / float(sub)
                if j % 2 == 0:
                    spc_cmpl[i][j] = complex(amp * np.cos(phase), amp * np.sin(phase))
                    if j > 0 and j < tap // 2:
                        spc_cmpl[i][tap - j] = complex(
                            amp * np.cos(-phase), amp * np.sin(-phase)
                        )
            cmpl[i] = np.fft.ifft(spc_cmpl[i][:])
            for j in range(tap):
                downfilter[i][j] = (cmpl[i][tap - j - 1].real) * winFunc[tap - j - 1]

        return downfilter, sub

## 畳み込みしてコンバートする
def kanta_convolve(sig, tap, downfilter, sub):
    downsig = np.zeros(len(sig))
    io = tap // 8
    ie = tap - io
    k = 0
    for n in range(tap // 2, (tap) // 2 + len(sig), 1):
        j = n % sub

        conv = 0
        for i in range(io, ie, 1):
            conv = conv + (downfilter[j][i] * sig[(n - i + len(sig)) % len(sig)])

        downsig[k] = conv
        k = k + 1
    return downsig