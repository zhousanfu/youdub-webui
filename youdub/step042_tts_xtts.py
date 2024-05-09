#!python3.10
# coding=utf-8
'''
 Author: Sanfor Chow
 Date: 2024-04-23 21:47:57
 LastEditors: Sanfor Chow
 LastEditTime: 2024-05-03 10:13:06
 FilePath: /YouDub-webui/youdub/step042_tts_xtts.py
'''
import os
from TTS.api import TTS
from loguru import logger
import numpy as np
import torch
import time
import edge_tts
import asyncio
from pydub import AudioSegment
try:
    from .utils import save_wav
except:
    from utils import save_wav
model = None

def init_TTS():
    load_model()
    
def load_model(model_path="tts_models/multilingual/multi-dataset/xtts_v2", device='auto'):
    global model
    if model is not None:
        return

    if device=='auto':
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f'Loading TTS model from {model_path}')
    t_start = time.time()
    model = TTS(model_path).to(device)
    t_end = time.time()
    logger.info(f'TTS model loaded in {t_end - t_start:.2f}s')
    

def tts(text, output_path, speaker_wav, model_name="tts_models/multilingual/multi-dataset/xtts_v2", device='auto', language='zh-cn'):
    global model
    
    if os.path.exists(output_path):
        logger.info(f'TTS {text} 已存在')
        return
    
    if model is None:
        load_model(model_name, device)
    
    for retry in range(3):
        try:
            wav = model.tts(text, speaker_wav=speaker_wav, language=language)
            wav = np.array(wav)
            save_wav(wav, output_path)
            logger.info(f'TTS {text}')
            break
        except Exception as e:
            logger.warning(f'TTS {text} 失败')
            logger.warning(e)

async def tts_function(text, output_path):
    tts = edge_tts.Communicate(
        text,
        voice='zh-CN-XiaoyiNeural',
        rate='-4%',
        volume='+0%'
        )
    await tts.save(output_path.split('.')[0] + '.mp3')
    audio = AudioSegment.from_mp3(output_path.split('.')[0] + '.mp3')
    audio.export(output_path, format="wav")


if __name__ == '__main__':
    # speaker_wav = r'videos/3Blue1Brown/20190113 The most unexpected answer to a counting puzzle/audio_vocals.wav'
    # while True:
    #     text = input('请输入：')
    #     tts(text, f'playground/{text}.wav', speaker_wav)
    asyncio.run(tts_function(
        text='有时数学和物理会相互作用，产生的结果让人感到太过奇怪。',
        output_path='videos/zh-CN-shaanxi-XiaoniNeural.wav'
    ))
        
