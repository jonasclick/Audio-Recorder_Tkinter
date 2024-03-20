import os
import wave
import time
import threading
import tkinter as tk
import pyaudio

# why using a class? things can refer to each other,
# unlike buttons and functions which are separate
class VoiceRecorder: 

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.button = tk.Button(text='✆', font=('Arial', 120, 'bold'), 
                                command=self.click_handler)
        self.button.pack()
        self.label = tk.Label(text='00:00:00')
        self.label.pack()
        self.recording = False
        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg='black')
        else:
            self.recording = True
            self.button.config(fg='red')

            #threading runs the recording process PARALLEL to the GUI process.
            threading.Thread(target=self.record).start() 
    
    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, 
                            input=True, frames_per_buffer=1024)
        
        frames = []

        start = time.time()

        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60

            # :02d adds zeros if there's no value, i.E. 8 will be 08.
            self.label.config(text=f'{int(hours):02d}:{int(mins):02d}:{int(secs):02d}') 

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        i = 1
        while exists:
            if os.path.exists(f'recording{i}.wav'):
                i += 1
            else:
                exists = False

        sound_file = wave.open(f'recording{i}.wav', 'wb') #wb = write bytes
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()


VoiceRecorder()