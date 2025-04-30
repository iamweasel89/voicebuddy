import queue
import sounddevice as sd
import sys
import json
from vosk import Model, KaldiRecognizer

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def main():
    model_path = "model"
    model = Model(model_path)

    samplerate = 16000
    device = None

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
