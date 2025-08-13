# Python Pro Project Ivan
import sqlite3
import database
import models
import datetime
from datetime import datetime
from sqlalchemy import select
from flask import Flask, request, render_template, session, redirect
from database import db_session, init_db

app = Flask(__name__)

app.secret_key = 'asdfueqwfgvh129345'

SPEND = 1
INCOME = 2


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
        init_db()
        data = list(db_session.execute(select(models.User).filter_by(email=email, password=password)).scalars())

        if data:
            session['user_id'] = data[0].id

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

        init_db()
        new_user = models.User(name=use_name, surname=sur_name, password=password, email=email)
        db_session.add(new_user)
        db_session.commit()

        return "User registered"


@app.route("/category", methods=["GET", "POST"])
def get_all_category():
    if 'user_id' in session:
        if request.method == 'GET':
            init_db()
            categories = list(db_session.execute(select(models.Category).filter_by(owner=session['user_id'])).scalars())
            sys_categories = list(db_session.execute(select(models.Category).filter_by(owner=1)).scalars())
            return render_template("category-list.html", categories=categories+sys_categories)
        else:
            category_name = request.form["category_name"]
            category_owner = session["user_id"]
            new_category = models.Category(name=category_name, owner=category_owner)
            db_session.add(new_category)
            db_session.commit()
            return redirect('/category')


@app.route("/category/<category_id>", methods=["GET", "POST"])
def get_category(category_id):
    if 'user_id' in session:
        if request.method == 'GET':
            init_db()
            current_category = db_session.scalar(select(models.Category).filter_by(id=int(category_id)))
            res = db_session.execute(select(models.Transaction).filter_by(category=int(category_id), owner=session['user_id'])).scalars
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
    if request.method == "GET":
        init_db()
        res = list(db_session.execute(select(models.Transaction).filter_by(owner=session['user_id'], type='income')).scalars())
        cat_res = list(db_session.execute(select(models.Category.id, models.Category.name)))
        return render_template('dashboard.html', transactions=res, categories=cat_res)

    else:
        init_db()
        new_trans = models.Transaction(description=request.form['description'], amount=request.form['amount'],
                                       owner=session['user_id'], category=request.form['category'],
                                       type='income', date=datetime.strptime(request.form['date'], "%Y-%m-%d"))
        db_session.add(new_trans)
        db_session.commit()
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
    if request.method == "GET":
        init_db()
        res = list(
            db_session.execute(select(models.Transaction).filter_by(owner=session['user_id'], type='spend')).scalars())
        cat_res = list(db_session.execute(select(models.Category.id, models.Category.name)))
        return render_template('dashboard.html', transactions=res, categories=cat_res)

    else:
        init_db()
        new_trans = models.Transaction(description=request.form['description'], amount=request.form['amount'],
                                       owner=session['user_id'], category=request.form['category'],
                                       type='spend', date=datetime.strptime(request.form['date'], "%Y-%m-%d"))
        db_session.add(new_trans)
        db_session.commit()
        return redirect('/spend')


@app.route("/spend/spend_id", methods=["GET", "POST"])
def get_spend(spend_id):
    if request.method == f"GET {spend_id}":
        return "GET"
    else:
        return "POST"


if __name__ == "__main__":
    app.run()
