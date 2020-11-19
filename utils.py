import numpy as np

def process_key(key_str):
    key_str = key_str.split('*')
    key = np.array(key_str, dtype=int).reshape(4, 4)
    return key