import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, hilbert, resample
import soundfile as sf
import math

carrier_freq = 500000
modulation_coeff = 0.7


def process_audio(input_file, output_file, noise_level=0.1):
    # Загрузка аудио и получение частоты дискретизации
    audio, fs = sf.read(input_file)
    audio_copy = audio.copy()
    print(f"Загружен файл с частотой дискретизации: {fs} Гц")
    up_factor = math.ceil(carrier_freq / fs) * 3

    # Конвертация в моно и нормализация
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)

    audio = audio / np.max(np.abs(audio))
    audio = resample(audio, up_factor * len(audio))
    fs = up_factor * fs

    t_max = len(audio) / fs
    t = np.linspace(0, t_max, (int)(t_max * fs))
    # 1. Амплитудная модуляция
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    modulated = (1 + modulation_coeff * audio) * carrier

    # 2. Добавление высокочастотных помех
    hf_noise = 0.0
    # Генерация 3 случайных высокочастотных помех
    for _ in range(3):
        freq = np.random.uniform(carrier_freq + 5000, fs / 2 - 1000)
        amplitude = np.random.uniform(0.1, 0.3) * noise_level
        hf_noise += amplitude * np.sin(2 * np.pi * freq * t)

    transmitted = modulated + hf_noise

    # Имитация высокодобротного колебательного контура через полосовой фильтр
    bandwidth = carrier_freq * 0.06
    b, a = butter(10, [carrier_freq - bandwidth / 2, carrier_freq + bandwidth / 2], btype='bandpass',
                  fs=fs)  # Увеличили порядок фильтра
    filtered = filtfilt(b, a, transmitted)

    # 4. Детектирование огибающей
    analytic_signal = hilbert(filtered)
    detected = np.abs(analytic_signal)

    # 5. Адаптивный ФНЧ с улучшенными параметрами
    lpf_cutoff = 20000
    b, a = butter(6, lpf_cutoff, btype='low', fs=fs)
    recovered = filtfilt(b, a, detected)

    # Нормализация и сохранение
    recovered = recovered - np.mean(recovered)
    recovered = recovered[::up_factor]
    sf.write(output_file, recovered, int(fs / up_factor))

    print(f"Успешно! Результат сохранен в {output_file}")

    plt.subplot(2, 1, 1)
    plt.plot(audio_copy, 'g')
    plt.ylabel('Amplitude')
    plt.xlabel('Modulator signal')
    plt.subplot(2, 1, 2)
    plt.plot(recovered, color="purple")
    plt.ylabel('Amplitude')
    plt.xlabel('AM signal')

    plt.subplots_adjust(hspace=1)
    plt.rc('font', size=15)
    plt.show()


process_audio(
    input_file='compress.wav',
    output_file='output2.wav',
    noise_level=1
)
