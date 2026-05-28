# Лабораторная работа 1. Ряд Фибоначчи

## Описание

Проект выполнен по заданию на реализацию итераторов и сопрограммы для работы с рядом Фибоначчи.

В работе реализованы:

1. Упрощённый итератор чисел Фибоначчи через метод `__getitem__`.
2. Обычный итератор чисел Фибоначчи через методы `__iter__` и `__next__`.
3. Итератор `FibonacchiLst`, который проходит по переданному списку и возвращает только те значения, которые входят в ряд Фибоначчи.
4. Упрощённая версия фильтрующего итератора `FibonacchiLstGetItem` через `__getitem__`.
5. Сопрограмма `my_genn`, которая получает число `n` через `send` и возвращает список из первых `n` чисел Фибоначчи.
6. Набор тестов на `unittest`.

## Структура проекта

```text
.
├── fibonacci.py        # основная логика
├── main.py             # пример запуска
├── test_fibonacci.py   # тесты unittest
├── requirements.txt    # зависимости проекта
├── .gitignore
└── README.md
```

## Примеры работы

### Упрощённый итератор

```python
from fibonacci import FibonacciGetItem

print(list(FibonacciGetItem(6)))
# [0, 1, 1, 2, 3, 5]
```

### Обычный итератор

```python
from fibonacci import FibonacciIterator

print(list(FibonacciIterator(6)))
# [0, 1, 1, 2, 3, 5]
```

### Фильтрация чисел Фибоначчи из списка

```python
from fibonacci import FibonacchiLst

lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
print(list(FibonacchiLst(lst)))
# [0, 1, 2, 3, 5, 8, 1]
```

### Сопрограмма

```python
from fibonacci import my_genn

gen = my_genn()
print(gen.send(3))
# [0, 1, 1]

print(gen.send(5))
# [0, 1, 1, 2, 3]
```

## Запуск программы

```bash
python main.py
```

## Запуск тестов

```bash
python -m unittest -v
```

## Требования задания

В коде используются:

- документация к функциям и классам в формате docstring;
- аннотации типов;
- тесты на `unittest`;
- два варианта итераторов;
- сопрограмма для генерации списка чисел Фибоначчи.
