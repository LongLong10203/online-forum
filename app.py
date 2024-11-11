from flask import Flask, request, redirect, url_for, render_template
import sqlite3


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
        return redirect(url_for("home"))
    else:
        return render_template("new_post.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        post_id = int(request.form["post_id"])
        answer_content = request.form["content"]
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO answers (post_id, content) VALUES (?, ?)", (post_id, answer_content))
            conn.commit()
        return redirect(url_for("home"))

    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM posts")
        posts = [dict(title=row[1], content=row[2], id=row[0], answers=[]) for row in c.fetchall()]
        c.execute("SELECT * FROM answers")
        answers = [dict(post_id=row[1], content=row[2], id=row[0]) for row in c.fetchall()]

    # i have no idea what codedium is doing here
    answers_by_post_id = {}
    for answer in answers:
        if answer["post_id"] not in answers_by_post_id:
            answers_by_post_id[answer["post_id"]] = []
        answers_by_post_id[answer["post_id"]].append(answer)

    for post in posts:
        post["answers"] = answers_by_post_id.get(post["id"], [])
    
    return render_template("home.html", posts=posts)


if __name__ == "__main__":
    app.run(debug=True)