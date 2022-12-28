import numpy as np 
import math
def makemimicsound(fStart,fEnd,BatCallConstant,amp,fs,dur):
    pi =np.pi
    nframes=int(dur*fs+1)
    arg= (BatCallConstant*fEnd)/fStart
    call=[]
    fStart=fStart/100
    fEnd=fEnd/100
    for i in range(nframes):
        t = float(i)/fs*100
        call.append(amp*np.sin(2.*pi*((fStart/(fStart-BatCallConstant*fEnd))*((fStart-fEnd)*np.float_power(arg, t)/math.log(arg)+(1-BatCallConstant)*fEnd*t))))
    return call

def makeLFM(fStart,fEnd,amp,fs,dur):
    pi =np.pi
    nframes=int(dur*fs+1)
    arg= np.float_power((fEnd/fStart),(1/dur))
    call=[]
    fStart=fStart/100
    fEnd=fEnd/100
    for i in range(nframes):
        t = float(i)/fs*100
        call.append(amp*np.sin(2.*pi*fStart*np.float_power(arg,t)/math.log(arg)))
    return call
    
def LPMCall( fi,ft,Dur, fs, amp):
    def GetLPMValue(fi,ft,Dur):
        return (1-ft/fi)/(ft*Dur)
    def GetLPMPhase(i,fi,fs,value):
        t = i/fs
        return 2.*np.pi*(1/value)*np.log(1+value*fi*t)
    nframes = (int)(Dur*fs+1)
    value = GetLPMValue(fi,ft,Dur)
    call = np.zeros(nframes)
    phase = np.zeros(nframes)
    for i in range(nframes):
        phase[i] = GetLPMPhase(i,fi,fs,value)
    for i in range(nframes):
        call[i] = amp*np.sin(phase[i])
    return call