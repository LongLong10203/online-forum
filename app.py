from flask import Flask, request, redirect, url_for, render_template
from prisma import Prisma


app = Flask(__name__)
prisma = Prisma()


@app.route("/")
def index():
    return render_template("index.html")


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
        return redirect(url_for("home"))
    else:
        return render_template("new_post.html")


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


if __name__ == "__main__":
    app.run(debug=True)