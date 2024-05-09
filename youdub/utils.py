#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-05-01 08:32:34
 LastEditors: Sanfor Chow
 LastEditTime: 2024-05-09 17:36:52
 FilePath: /YouDub-webui/youdub/utils.py
'''
import re
import string
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment



def convert_khz(output_file):
    # 输入文件路径和输出文件路径
    input_file = output_file
    output_file = output_file.split('.')[0] + '_16khz.wav'

    # 读取音频文件
    audio = AudioSegment.from_wav(input_file)

    # 设置目标采样率为16 kHz
    target_sample_rate = 16000

    # 执行采样率转换
    audio = audio.set_frame_rate(target_sample_rate)

    # 导出音频文件
    audio.export(output_file, format="wav")

def sanitize_filename(filename: str) -> str:
    # Define a set of valid characters
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

    # Keep only valid characters
    sanitized_filename = ''.join(c for c in filename if c in valid_chars)

    # Replace multiple spaces with a single space
    sanitized_filename = re.sub(' +', ' ', sanitized_filename)

    return sanitized_filename


def save_wav(wav: np.ndarray, output_path: str, sample_rate=24000):
    # wav_norm = wav * (32767 / max(0.01, np.max(np.abs(wav))))
    wav_norm = wav * 32767
    wavfile.write(output_path, sample_rate, wav_norm.astype(np.int16))

def save_wav_norm(wav: np.ndarray, output_path: str, sample_rate=24000):
    wav_norm = wav * (32767 / max(0.01, np.max(np.abs(wav))))
    wavfile.write(output_path, sample_rate, wav_norm.astype(np.int16))
    
def normalize_wav(wav_path: str) -> None:
    sample_rate, wav = wavfile.read(wav_path)
    wav_norm = wav * (32767 / max(0.01, np.max(np.abs(wav))))
    wavfile.write(wav_path, sample_rate, wav_norm.astype(np.int16))