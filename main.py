from flask import Flask, redirect, url_for, render_template, request, flash, session
import prettytable

# import requests
# import json
import flask
import sqlite3
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)
# print(dir(flask))
app.secret_key = "the random string"
current = []
done = {}


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


@app.route("/")
def home():

    return render_template("main.html")


@app.route("/shubh/information/<var>")
def all(var):
    global done
    sqliteConnection = sqlite3.connect("data.db")
    cursor = sqliteConnection.cursor()
    if var == "secret":
        cursor.execute("select * from data;")
        a = prettytable.from_db_cursor(cursor)
        return render_template(
            "table.html", tbl=a.get_html_string(attributes={"class": "foo"})
        )
    else:
        try:
            cursor.execute(f'delete from data where alias="{var}";')
            sqliteConnection.commit()
            flash("Done Bro!")
            if var in done.keys():
                current.pop(var)
        except:
            pass
        return redirect("/")


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


@app.route("/short/", methods=["GET"])
def short():
    if request.method == "GET":
        url = request.args.get("url")
        alias = request.args.get("alias")
    else:
        print("POST RECEIVED LOL")
        return redirect("/")

    global current, done
    sqliteConnection = sqlite3.connect("data.db")
    cursor = sqliteConnection.cursor()

    alias = alias.replace(" ", "")
    alias = alias.lower()
    cursor.execute("select alias from data;")
    c = [i[0] for i in cursor.fetchall()]
    if alias in c or alias == "short":
        flash("Alias Already Exists")
    elif bool(
        list(
            filter(
                lambda x: x
                in [
                    "@",
                    "!",
                    "#",
                    "$",
                    "%",
                    "^",
                    "&",
                    "*",
                    "(",
                    ")",
                    "'",
                    '"',
                    ".",
                    ",",
                    "/",
                    "\\",
                    "; ",
                    " ~ ",
                    " + ",
                    " - ",
                ],
                [*alias],
            )
        )
    ):
        flash("Invalid Alias")
        return redirect("/")
    else:
        cursor.execute(f'insert into data values("{alias}","{url}");')
        done[alias] = url
        sqliteConnection.commit()
        if alias in current:
            current.remove(alias)
        # flash(f"Success!")
        # flash(f"visit at - \nsmittal.tech/{alias}"
        img = qrcode.make(f"smittal.tech/{alias}")

        buffered = BytesIO()
        img.save(buffered, format="png")
        img_str = base64.b64encode(buffered.getvalue())
        session["b64"] = img_str
        session["alias"] = alias
        return redirect("/final")


@app.route("/final")
def login():
    alias = session.get("alias", None)
    img_str = session.get("b64", None)
    return render_template("final.html", link=f"smittal.tech/{alias}", data=img_str)


if __name__ == "__main__":
    app.run(ssl_context=("cert.crt", "key.key"))
