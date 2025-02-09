import pyaudio
import vosk
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Initialize Vosk Speech-to-Text
model_path = "/home/weeshan29/car_project2/vosk-model-small-en-us-0.15"
vosk_model = vosk.Model(model_path)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=2000)  # Reduced buffer size
stream.start_stream()
rec = vosk.KaldiRecognizer(vosk_model, 16000)

# Initialize DistilGPT-2 Model for Text-to-Command
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")

# Predefined Commands for Filtering
predefined_commands = {
    "move forward": "forward",
    "go forward" :"forward",
    "go left": "left",
    "turn left": "left",
    "turn right": "right",
    "go right": "right",
    "stop": "stop",
    "move back": "backwards",
    "go backwards": "backwards",
    "move backwards": "backwards",
}

def generate_command(input_text):
    # Check predefined commands only
    if input_text in predefined_commands:
        return predefined_commands[input_text]
    else:
        return None  # Ignore invalid commands

# Main loop
print("Listening for voice commands...")

while True:
    data = stream.read(2000)

    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        recognized_text = result.get('text', '').strip()

        if recognized_text:
            print(f"Recognized Speech: {recognized_text}")

            # Generate a command only if it's predefined
            robot_command = generate_command(recognized_text)

            if robot_command:
                print(f"Robot Command: {robot_command}")
                # TODO: Add robot control logic here (e.g., moving the PiCar-X)
            else:
                print("Ignored: Command not recognized")
