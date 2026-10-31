```
# 1
"""MOCS Notes —— 一個「有洞」的筆記服務（教學用，故意不安全）

三個洞，三條路，三條 flag：
  1. /download?file=../flag1.txt     路徑穿越（最簡單）        → /srv/flag1.txt
  2. /login  admin' --                SQL 注入繞過登入 → /admin → /srv/flag3.txt
  3. /hello?name={{7*7}}              模板注入（最難）          → /srv/flag2.txt

flag 由 checker 每輪寫進 /srv/flag1.txt、flag2.txt、flag3.txt；
每條路各拿到一條，三條都拿到才是滿分。
"""


# 2、
import os
import sqlite3

from flask import Flask, request, render_template_string, session, redirect

app = Flask(__name__)
app.secret_key = "mocs-lab-a-not-a-real-secret"

DATA_DIR = os.environ.get("DATA_DIR", "/srv")
FLAG1 = os.path.join(DATA_DIR, "flag1.txt")   # 路徑穿越
FLAG2 = os.path.join(DATA_DIR, "flag2.txt")   # 模板注入
FLAG3 = os.path.join(DATA_DIR, "flag3.txt")   # SQL 注入 → /admin
NOTES_DIR = os.path.join(DATA_DIR, "notes")
DB_PATH = os.path.join(DATA_DIR, "app.db")


def db():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.row_factory = sqlite3.Row
    return conn


def init():
    os.makedirs(NOTES_DIR, exist_ok=True)
    for path in (FLAG1, FLAG2, FLAG3):
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("no-flag-yet\n")
    with open(os.path.join(NOTES_DIR, "welcome.txt"), "w") as f:
        f.write("welcome to MOCS Notes\n")
    conn = db()
    conn.executescript(
    """
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    );
    CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT NOT NULL,
        body TEXT NOT NULL
    );
    """
)
conn.execute("INSERT OR IGNORE INTO users VALUES('demo','demo','user')")
conn.execute("INSERT OR IGNORE INTO users VALUES('admin','admin123','admin')")
conn.execute("INSERT OR IGNORE INTO notes(owner, body) VALUES('demo','買牛奶')")
conn.commit()
conn.close()


# 3、
@app.get("/health")
def health():
return "ok"


@app.get("/")
def index():
user = session.get("user")
rows = []
if user:
    conn = db()
    rows = conn.execute("SELECT body FROM notes WHERE owner=?", (user,)).fetchall()
    conn.close()
out = ["<h1>MOCS Notes</h1>", f"<p>目前使用者：{user or '未登入'}</p>", "<ul>"]
out += [f"<li>{r['body']}</li>" for r in rows]
out.append("</ul><p><a href='/download?file=welcome.txt'>下載 welcome.txt</a></p>")
return "".join(out)

@app.post("/login")
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    # 洞 2：字串拼接（故意）
    query = f"SELECT username FROM users WHERE username='{username}' AND password='{password}'"
    try:
        row = db().execute(query).fetchone()
    except sqlite3.Error as exc:
        return f"db error: {exc}", 500
    if row:
        session["user"] = row["username"]
        return redirect("/")
    return "bad login", 401


@app.get("/admin")
def admin():
    if session.get("user") != "admin":
        return "forbidden", 403
    try:
        with open(FLAG3) as f:
            backup = f.read().strip()
    except OSError:
        backup = "(empty)"
    # 洞 2 的收尾：登入成 admin 就能看到這頁
    return f"<h1>admin console</h1><p>最近一次備份：</p><pre>{backup}</pre>"


@app.get("/download")
def download():
    name = request.args.get("file", "welcome.txt")
    # 洞 1：沒有把 ../ 擋掉（故意）
    path = os.path.join(NOTES_DIR, name)
    try:
        with open(path, "rb") as f:
            body = f.read()
    except OSError:
        return "not found", 404
    return body, 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.get("/hello")
def hello():
    name = request.args.get("name", "guest")
    # 洞 3：把使用者輸入直接拼進模板（故意）
    return render_template_string("<h1>Hello " + name + "</h1>")


init()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True)
```



# `{{7*7}}` :模板引擎(Template Engine)的语法格式;如果页面返回了49而不是原样输出`{{7*7}}`说明输入没有被过滤,被服务器当成代码执行
## 用于测试SSTI漏洞的探测Payload
## SSTI(Server-Side Template Injection) :服务端模板注入

# sed(Stream Editor,流编辑器) :Linux文本处理器
## `sed -n` 
### -n(no auto-print) :安静模式;取消sed默认的打印输出
## `sed -n '1p' 文件` :查看文件的某行
### `sed -n '5p' file.txt`(查看文件的第5行)
## `sed -n '1,2p' 文件` :查看文件的某几行 
### `sed -n 2,5p file.txt`(查看文件的2到5行) 等同于 `head -n 5 file.txt | tail -n 4`
## `sed -n '/error/p' 文件` :查看包含特定关键字的行(相当于带行号的grep)
## `sed -n '/error/=' file.txt`或者`sed -n '/error/{=;p} file.txt'` :显示行号