# Python Pro Project Ivan
import sqlite3

from flask import Flask, request, render_template, session, redirect

app = Flask(__name__)

app.secret_key = 'asdfueqwfgvh129345'

SPEND = 1
INCOME = 2



class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


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
        email = request.form["email"]
        password = request.form["password"]
        with Database("financial_tracker.db") as cursor:
            result = cursor.execute(f"SELECT id FROM user where email = '{email}' and password = '{password}'")
            data = result.fetchone()
        if data:
            session['user_id'] = data[0]
            return "Correct"
        return "Wrong"


@app.route("/register", methods=["GET", "POST"])
def get_register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        use_name = request.form["name"]
        sur_name = request.form["surname"]
        password = request.form["password"]
        email = request.form["email"]

        with Database("financial_tracker.db") as cursor:
            cursor.execute(f"INSERT INTO user (name, surname, password, email) VALUES ('{use_name}', '{sur_name}', '{password}', '{email}')")

        return "User registered"


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
    if 'user_id' in session:
       if request.method == "GET":
                with Database("financial_tracker.db") as cursor:
                    data = cursor.execute(
                        f"SELECT * FROM 'transaction' where owner = {session['user_id']} and type = {INCOME}")
                    res = data.fetchall()

                return render_template('dashboard.html', transactions=res)
       else:
           with Database("financial_tracker.db") as cursor:

               description = request.form['description']
               amount = request.form['amount']
               owner = request.form['owner']
               category = request.form['category']
               type = INCOME
               date = request.form['date']
               cursor.execute(f"INSERT INTO 'transiction' (description, amount, owner, category, type, date) VALUES ('{transaction_description}', '{transaction_amount}')")
           return redirect('/income')

    else:
        return redirect('/login')


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
