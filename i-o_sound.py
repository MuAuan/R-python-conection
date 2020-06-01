# -*- coding:utf-8 -*-
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import wave
import struct

def savewav(sig,sk):
    RATE = 44100 #サンプリング周波数
    #サイン波を-32768から32767の整数値に変換(signed 16bit pcmへ)
    msig = max(sig)
    print(msig)
    swav = [(int(32766*x)) for x in sig] #32767
    #バイナリ化
    binwave = struct.pack("h" * len(swav), *swav)
    #サイン波をwavファイルとして書き出し
    w = wave.Wave_write("./wine/"+str(sk)+".wav")
    params = (1, 2, RATE, len(binwave), 'NONE', 'not compressed')
    w.setparams(params)
    w.writeframes(binwave)
    w.close()

RATE=44100
p=pyaudio.PyAudio()
N=100
CHUNK=1024*N
stream=p.open(format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        frames_per_buffer = CHUNK,
        input = True,
        output = True) # inputとoutputを同時にTrueにする

sk=0
while stream.is_active():
    input = stream.read(CHUNK, exception_on_overflow = False)
    print(len(input))
    sig =[]
    sig = np.frombuffer(input, dtype="int16") / 32768
    savewav(sig,sk)
    plt.plot(sig[0:1024])
    plt.pause(0.5)
    plt.savefig("./wine/sound_"+str(sk)+".png")
    plt.close()
    plt.plot(sig[0:CHUNK])
    plt.pause(0.5)
    plt.savefig("./wine/sound_C_"+str(sk)+".png")
    plt.close()
    sk+=1
    output = stream.write(input)
