import pyaudio
import wave
import speech_recognition as sr
import os

from  AppKit import NSSpeechSynthesizer
import time
import sys

import aiml

CHUNK = 1024
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 2
RATE = 44100 #sample rate
RECORD_SECONDS = 5
THRESHOLD = 3500

def listen():
    WAVE_OUTPUT_FILENAME = "output1.wav"
    stream = None
    
    try:
        os.remove(WAVE_OUTPUT_FILENAME)
    except:
        print "no file"
        
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK) #buffer
    
    print("* recording")
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data) # 2 bytes(16 bits) per channel
    
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()    
    return WAVE_OUTPUT_FILENAME

def listenAudio():
    r=sr.Recognizer()
    
    #Microphone(device_index=i, sample_rate=48000)
    with sr.Microphone(sample_rate=48000) as source:
        print("Say Something!")
        audio=r.listen(source) 
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text  = r.recognize_google(audio)
            print(text)
            
        except sr.UnknownValueError:
            print("could not understand audio")
            text = ''
        except sr.RequestError as e:
            text = ''
            print("Could not request results; {0}".format(e))  
        
        return text
    
def speak(sentense):
    print sentense
    nssp = NSSpeechSynthesizer
    
    ve = nssp.alloc().init()

    #voices = ["com.apple.speech.synthesis.voice.Alex",
            #"com.apple.speech.synthesis.voice.Vicki",
            #"com.apple.speech.synthesis.voice.Victoria",
            #"com.apple.speech.synthesis.voice.Zarvox" ]

    voice = "com.apple.speech.synthesis.voice.Alex"
    ve.setVoice_(voice)
    ve.startSpeakingString_(sentense)
    while ve.isSpeaking():
        time.sleep(1)
    

kernel = aiml.Kernel()

kernel.setBotPredicate("name","Nick")
kernel.learn("std-startup.xml")
kernel.respond("LOAD AIML B")

while True:
    print kernel.respond(raw_input("Enter your Message: " ))
    #response = listenAudio()
    #if response != '':
        #speak(kernel.respond(response))
        #time.sleep(3)

