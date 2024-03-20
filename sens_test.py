import pyaudio
import wave
import RPi.GPIO as GPIO
import time


PIR_PIN = 17  
GPIO.setmode(GPIO.BCM)  
GPIO.setup(PIR_PIN, GPIO.IN)  


FORMAT = pyaudio.paInt16  
CHANNELS = 1              
RATE = 44100              
CHUNK = 1024              
RECORD_SECONDS = 5        
WAVE_OUTPUT_FILENAME = "motion_detected_output.wav"  


audio = pyaudio.PyAudio()

def record_audio():
    # Open stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Motion detected! Recording...")

    frames = []

    
    for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording stopped.")

    
    stream.stop_stream()
    stream.close()

    
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

try:
    print("PIR Module Test (CTRL+C to exit)")
    time.sleep(2)
    print("Ready")

    while True:
        if GPIO.input(PIR_PIN):
            record_audio()
            
            time.sleep(RECORD_SECONDS + 2)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
