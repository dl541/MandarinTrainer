import pyaudio
import numpy
import scipy.io.wavfile as wav
import wave
import sys

def audio_to_nparray():
    RATE=16000
    RECORD_SECONDS = 3
    CHUNKSIZE = 1024
    
    # initialize portaudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNKSIZE)
    
    frames = [] # A python-list of chunks(numpy.ndarray)
    for _ in range(0, int(RATE / CHUNKSIZE * RECORD_SECONDS)):
        data = stream.read(CHUNKSIZE)
        frames.append(numpy.fromstring(data, dtype=numpy.int16))
    
    #Convert the list of numpy-arrays into a 1D array (column-wise)
    numpydata = numpy.hstack(frames)

    
    return numpydata,RECORD_SECONDS
    # close stream
#    stream.stop_stream()
#    stream.close()
#    p.terminate()
#    
#    wav.write('out.wav',RATE,numpydata)
    



def play_audio(pinyin):
    CHUNK = 1024
    
    wf = wave.open(pinyin+'.wav', 'rb')
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(CHUNK)
    
    while len(data)>0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    
    stream.stop_stream()
    stream.close()
    
    p.terminate()