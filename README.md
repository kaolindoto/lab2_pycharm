# Лабораторная работа по ТП: поиск устранение уязвимостей Command Injection и IDOR

> **Дисклеймер**
> Проект создан в учебных целях в рамках курса по информационной безопасности. Приложение запускается только локально (`127.0.0.1`) и не предназначено для продакшена. Код демонстрирует уязвимости исключительно для изучения их природы и способов защиты. Использование материалов против систем без разрешения владельца незаконно.

## Цель

Найти и исправить две уязвимости в учебном Flask-приложении:
Наши уязвимости:
- **Command Injection** в `/search`
- **IDOR** в `/note`

## До исправления

```python
raw = subprocess.run(f'findstr "{q}" notes_log.txt', shell=True, capture_output=True).stdout
```

```python
@app.route("/note", methods=["GET", "POST"])
def note():
    note_id = int(request.args.get("id", ""))
    if note_id not in NOTES:
        return redirect("/")
```

## После исправления

```python
raw = subprocess.run(['findstr', q, 'notes_log.txt'], capture_output=True).stdout
```

```python
@app.route("/note", methods=["GET", "POST"])
def note():
    note_id = int(request.args.get("id", ""))
    if note_id not in NOTES or note_id == 1:
        return redirect("/")
```

## Что изменилось

| Уязвимость | Было | Стало |
|---|---|---|
| Command Injection | `shell=True` + строка с пользовательским вводом | список аргументов, без `shell=True` |
| IDOR | доступ к любой заметке по `id` | доступ к заметке `id=1` закрыт |

## Вывод

Обе уязвимости устранены: команда ОС больше не собирается из пользовательского ввода, а доступ к чужой заметке ограничен проверкой id.
