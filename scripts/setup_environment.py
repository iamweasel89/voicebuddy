import os
import subprocess
import zipfile
import urllib.request

VOSK_MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
VOSK_MODEL_ZIP = "vosk-model-small-ru-0.22.zip"
VOSK_MODEL_DIR = "model"

def install_dependencies():
    print("Установка зависимостей...")
    subprocess.run(["pip3", "install", "--upgrade", "pip"], check=True)
    subprocess.run(["pip3", "install", "vosk", "sounddevice"], check=True)

def download_model():
    print("Скачиваем модель VOSK...")
    urllib.request.urlretrieve(VOSK_MODEL_URL, VOSK_MODEL_ZIP)

def extract_model():
    print("Распаковываем модель...")
    with zipfile.ZipFile(VOSK_MODEL_ZIP, 'r') as zip_ref:
        zip_ref.extractall(".")
    os.rename("vosk-model-small-ru-0.22", VOSK_MODEL_DIR)

def main():
    print("=== Инициализация окружения VoiceBuddy ===")
    
    install_dependencies()
    
    if not os.path.exists(VOSK_MODEL_DIR):
        download_model()
        extract_model()
        os.remove(VOSK_MODEL_ZIP)
    else:
        print("Модель уже существует, пропускаем загрузку.")

    print("=== Готово ===")

if __name__ == "__main__":
    main()
