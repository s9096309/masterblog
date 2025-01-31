from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

POSTS_FILE: str = "posts.json"


def load_posts() -> list[dict]:
    """Load posts from the JSON file."""
    if not os.path.exists(POSTS_FILE):
        return []

    with open(POSTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_posts(posts: list[dict]) -> None:
    """Save the list of posts to the JSON file."""
    with open(POSTS_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4)


@app.route("/")
def index():
    """Render the homepage displaying all blog posts."""
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Handle adding a new blog post."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()

        if title and author and content:
            blog_posts = load_posts()
            new_post = {
                "id": len(blog_posts) + 1,
                "title": title,
                "author": author,
                "content": content,
                "likes": 0  # Ensure likes field exists
            }
            blog_posts.append(new_post)
            save_posts(blog_posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route('/delete/<int:post_id>')
def delete(post_id: int):
    """Delete a blog post by its ID."""
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post["id"] != post_id]
    save_posts(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id: int):
    """Update an existing blog post."""
    blog_posts = load_posts()
    post = next((p for p in blog_posts if p["id"] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post["title"] = request.form["title"].strip()
        post["author"] = request.form["author"].strip()
        post["content"] = request.form["content"].strip()
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id: int):
    """Increase the like count for a specific blog post."""
    blog_posts = load_posts()
    post = next((p for p in blog_posts if p["id"] == post_id), None)

    if post:
        post["likes"] = post.get("likes", 0) + 1  # Ensure likes field exists
        save_posts(blog_posts)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
