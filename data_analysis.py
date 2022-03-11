import ast
import pywt
import wfdb
import os.path
import numpy as np
import pandas as pd
from biosppy.signals import ecg
import matplotlib.pyplot as plt


def load_raw_data(df, _sampling_rate, _path):
    if _sampling_rate == 100:
        data = [wfdb.rdsamp(_path+f) for f in df.filename_lr]
    else:
        data = [wfdb.rdsamp(_path+f) for f in df.filename_hr]
    data = [signal for signal, meta in data]
    return np.array(data)


path = 'data/ptb-xl/'
sampling_rate = 100

ds_x = pd.read_csv(os.path.join(path, 'ptbxl_database.csv'), index_col='ecg_id')
#ds_x.scp_codes = ds_x.scp_codes.apply(lambda x: ast.literal_eval(x))

x_train = load_raw_data(ds_x, sampling_rate, path)
y_train = ds_x.weight


def wavelet_denoising(x, wavelet='db4', level=1):
    coeff = pywt.wavedec(x, wavelet, mode="per")
    sigma = (1/0.6745) * madev(coeff[-level])
    uthresh = sigma * np.sqrt(2 * np.log(len(x)))
    coeff[1:] = (pywt.threshold(i, value=uthresh, mode='hard') for i in coeff[1:])
    return pywt.waverec(coeff, wavelet, mode='per')


def madev(d, axis=None):
    """ Mean absolute deviation of a signal """
    return np.mean(np.absolute(d - np.mean(d, axis)), axis)


fig, ax = plt.subplots(1, len(pywt.wavelist()[:2]))
for i, wav in enumerate(pywt.wavelist()[:2]):
    try:
        filtered = wavelet_denoising(x_train[0, :, 0], wavelet=wav, level=1)
        ax[0, i].plot(x_train[0, :, 0], label='Raw')
        ax[0, i].plot(filtered, label='Filtered')
        ax[0, i].set_title(f"DWT Denoising with {wav} Wavelet", size=15)
    except:
        pass
plt.show()

filtered = filtered*np.hamming(len(filtered))

plt.plot(filtered)
plt.show()

# #'sig_name': ['I', 'II', 'III', 'AVR', 'AVL', 'AVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
# out = ecg.ecg(signal=x_train[0, :, 0], sampling_rate=100., show=True)



