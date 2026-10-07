import pytest
from pathlib import Path
from mimeapps import read_associations, merge_associations, write_associations

"""
Тест-план

read_associations:
  1. Чтение корректного файла с несколькими типами в [Default Applications].
  2. Файл без секции [Default Applications] — пустой словарь.
  3. Пустой файл — пустой словарь.
  4. Несуществующий файл — пустой словарь.

merge_associations:
  1. Словари с разными ключами объединяются.
  2. Совпадающие ключи — значение из override побеждает.
  3. Пустой base.
  4. Пустой override.
  5. Оба пустые.

write_associations:
  1. Запись непустого словаря — файл создаётся с корректным содержимым.
  2. Запись пустого словаря — файл создаётся, секция пустая.
  3. Перезапись существующего файла — старое содержимое затирается.
  4. Roundtrip: write → read возвращает исходный словарь.
"""

# ------------------------------------------------------------------
# read_associations
# ------------------------------------------------------------------

def test_read_associations_valid_file(tmp_path):
    """Чтение корректного файла с несколькими типами."""
    content = (
        "[Default Applications]\n"
        "text/plain=gedit.desktop\n"
        "image/png=gimp.desktop\n"
        "application/pdf=evince.desktop\n"
    )
    file_path = tmp_path / "mimeapps.list"
    file_path.write_text(content, encoding="utf-8")

    result = read_associations(file_path)
    assert result == {
        "text/plain": "gedit.desktop",
        "image/png": "gimp.desktop",
        "application/pdf": "evince.desktop",
    }


def test_read_associations_missing_section(tmp_path):
    """Файл без секции [Default Applications] — пустой словарь."""
    content = "[Added Associations]\ntext/plain=gedit.desktop;\n"
    file_path = tmp_path / "mimeapps.list"
    file_path.write_text(content, encoding="utf-8")

    assert read_associations(file_path) == {}


def test_read_associations_empty_file(tmp_path):
    """Пустой файл — пустой словарь."""
    file_path = tmp_path / "mimeapps.list"
    file_path.write_text("", encoding="utf-8")

    assert read_associations(file_path) == {}


def test_read_associations_nonexistent_file(tmp_path):
    """Несуществующий файл — пустой словарь (без исключения)."""
    file_path = tmp_path / "does_not_exist.list"
    assert read_associations(file_path) == {}


# ------------------------------------------------------------------
# merge_associations
# ------------------------------------------------------------------

def test_merge_associations_different_keys():
    """Разные ключи — объединяются в один словарь."""
    base = {"text/plain": "gedit.desktop"}
    override = {"image/png": "gimp.desktop"}

    assert merge_associations(base, override) == {
        "text/plain": "gedit.desktop",
        "image/png": "gimp.desktop",
    }


def test_merge_associations_same_key_override_wins():
    """При совпадении ключей значение из override побеждает."""
    base = {"text/plain": "gedit.desktop"}
    override = {"text/plain": "code.desktop"}

    assert merge_associations(base, override) == {"text/plain": "code.desktop"}


@pytest.mark.parametrize(
    "base, override, expected",
    [
        ({}, {"text/plain": "gedit.desktop"}, {"text/plain": "gedit.desktop"}),
        ({"text/plain": "gedit.desktop"}, {}, {"text/plain": "gedit.desktop"}),
        ({}, {}, {}),
    ],
)
def test_merge_associations_empty_inputs(base, override, expected):
    """Пустые входные словари (один или оба)."""
    assert merge_associations(base, override) == expected


def test_merge_associations_does_not_mutate_base():
    """merge_associations не изменяет исходный base."""
    base = {"text/plain": "gedit.desktop"}
    override = {"text/plain": "code.desktop", "image/png": "gimp.desktop"}
    base_copy = dict(base)

    merge_associations(base, override)
    assert base == base_copy


# ------------------------------------------------------------------
# write_associations
# ------------------------------------------------------------------

def test_write_associations_creates_file(tmp_path):
    """Запись непустого словаря — файл создаётся, содержимое читается обратно."""
    associations = {
        "text/plain": "code.desktop",
        "image/png": "gimp.desktop",
    }
    file_path = tmp_path / "mimeapps.list"

    write_associations(associations, file_path)

    assert file_path.exists()
    assert read_associations(file_path) == associations


def test_write_associations_empty_dict(tmp_path):
    """Запись пустого словаря — файл создаётся, ассоциаций нет."""
    file_path = tmp_path / "mimeapps.list"

    write_associations({}, file_path)

    assert file_path.exists()
    assert read_associations(file_path) == {}


def test_write_associations_overwrites_existing(tmp_path):
    """Запись поверх существующего файла полностью затирает старое содержимое."""
    file_path = tmp_path / "mimeapps.list"
    file_path.write_text(
        "[Default Applications]\ntext/plain=old.desktop\n",
        encoding="utf-8",
    )

    new_associations = {"image/png": "gimp.desktop"}
    write_associations(new_associations, file_path)

    result = read_associations(file_path)
    assert result == new_associations
    assert "old.desktop" not in file_path.read_text(encoding="utf-8")


def test_write_associations_roundtrip(tmp_path):
    """write → read возвращает исходный словарь (roundtrip)."""
    associations = {
        "application/pdf": "evince.desktop",
        "video/mp4": "vlc.desktop",
        "text/plain": "code.desktop",
    }
    file_path = tmp_path / "mimeapps.list"

    write_associations(associations, file_path)
    assert read_associations(file_path) == associations
