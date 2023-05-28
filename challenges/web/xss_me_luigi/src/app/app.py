from flask import Flask, make_response, request, render_template
from utils.security import sanitize_html
from subprocess import run
from re import match


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def index():
    html = request.args.get("html") or ""
    return render_template("index.html", html=sanitize_html(html))


@app.route("/report", methods=["GET", "POST"])
def report():

    if request.method == "GET":
        return render_template("report.html")

    elif request.method == "POST":
        url = request.form.get("url")
        if not match("^http(s)?://.*", url):
            return render_template("report.html", msg="The URL must match ^http(?)://.* !")

        else:
            run(["node", "/usr/app/bot/bot.js", url])
            return render_template("report.html", msg="Your request has been sent to an administrator!")


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
