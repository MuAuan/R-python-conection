#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import pyper
import wave
import pyaudio
 
r=pyper.R()
r("source(file='r-python.R')")
rwav=r.get("wp")

def printWaveInfo(wf):
    #WAVEファイルの情報
    print("チャンネル数:", wf.getnchannels())
    print("サンプル幅:", wf.getsampwidth())
    print("サンプリング周波数:", wf.getframerate())
    print("フレーム数:", wf.getnframes())
    print("長さ（秒）:", float(wf.getnframes()) / wf.getframerate())
    print("パラメータ:", wf.getparams())
    print("\n")
 
if __name__ == '__main__':
    wf = wave.open(rwav, "r")
 
    printWaveInfo(wf)
 
    # ストリームを開く
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
 
    # チャンク単位でストリーム出力
    chunk=2048
    data = wf.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.close()
    p.terminate()
