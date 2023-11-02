import requests
#from playsound import playsound
import torch
import wave
import sounddevice as sd
import soundfile as sf

def launch_tts():
    language = 'en'
    model_id = 'v3_en'

    model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                        model='silero_tts',
                                        language=language,
                                        speaker=model_id)
    return model

def run_tts(text, model):   
    sample_rate = 48000
    speaker = 'en_56'
    device = torch.device('cpu')
    model.to(device)  # gpu or cpu

    audio_paths = model.save_wav(text=text,
                             speaker=speaker,
                             sample_rate=sample_rate)
    print("Response Saved")
    #print(audio_paths)

def playtts():
    # Specify the audio device ID you want to use (replace with your device ID)
    device_id = 55

    # Load the WAV file
    file_path = 'test.wav'
    data, sample_rate = sf.read(file_path)

    # Get the list of available audio devices
    devices = sd.query_devices()
    device_name = "CABLE Input (VB-Audio Virtual C, MME"

    # Play the audio on the specified device
    sd.default.device = device_name
    sd.play(data, sample_rate)
    sd.wait()

#model = launch_tts()
#run_tts("Hello, my name is Sarah. I am a chatbot created by Tayyab. I am a work in progress, but I am learning more every day. I am currently in chat mode. I will respond to messages that start with my name. I am not perfect, but I am trying my best. I hope you enjoy my company.", model)    
#playtts()