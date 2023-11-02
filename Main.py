import requests
import json
import pyttsx3
from twitch_chat import TwitchChat
import tts
import dotenv
import os


def TTS(text):
    engine = pyttsx3.init("espeak-ng")
    engine.say(text)
    engine.runAndWait()

def SendToLLM(prompt, user = "Tayyab", chatmode = False):
    server = "127.0.0.1"
    f = open("BasePrompts.txt", "r")
    BasePrompt = f.read()
    
    headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    }
    
    params = {
    'max_new_tokens': 65,
    'do_sample': True,
    'temperature': 0.44,
    'top_p': 1,
    'typical_p': 1,
    'repetition_penalty': 1.15,
    'encoder_repetition_penalty': 1.0,
    'top_k': 0,
    'min_length': 0,
    'no_repeat_ngram_size': 0,
    'num_beams': 1,
    'penalty_alpha': 0,
    'length_penalty': 1,
    'early_stopping': False,
    'seed': -1,
    'add_bos_token': True,
    'truncation_length': 2048,
    'ban_eos_token': False,
    'skip_special_tokens': True,
    'stopping_strings': [],
}
    
    if chatmode == True:
        prompt = user + " in chat: " + prompt
    else:
        prompt = user + ": " + prompt
    
    
    payload = json.dumps([BasePrompt+"\n"+ prompt + "<ENDOFTURN>" , params])
    
    response = requests.post(f"http://{server}:7860/run/textgen", json={"data": [payload]}).json()

    reply = response["data"][0]
    #print(reply)
    reply = reply[reply.find("Current chat:") + 13:]
    #print(reply)
    reply = reply[reply.find("<ENDOFTURN>")+11:]
    #print(reply)
    return reply[reply.find("Sarah:")+6:reply.find("<ENDOFTURN>")]

def main():
    msgqueue = []
    model = tts.launch_tts()
    dotenv.load_dotenv()
    oath = os.getenv('OATH')
    channel = os.getenv('CHANNEL')
    my_chat = TwitchChat(oath=oath, bot_name='sarah', channel_name=channel)
    while True:
        user, message = my_chat.listen_to_chat()
        msgqueue.append((user, message))
        if len(msgqueue) > 1:
            user, message = msgqueue.pop(0)
            msgqueue = []
        if message[:6].lower() == "sarah:":
            message = message[6:]
            resp = SendToLLM(message, user=user, chatmode=True)
            print("\nchat reply:\n"+ resp)
            tts.run_tts(resp, model)
            tts.playtts()
        else:
            print(f"Error for message:\n{message}")
    

if __name__ == "__main__":
    main()
    
    

