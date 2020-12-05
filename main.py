from flask import Flask, redirect, url_for, render_template, request, flash
import prettytable

# import requests
# import json
import flask
import sqlite3

app = Flask(__name__)
# print(dir(flask))
app.secret_key = "the random string"
current = []
done = {}


@app.route("/")
def home():

    return render_template("main.html")


@app.route("/shubh/information/secret")
def all():
    sqliteConnection = sqlite3.connect("data.db")
    cursor = sqliteConnection.cursor()
    cursor.execute("select * from data;")
    a = prettytable.from_db_cursor(cursor)
    return render_template(
        "table.html", tbl=a.get_html_string(attributes={"class": "foo"})
    )


# @app.route("/hello/<name>")
# def hello_world(name):
#     return f"Hello World {name}"


# @app.route("/weather", methods=["POST", "GET"])
# def weather():
#     city = request.form["city"]
#     url = f"http://api.openweathermap.org/data/2.5/weather?appid=be5af63b2dadbf2170846910fb5dec85&q={city}"
#     res = requests.get(url)
#     res = res.json()
#     if res["cod"] != "404":
#         print(f'{str(round(res["main"]["temp"] - 273, 2))}°C')
#         return f'{str(round(res["main"]["temp"] - 273, 2))}°C'


# @app.route("/go/<alias>")
# def first(alias):
#     sqliteConnection = sqlite3.connect("data.db")
#     cursor = sqliteConnection.cursor()
#     cursor.execute(f"select * from data;")
#     b = cursor.fetchall()
#     print(b)
#     cursor.execute(f"select url from data where alias='{alias}';")
#     b = cursor.fetchall()
#     print(type(b))
#     print(b)
#     if b:
#         return redirect(b[0][0])
#     else:
#         return url_for("home")
@app.route("/<var>")
def start(var):
    global current, done
    if var in current:
        return redirect("/")
    if var in done.keys():
        return redirect(done[var])
    sqliteConnection = sqlite3.connect("data.db")
    cursor = sqliteConnection.cursor()
    # alias=alias.replace(' ','')
    var = var.lower()
    cursor.execute(f"select url from data where alias='{var}';")
    c = cursor.fetchall()
    # print(c)
    if c:
        print(c[0])
        return redirect(c[0][0])
    else:
        # print("yoyo")
        current.append(var)
        return redirect("/")
    # c = [i for i in cursor.fetchall()]


@app.route("/short/", methods=["POST"])
def short():
    global current, done
    sqliteConnection = sqlite3.connect("data.db")
    cursor = sqliteConnection.cursor()
    u = request.form
    url = u["url"]
    alias = u["alias"]
    alias = alias.replace(" ", "")
    alias = alias.lower()
    cursor.execute("select alias from data;")
    c = [i[0] for i in cursor.fetchall()]
    if alias in c:
        flash("Alias Already Exists")
    else:
        cursor.execute(f'insert into data values("{alias}","{url}");')
        done[alias] = url
        sqliteConnection.commit()
        if alias in current:
            current.remove(alias)
        flash(f"Success!")
        flash(f"visit at - \nsmittal.tech/{alias}")
    return redirect("/")


# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if request.method == "POST":
#         user = request.form["nm"]
#         return redirect(url_for("user", usr=user))
#     else:
#         return render_template("login.html")

if __name__ == "__main__":
    app.run()