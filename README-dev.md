# Черновые инструкции и хронология

## Установка VOSK-сервера (черновик)

> **Внимание:** эта инструкция находится в стадии уточнения.  
> Она описывает промежуточную схему установки VOSK-сервера без прав root.  
> Окончательная версия будет приведена после успешного тестирования цепочки:  
> AudioRelay (Android) → Termux → VPS (VOSK-сервер) → Termux.

---

### Шаги установки

#### Шаг 0: Очистка

rm -rf ~/vosk-env ~/model ~/server.py ~/start-vosk.sh ~/.bashrc.bak_step4 vosk-model-*.zip vosk-backup.tar.gz

#### Шаг 1: Создание окружения

python3.8 -m venv ~/vosk-env
source ~/vosk-env/bin/activate
pip install --upgrade pip
pip install vosk websockets

#### Шаг 2: Модель и server.py

wget https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
unzip vosk-model-small-ru-0.22.zip
mv vosk-model-small-ru-0.22 ~/model

nano ~/server.py
# [вставить код сервера]

#### Шаг 3: Проверка вручную

source ~/vosk-env/bin/activate
python ~/server.py

#### Шаг 4: Автозапуск и подсказка

cp ~/.bashrc ~/.bashrc.bak_step4

cat << 'EOB' >> ~/.bashrc

### >>> VOSK AUTOLAUNCH + STATUS HINT ###
echo -e "\n\033[1;32m[ VOSK SERVER STATUS ]\033[0m"
echo "Для запуска вручную:"
echo "  source ~/vosk-env/bin/activate && python ~/server.py"
echo
echo "Для проверки статуса:"
echo "  pgrep -f server.py && echo 'VOSK работает' || echo 'VOSK НЕ запущен'"
echo

pgrep -f server.py > /dev/null || (
    echo "[!] Автоматический запуск сервера VOSK..."
    source ~/vosk-env/bin/activate && python ~/server.py &
)
### <<< VOSK AUTOLAUNCH + STATUS HINT ###
EOB

---

#### Откаты

- Удаление окружения: `rm -rf ~/vosk-env`
- Удаление модели и скрипта: `rm -rf ~/model ~/server.py`
- Откат bashrc: `mv ~/.bashrc.bak_step4 ~/.bashrc`
