# Python Pro Project Ivan
import sqlite3

from flask import Flask, request, render_template, session, redirect

app = Flask(__name__)

app.secret_key = 'asdfueqwfgvh129345'

SPEND = 1
INCOME = 2


class DBwrapper:

    def insert(self, table, data):

        with Database('financial_tracker.db') as cursor:
            cursor.execute(f'INSERT INTO {table} ({", ".join(data.keys())}) VALUES ({", ".join(["?"] * len(data))})', tuple(data.values()))

    def select(self, table, params):

        with Database('financial_tracker.db') as cursor:
            if params:
                result_params = []

                for key, value in params.items():
                    if isinstance(value, list):
                        result_params.append(f"{key} IN ({', '.join(map(str, value))})")
                    else:
                        if isinstance(value, str):
                            result_params.append(f"{key} = '{value}'")
                        else:
                            result_params.append(f"{key} = {value}")

                    result_where = ' AND '.join(result_params)

                    cursor.execute(f'SELECT * FROM {table} WHERE {result_where}')
            else:
                cursor.execute(f'SELECT * FROM {table}')
            return cursor.fetchall()


class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
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
        db = DBwrapper()
        data = db.select('user', {'email': email, 'password': password})

        if data:
            session['user_id'] = data[0]['id']

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

        db = DBwrapper()
        db.insert('user', {'name': use_name, 'surname': sur_name, 'password': password, 'email': email})

        return "User registered"


@app.route("/category", methods=["GET", "POST"])
def get_all_category():
    if 'user_id' in session:
        if request.method == 'GET':
            db = DBwrapper()
            res = db.select('category', {'owner': [session['user_id'], 1]})
            return render_template("category-list.html", categories=res)
        else:
            category_name = request.form["category_name"]
            category_owner = session["user_id"]
            db = DBwrapper()
            db.insert("category", {'name': category_name, 'owner': category_owner})
            return redirect('/category')


@app.route("/category/<category_id>", methods=["GET", "POST"])
def get_category(category_id):
    if 'user_id' in session:
        if request.method == 'GET':
            db = DBwrapper()
            current_category = db.select('category', {'id': int(category_id)})[0]
            res = db.select('transactions', {'category': int(category_id), 'owner': session['user_id']})
            return render_template('one_category.html', transactions=res, category=current_category)
        else:
            return "bla bla bla"


@app.route("/category/<category_id>/delete", methods=["GET"])
def delete_category(category_id):
    return f"Delete_category {category_id}"


@app.route("/income", methods=["GET", "POST"])
def get_all_income():
    if 'user_id' not in session:
        return redirect('/login')

    db = DBwrapper()

    if request.method == "GET":
        res = db.select('transactions', {'owner': session['user_id'], 'type': INCOME})

        with Database('financial_tracker.db') as cursor:
            cursor.execute("SELECT id, name FROM category")
            cat_res = cursor.fetchall()
        return render_template('dashboard.html', transactions=res, categories=cat_res)

    else:
        db.insert('transactions', {
            'description': request.form['description'],
            'amount': request.form['amount'],
            'owner': request.form['owner'],
            'category': request.form['category'],
            'type': INCOME,
            'date': request.form['date']
        })
        return redirect('/income')


@app.route("/income/<income_id>", methods=["GET", "POST"])
def get_income(income_id):
    if request.method == "GET":
        return f"GET {income_id}"
    else:
        return "POST"


@app.route("/spend", methods=["GET", "POST"])
def get_all_spend():
    if 'user_id' not in session:
        return redirect('/login')

    db = DBwrapper()

    if request.method == "GET":
        res = db.select('transactions', {'owner': session['user_id'], 'type': SPEND})

        with Database('financial_tracker.db') as cursor:
            cursor.execute("SELECT id, name FROM category")
            cat_res = cursor.fetchall()
        return render_template('dashboard.html', transactions=res, categories=cat_res)

    else:
        db.insert('transactions', {
            'description': request.form['description'],
            'amount': request.form['amount'],
            'owner': request.form['owner'],
            'category': request.form['category'],
            'type': INCOME,
            'date': request.form['date']
        })
        return redirect('/spend')


@app.route("/spend/spend_id", methods=["GET", "POST"])
def get_spend(spend_id):
    if request.method == f"GET {spend_id}":
        return "GET"
    else:
        return "POST"


if __name__ == "__main__":
    app.run()
