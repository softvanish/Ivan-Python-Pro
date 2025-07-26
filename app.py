# Python Pro Project Ivan

from flask import Flask

app = Flask(__name__)


@app.route("/user", methods=["GET", "POST"])
def user_handler():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
