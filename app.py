from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "dev"  # local dev only (use env var for real apps)

# Starter data (no ghost task key mismatch)
todos = [{"task": "Sample Todo", "done": False}]


def get_theme():
    return session.get("theme", "light")


@app.route("/")
def index():
    return render_template("index.html", todos=todos, theme=get_theme())


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("todo", "").strip()
    if task:
        todos.append({"task": task, "done": False})
    return redirect(url_for("index"))


@app.route("/check/<int:index>", methods=["POST"])
def check(index):
    if 0 <= index < len(todos):
        todos[index]["done"] = not todos[index]["done"]
    return redirect(url_for("index"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    if not (0 <= index < len(todos)):
        return redirect(url_for("index"))

    if request.method == "POST":
        new_task = request.form.get("todo", "").strip()
        if new_task:
            todos[index]["task"] = new_task
        return redirect(url_for("index"))

    return render_template("edit.html", todo=todos[index], index=index, theme=get_theme())


@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(todos):
        todos.pop(index)
    return redirect(url_for("index"))


@app.route("/toggle-theme", methods=["POST"])
def toggle_theme():
    session["theme"] = "dark" if get_theme() == "light" else "light"
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
