# scripts/server.py

import asyncio
import websockets
import json
from vosk import Model, KaldiRecognizer
import soundfile as sf

# Путь к модели (относительно корня проекта)
model_path = "model"  # или "vosk-model-small-ru-0.22" — в зависимости от того, как ты её называешь
model = Model(model_path)

async def recognize(websocket):
    rec = KaldiRecognizer(model, 16000)
    while True:
        data = await websocket.recv()
        if isinstance(data, str):
            data = data.encode('latin1')  # fallback, если вдруг пришла строка
        if rec.AcceptWaveform(data):
            await websocket.send(rec.Result())
        else:
            await websocket.send(rec.PartialResult())

async def main():
    print("Server started on port 2700")
    async with websockets.serve(recognize, "0.0.0.0", 2700):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
