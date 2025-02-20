from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

POSTS_FILE = "posts.json"


def load_posts():
    """Load posts from the JSON file."""
    if not os.path.exists(POSTS_FILE):
        return []

    try:
        with open(POSTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_posts(posts):
    """Save the list of posts to the JSON file."""
    with open(POSTS_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4)


def get_next_id(posts):
    """Return the next available post ID (incremental)."""
    return max((post["id"] for post in posts), default=0) + 1


@app.route("/")
def index():
    """Render the homepage displaying all blog posts."""
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Add a new blog post."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()

        if title and author and content:
            blog_posts = load_posts()
            new_post = {
                "id": get_next_id(blog_posts),
                "title": title,
                "author": author,
                "content": content,
                "likes": 0
            }
            blog_posts.append(new_post)
            save_posts(blog_posts)
            flash("Post successfully added!", "success")
        else:
            flash("All fields are required!", "danger")

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    """Delete a blog post by its ID."""
    blog_posts = load_posts()
    updated_posts = [post for post in blog_posts if post["id"] != post_id]

    if len(updated_posts) == len(blog_posts):
        flash("Post not found!", "danger")
    else:
        save_posts(updated_posts)
        flash("Post successfully deleted!", "success")

    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """Update an existing blog post."""
    blog_posts = load_posts()
    post = next((p for p in blog_posts if p["id"] == post_id), None)

    if post is None:
        flash("Post not found!", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        post["title"] = request.form["title"].strip()
        post["author"] = request.form["author"].strip()
        post["content"] = request.form["content"].strip()
        save_posts(blog_posts)
        flash("Post successfully updated!", "success")
        return redirect(url_for("index"))

    return render_template("update.html", post=post)


@app.route("/like/<int:post_id>")
def like(post_id):
    """Increase the like count for a specific blog post."""
    blog_posts = load_posts()
    post = next((p for p in blog_posts if p["id"] == post_id), None)

    if post:
        post["likes"] += 1
        save_posts(blog_posts)
        flash("You liked a post!", "success")
    else:
        flash("Post not found!", "danger")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
