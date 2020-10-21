# -*- coding: utf-8 -*-
import os
import sys
import datetime
import wave
import numpy as np
from scipy.stats import norm
#import matplotlib.pyplot as plt

def argumentsparser():
    usage = "Usage: python {}".format(__file__)
    arguments = sys.argv
    if len(arguments) > 1:
        return usage

if __name__ == '__main__' :
    if argumentsparser() is None :

        # normal distribution curve is used to simulate msm5232 output volume.        
        def dist(x):
            func = norm.pdf(x,1,5.8)*4000-23
            return func

        # an alternative curve
        #def tanh(x):
        #    a = 3
        #    b = 6.4/15
        #    tanh = ((np.exp(a - b*(x)) - 1)/(np.exp(a - b*(x)) + 1)/((np.exp(a)-1)/(np.exp(a)+1)) + 1)*100
        #    return tanh
        
        def wav1(x):
            xx = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
            flip = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
            ans = flip[x]*dist(xx[x])
            return ans
        
        def wav2(x):
            xx = np.array([0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7])
            flip = np.array([-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1])
            ans = flip[x]*dist(xx[x])
            ans = ans*0.6
            return ans
        
        def wav4(x):
            xx = np.array([0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3])
            flip = np.array([-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,1,1,1,1])
            ans = flip[x]*dist(xx[x])
            ans = ans*0.5
            return ans
        
        def wav8(x):
            xx = np.array([0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1])
            flip = np.array([-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1])
            ans = flip[x]*dist(xx[x])
            ans = ans*0.45
            return ans
        
        def switch(num: int, n: int):
            if num & (1 << n):
                return 1
            return 0

        now = datetime.datetime.now()
        dirname = "{0:%y%m%d%H%M%S}".format(now)
        os.makedirs(dirname, exist_ok=True)

        x = np.arange(32)
        y = np.empty(32)
        
        for i in range(1,16):

            #------MSM5232 like wavetable data calculation------
            for j in range(32):
                y[j] = switch(i,0)*wav1(j) + switch(i,1)*wav2(j) + switch(i,2)*wav4(j) + switch(i,3)*wav8(j)
            y = y * 127/max(max(y),-min(y))
            #print(y)
            #plt.bar(x,y)
            #plt.show()
            y = ((y + 127)/254*255*2 + 1) // 2
            list = y.astype(np.uint8).tobytes()

            #------wave for ELZ_1 output------
            fout = wave.Wave_write(dirname + "/" + "MSM5232Table" + "{0:02d}".format(i) + ".wav")
            fout.setparams((
                1,                 # mono
                1,                 # 8 bits = 1 byte
                48000,             # sampling bitrate
                32,                # samples
                "NONE",            # not compressed
                "not compressed"   # not compressed
                ))
            fout.writeframesraw(list)
            fout.close()
 
        print("\n15 wave files are created in the", dirname, "folder successfully.")
        print("The format is monoral, 8-bit, 48kHz and 32 samples.\nThose wave files are expected to be readable for an ELZ_1 synthesizer.")
           
    else: 
        print(argumentsparser())