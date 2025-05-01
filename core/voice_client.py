import queue
import sounddevice as sd
import sys
import json
import socket
import re
from vosk import Model, KaldiRecognizer

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def extract_block(text):
    pattern = r"\b(краска|рубероид|швеллер)\s+(\d+)\b"
    match = re.search(pattern, text.lower())
    if match:
        return match.group(1), match.group(2)
    return None, None

def send_to_server(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', 5000))
        sock.sendall(data.encode('utf-8'))

def main():
    model_path = "model"
    model = Model(model_path)

    device = None
    samplerate = 16000

    rec = KaldiRecognizer(model, samplerate)
    rec.SetWords(True)

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                           dtype="int16", channels=1, callback=callback):
        print("=== Система готова к распознаванию ===")
        last_partial = ""
        try:
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if text:
                        print("\r" + text, end="", flush=True)
                        item, quantity = extract_block(text)
                        if item and quantity:
                            print(f"\nОтправляем блок на сервер: {item} {quantity}")
                            send_to_server(f"{item} {quantity}")
                else:
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "")
                    if partial_text != last_partial:
                        last_partial = partial_text
                        print("\r" + partial_text, end="", flush=True)

        except KeyboardInterrupt:
            print("\n\n--- Работа остановлена пользователем (Ctrl+C) ---")

if __name__ == "__main__":
    main()
