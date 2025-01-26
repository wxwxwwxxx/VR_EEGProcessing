import numpy as np

# 输入array格式 [24,26,3000]
# 单个数据 [26,3000]
#数量级 0.01

from scipy.signal import butter, filtfilt
from sklearn.preprocessing import StandardScaler
from scipy.signal.windows import hamming
from scipy.signal import welch

# 采样频率和滤波范围


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

# 滤波数据
def bandpass_filter(data, lowcut, highcut, fs):
    b, a = butter_bandpass(lowcut, highcut, fs)
    return filtfilt(b, a, data)


# 实时数据流处理（示例：模拟数据流）
def preprocess_all(data,fs = 1000,lowcut = 1.0,highcut = 40.0):
    filtered_data = bandpass_filter(data, lowcut, highcut, fs)
    window = hamming(len(filtered_data))[:,None]
    data_windowed = filtered_data * window  # 数据乘上窗函数
    scaler = StandardScaler()
    filtered_data_normalized = scaler.fit_transform(data_windowed.T).T  # 按时间维度标准化
    return filtered_data_normalized
# 特征提取


def extract_band_power(data, sf, band):
    freqs, psd = welch(data, fs=sf, nperseg=1024)
    band_freqs = (freqs >= band[0]) & (freqs <= band[1])
    power = np.sum(psd[band_freqs])
    return power



# 计算给定频带范围的功率（例如Alpha波 8-12Hz）
def extract_band_power(data, sf, band):
    # 计算功率谱密度（PSD）
    freqs, psd = welch(data, fs=sf, nperseg=sf)  # nperseg为采样率（1000），即每个窗口1秒
    # 找到所需频带的索引
    band_freqs = (freqs >= band[0]) & (freqs <= band[1])
    # 计算目标频带的功率
    power = np.sum(psd[band_freqs])  # 将目标频带的功率加总
    return power

# 设置Alpha波频带（8-12Hz）

# 采样率1000Hz
def extract_feature(data,sf,z_score=True):
    freq_bands = [(1, 5), (5, 8), (8, 13), (13, 30), (30, 40)]  # (1, 40)
    feature = []
    for band in freq_bands:
        feature.append(np.stack([extract_band_power(data[i, :], sf, band) for i in range(data.shape[0])])[None,:])
    feature = np.concatenate(feature)
    if z_score:
        mean = np.mean(feature)  # 计算均值
        std = np.std(feature)  # 计算标准差
        feature = (feature - mean) / std
    return feature



if __name__ == '__main__':
    data = np.random.normal(size=(26, 3000))
    print(extract_feature(1000,data))
