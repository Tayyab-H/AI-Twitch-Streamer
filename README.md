# AI-VTUBER


**This is a POC**
 
This allows you to create a vtube avatar that uses a Local Large Language Model to responds dynamically to twitch chat in character depending on BasePrompt.txt

This will require a decent gpu, specifically an RTX card if possible (with cuda support at minimum) to run even somewhat low latency. 

Use with oobobooga webui in --listen mode and --no-stream mode, vtubestudio and voicemeeter banana
Route the output of the .wav into vtube studio using voicemeeter.
Current best LLM to use is llama-7b-4bit-128g
