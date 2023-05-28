from flask import Flask, make_response, request, render_template
from subprocess import run
from re import match

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/screen/<path:url>")
def screen(url):
    output = {}

    regex = "^http:\/\/[a-zA-Z]{0,63}\.saas\.esaip-cyber\.com$"
    if match(regex, url):
        image = run(["node", "/usr/app/screenshot/bot.js", url], capture_output=True)
        output["data"] = image.stdout.decode()
    else:
        output["error"] = f"The URL must match {regex} !"

    response = make_response(output, 200)
    response.mimetype = "application/json"
    return response


@app.route("/flag")
def flag():
    if not request.environ["REMOTE_ADDR"] == "127.0.0.1":
        return "<h1>Unauthorized</h1>", 403

    response = make_response("ECTF{SuBD0m41n_T4k3_0v3R_1S_R34LY_Str0nG}", 200)
    response.mimetype = "application/json"
    return response


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
