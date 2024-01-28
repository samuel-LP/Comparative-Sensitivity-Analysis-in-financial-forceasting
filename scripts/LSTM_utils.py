import numpy as np

def prepare_data(data, n_steps):
    x, y = [], []
    for i in range(len(data) - n_steps):
        x.append(data[i:(i + n_steps), 0])
        y.append(data[i + n_steps, 0])
    return np.array(x), np.array(y)

def prepare_data2(data, n_steps, n_future=7):
    x, y = [], []
    for i in range(len(data) - n_steps - n_future + 1):
        x.append(data[i:(i + n_steps), 0])
        y.append(data[(i + n_steps):(i + n_steps + n_future), 0])
    return np.array(x), np.array(y)