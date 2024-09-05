import pyaudio
import wave

def capture_audio(filename="output.wav", duration=5):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    stream = p.open(format=sample_format, channels=channels, rate=fs,
                    frames_per_buffer=chunk, input=True)

    frames = []  # Initialize array to store frames

    for _ in range(0, int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    output_path = f"data_storage/audio/{filename}"  
    # Save the recorded data as a WAV file
    wf = wave.open(output_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
