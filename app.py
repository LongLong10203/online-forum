from flask import Flask, request, redirect, url_for, render_template
<<<<<<< HEAD
import sqlite3


app = Flask(__name__)
=======
from prisma import Prisma


app = Flask(__name__)
prisma = Prisma()
>>>>>>> 4b8b9a1 (init)


@app.route("/")
def index():
    return render_template("index.html")


<<<<<<< HEAD
@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
=======
async def create_post(title, content):
    await prisma.connect()

    post = await prisma.post.create(
        data={
            "title": title,
            "content": content
        }
    )

    await prisma.disconnect()


@app.route("/new", methods=["GET", "POST"])
async def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        await create_post(title, content)
>>>>>>> 4b8b9a1 (init)
        return redirect(url_for("home"))
    else:
        return render_template("new_post.html")


<<<<<<< HEAD
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


=======
async def create_answer(post_id, content):
    await prisma.connect()

    answer = await prisma.answer.create(
        data={
            "content": content,
            "post": {
                "connect": {"id": post_id}
            }
        }
    )

    await prisma.disconnect()


async def get_all_posts():
    await prisma.connect()

    posts = await prisma.post.find_many(
        include={"answers": True}  # Including answers from the post
    )

    await prisma.disconnect()

    return posts


@app.route("/home", methods=["GET", "POST"])
async def home():
    if request.method == "POST":
        post_id = int(request.form["post_id"])
        answer_content = request.form["content"]
        await create_answer(post_id, answer_content)
        return redirect(url_for("home"))

    posts = await get_all_posts()

    return render_template("home.html", posts=posts)



>>>>>>> 4b8b9a1 (init)
if __name__ == "__main__":
    app.run(debug=True)