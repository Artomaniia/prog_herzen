import os
from configparser import ConfigParser

CONFIG_PATH = os.path.expanduser("~/.config/mimeapps.list")
SECTION = "Default Applications"


def read_associations(path=None):
    """Читает mimeapps.list и возвращает {mime_type: desktop_file}."""
    path = path or CONFIG_PATH
    parser = ConfigParser()
    parser.optionxform = str
    if os.path.exists(path):
        parser.read(path, encoding="utf-8")
    if SECTION in parser:
        return dict(parser[SECTION])
    return {}


def merge_associations(base, override):
    """Объединяет два словаря; при совпадении ключей побеждает override."""
    result = dict(base)
    result.update(override)
    return result


def write_associations(associations, path=None):
    """Записывает словарь ассоциаций в mimeapps.list."""
    path = path or CONFIG_PATH
    parser = ConfigParser()
    parser.optionxform = str
    if os.path.exists(path):
        parser.read(path, encoding="utf-8")
    if SECTION in parser:
        parser.remove_section(SECTION)
    parser.add_section(SECTION)
    for mime, desktop in associations.items():
        parser[SECTION][mime] = desktop
    with open(path, "w", encoding="utf-8") as f:
        parser.write(f)
