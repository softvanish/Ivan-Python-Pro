# Python Pro Project Ivan

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/user", methods=["GET", "POST"])
def user_handler():
    if request.method == "GET":
        return "GET"
    else:
        return "POST"


@app.route("/login", methods=["GET", "POST"])
def get_login():
    if request.method == "GET":
        return "GET"
    else:
        return "POST"


@app.route("/register", methods=["GET", "POST"])
def get_register():
    if request.method == "GET":
        return "GET"
    else:
        return "POST"


@app.route("/category", methods=["GET", "POST"])
def get_category():
    if request.method == "GET":
        return "GET"
    else:
        return "POST"


@app.route("/category/<category_id>", methods=["GET", "PATCH", "DELETE"])
def get_category(category_id):
    if request.method == "GET":
        return f"GET, {category_id}"
    elif request.method == "PATCH":
        return "PATCH"
    else:
        return "DELETE"


@app.route("/income", methods=["GET", "POST"])
def get_income():
    if request.method == "GET":
        return "GET"
    else:
        return "POST"


@app.route("/income/<income_id>", methods=["GET", "POST"])
def get_income(income_id):
    if



if __name__ == "__main__":
    app.run()
