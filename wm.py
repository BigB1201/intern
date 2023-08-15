# %%

import matplotlib.pyplot as plt
from numpy import median, multiply, divide, abs as magnitude
from scipy.fftpack import rfft as fft, irfft as ifft
from scipy.io import wavfile

def twin_plots(fig_name: str, time_data, freq_data):
    fig, (axt, axf) = plt.subplots(2, 1, constrained_layout = 1,figsize = (11.8,3))
    fig.suptitle(fig_name, fontsize = 20)
    axt.plot(time_data, lw = 0.15) ; axt.grid(1)
    plt.xlim([0, 8000]); axf.plot(magnitude(freq_data), lw = 0.15) ; axf.grid(1)
    plt.show()

def zero_frequencies(audiofile: str, frequencies: list[tuple]):
    sample_rate, signal = wavfile.read(f"{audiofile}.wav")
    Signal = fft(signal)

    med = median(signal)
    RSignal = divide(Signal, med)
    for bounds in frequencies:
        for index in range(bounds[0], bounds[1]):
            RSignal[index] = 0
    rsignal = multiply(ifft(RSignal), med)

    twin_plots("Original signal", signal, Signal)
    twin_plots("Modified signal", rsignal, multiply(RSignal, med))

    wavfile.write(f"{audiofile} -{frequencies[0][0]}-{frequencies[0][1]}.wav", sample_rate, rsignal.astype(signal.dtype))

# zero_frequencies("vocofy", [(5000, 6000)])

def aftermash(audiopath: str, times: int):
    from conversion_cycle import ccycle
    from os.path import exists
    if not exists(f"./{audiopath} +mash-{times}.wav"): ccycle(times, f"{audiopath}.wav")
    _, p = wavfile.read(f"{audiopath} +mash-{times}.wav")
    twin_plots("Mashed signal", p, fft(p))
# %%
