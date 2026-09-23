import os
from configparser import ConfigParser

CONFIG_PATH = os.path.expanduser("~/.config/mimeapps.list")

def load_mimeapps():
    parser = ConfigParser()
    # mimeapps.list может не иметь кавычек, а configparser по умолчанию их ждёт,
    # поэтому отключаем обработку кавычек и разрешаем дубликаты ключей (если нужно).
    parser.optionxform = str  # сохранять регистр ключей
    if os.path.exists(CONFIG_PATH):
        parser.read(CONFIG_PATH, encoding="utf-8")
    else:
        # создадим пустой конфиг, если нет
        pass
    return parser

def save_mimeapps(parser):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        parser.write(f)

def set_default_app(mime_type, desktop_file):
    parser = load_mimeapps()
    section = "Default Applications"
    if section not in parser:
        parser.add_section(section)
    parser[section][mime_type] = desktop_file
    save_mimeapps(parser)

if __name__ == "__main__":
    # Пример: меняем дефолтное приложение для text/plain на code.desktop
    set_default_app("text/plain", "code.desktop")
