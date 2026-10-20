from flask import Flask, request, redirect
import subprocess
import os
import atexit

app = Flask(__name__)

NOTES = {
    1: {"title": "Секретный пароль", "text": "1234"}
}
next_id = [2]


def log_title(title):
    with open("notes_log.txt", "a", encoding="cp866") as f:
        f.write(title + "\n")


def clear_log():
    if os.path.exists("notes_log.txt"):
        os.remove("notes_log.txt")


atexit.register(clear_log)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "")
        ex = any(title.lower() == n["title"].lower() for n in NOTES.values())
        if title != "" and not ex:
            nid = next_id[0]
            next_id[0] += 1
            NOTES[nid] = {"title": title, "text": ""}
            log_title(title)

    links = ''
    for nid, n in NOTES.items():
        if nid > 1:
            links += f'<li><a href="/note?id={nid}">{n["title"]}</a></li>'

    return (f"""
    <h2>Личные заметки</h2>
    <form method="post">
        Название: <input name="title"><br>
        <button type="submit">Создать</button>
    </form>
    <h3>Поиск по заметкам:</h3>
    <form method="get" action="/search">
        <input name="q"><button type="submit">Найти</button>
    </form>
    <h3>Мои заметки:</h3>
    <ul>{links}</ul>
    """)


@app.route("/search")
def search():
    q = request.args.get("q", "")

    note_block = ""
    for nid, n in NOTES.items():
        if nid != 1 and n["title"] == q:
            note_block = f'<h3><a href="/note?id={nid}">"Ссылка на заметку"</a></h3>'
            break

    raw = subprocess.run(f'findstr "{q}" notes_log.txt', shell=True, capture_output=True).stdout
    result = raw.decode("cp866", errors="replace")

    return (f"""
    <h3>Результаты поиска:</h3>
    <pre>{result}</pre>
    {note_block}
    <a href='/'>Назад</a>
    """)


@app.route("/note", methods=["GET", "POST"])
def note():
    note_id = int(request.args.get("id", ""))
    if note_id not in NOTES:
        return redirect("/")

    if request.method == "POST":
        NOTES[note_id]["text"] = request.form.get("text", "")

    n = NOTES[note_id]
    return f"""
    <h2>{n['title']}</h2>
    <form method="post">
        <textarea name="text" onchange="this.form.submit()">{n['text']}</textarea>
    </form>
    <a href="/delete?id={note_id}">Удалить заметку</a><br>
    <a href="/">Назад</a>
    """


@app.route("/delete")
def delete():
    note_id = int(request.args.get("id", ""))
    NOTES.pop(note_id, None)
    return redirect("/")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
