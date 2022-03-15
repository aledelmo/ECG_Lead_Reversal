import ast
import pywt
import wfdb
import os.path
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import resample
from biosppy.signals.tools import filter_signal


def load_raw_data(df, _sampling_rate, _path, drop):
    if _sampling_rate == 100:
        data = [wfdb.rdsamp(_path+f) for i, f in enumerate(df.filename_lr[:40]) if i not in drop]
    else:
        data = [wfdb.rdsamp(_path+f) for f in df.filename_hr]
    data = [signal[:, 3] for signal, meta in data]
    return np.array(data)


def madev(d, axis=None):
    """ Mean absolute deviation of a signal """
    return np.mean(np.absolute(d - np.mean(d, axis)), axis)


def wavelet_denoising(x, wavelet='db4', level=1):
    coeff = pywt.wavedec(x, wavelet, mode="per", level=level)
    #coeff[0] = np.array([0 if i != 6 else coeff[0][i] for i in range(len(coeff[0]))])

    #keep = [0, level - 6 + 1, level - 5 + 1, level - 4 + 1]
    #for i in range(len(coeff)):
    #    if i not in keep:
    #        coeff[i] = np.zeros(len(coeff[i]))

    sigma = madev(coeff[-1]) / 0.6745
    uthresh = sigma * np.sqrt(2 * np.log(len(x)))
    coeff[1:] = (pywt.threshold(i, value=uthresh, mode='hard') for i in coeff[1:])
    return pywt.waverec(coeff, wavelet, mode='per')


path = 'data/ptb-xl/'
sampling_rate = 100

ds_x = pd.read_csv(os.path.join(path, 'ptbxl_database.csv'), index_col='ecg_id')

y_train = [max(ast.literal_eval(code), key=ast.literal_eval(code).get)
           if max(ast.literal_eval(code).values()) > 20 else 'NONE'
           for code in ds_x.scp_codes]
class_dict = {'NORM': 1,
              'LAFB': 2, 'LPFB': 2, 'IRBBB': 2, 'CLBBB': 2, 'CRBBB': 2, 'IVCD': 2, '_AVB': 2, 'WPW': 2, 'ILBBB': 2,
              'STTC': 3, 'NST_': 3, 'ISCA': 3, 'ISC_': 3, 'ISCI': 3,
              'AMI': 4, 'IMI': 4, 'LMI': 4,
              'LVH': 5, 'LAO': 5, 'LAE': 5, 'RAO': 5, 'RAE': 5,
              }
to_drop = [i for i, c in enumerate(y_train) if c not in class_dict]


x_train = load_raw_data(ds_x, sampling_rate, path, drop=to_drop)
y_train = [class_dict[c] for i, c in enumerate(y_train) if i not in to_drop]

sns.countplot(x=y_train)
plt.show()

wav = pywt.Wavelet('db4')
filtered = wavelet_denoising(x_train[0, :], wavelet=wav, level=int(np.log2((0.6745 * 100) / 0.5)))
plt.plot(x_train[0, :], label='Raw')
plt.plot(filtered, label='High-Frequency Filtered')
plt.show()

order = int(0.3 * sampling_rate)
filtered2, _, _ = filter_signal(
        signal=filtered,
        ftype="FIR",
        band="highpass",
        order=order,
        frequency=2.5,
        sampling_rate=sampling_rate,
    )
plt.plot(filtered, label='High-Frequency Filtered')
plt.plot(filtered2, label='Drift Removed')
plt.show()

target_samplerate = 200
sample_ratio = target_samplerate / sampling_rate

resampled = resample(filtered2, int(len(filtered2)*sample_ratio))
plt.plot(resampled, label='Resampled')
plt.show()

