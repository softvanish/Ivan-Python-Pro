# Python Pro Project Ivan

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/user", methods=["GET", "DELETE"])
def user_handler():
    if request.method == "GET":
        return "GET"
    else:
        return "DELETE"


@app.route("/login", methods=["GET", "POST"])
def get_login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        return f"POST {username}, {password}"


@app.route("/register", methods=["GET", "POST"])
def get_register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        return f"POST {username}, {password}"


@app.route("/category", methods=["GET", "POST"])
def get_all_category():
    if request.method == "GET":
        return "GET"
    else:
        return "POST"


@app.route("/category/<category_id>", methods=["GET", "POST"])
def get_category(category_id):
    if request.method == "GET":
        return render_template("one_category.html")
    else:
        return "edit category"


@app.route("/category/<category_id>/delete", methods=["GET"])
def delete_category(category_id):
    return f"Delete_category {category_id}"


@app.route("/income", methods=["GET", "POST"])
def get_all_income():
    if request.method == "GET":
        return "GET"
    else:
        return "POST"


@app.route("/income/<income_id>", methods=["GET", "POST"])
def get_income(income_id):
    if request.method == "GET":
        return f"GET {income_id}"
    else:
        return "POST"


@app.route("/spend", methods=["GET", "POST"])
def get_all_spend():
    if request.method == "GET":
        return "GET"
    else:
        return "POST"


@app.route("/spend/spend_id", methods=["GET", "POST"])
def get_spend(spend_id):
    if request.method == f"GET {spend_id}":
        return "GET"
    else:
        return "POST"


if __name__ == "__main__":
    app.run()
