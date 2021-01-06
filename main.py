from flask import Flask, redirect, url_for, render_template, request, flash, session
import prettytable
from flask_sitemap import Sitemap
import flask
import sqlite3
import qrcode
import base64
from io import BytesIO
import mysql.connector as ms

db = ms.connect(
    host="logs.c7xtjtjv8ph3.ap-south-1.rds.amazonaws.com",
    port=3306,
    user="shubh",
    passwd="shubh2003",
    db="short",
)
db.autocommit = True
cursor = db.cursor()
app = Flask(__name__)
# print(dir(flask))
app.secret_key = "lmao"
current = []
done = {}
app.config["SITEMAP_URL_SCHEME"] = "https"
app.config["SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS"] = True
ext = Sitemap(app=app)


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


@app.route("/")
def home():

    return render_template("main.html")


@app.route("/shubh/information/<var>/")
def all(var):
    global done
    db.ping(reconnect=True, attempts=1, delay=0)
    if var == "secret":
        cursor.execute("select * from data;")
        a = cursor.fetchall()
        a = a[-1:1:-1]
        print(a)
        return render_template("table2.html", data=a)
    else:

        try:
            cursor.execute(f'delete from data where alias="{var}";')

            flash("Done Bro!")
            if var in done.keys():
                done.pop(var)
        except:
            pass
        return redirect("/")


@app.route("/<var>/qr/")
def qr(var):
    if var in current:
        img = qrcode.make(f"smittal.tech/{var}")
        buffered = BytesIO()
        img.save(buffered, format="png")
        img_str = base64.b64encode(buffered.getvalue())
        session["b64"] = img_str
        session["alias"] = var
        return redirect("/final")
    else:
        var = var.lower()
        cursor.execute(f"select url from data where alias='{var}';")
        c = cursor.fetchall()
        # print(c)
        if c:
            img = qrcode.make(f"smittal.tech/{var}")
            buffered = BytesIO()
            img.save(buffered, format="png")
            img_str = base64.b64encode(buffered.getvalue())
            session["b64"] = img_str
            session["alias"] = var
            flash(f"USE smittal.tech/{var}/qr TO VISIT THIS PAGE")
            return redirect("/final")
        else:
            return redirect("/")


@app.route("/<var>/")
def start(var):
    global current, done
    if var in current:
        return redirect("/")
    if var in done.keys():
        return redirect(done[var])
    db.ping(reconnect=True, attempts=1, delay=0)
    # alias=alias.replace(' ','')
    var = var.lower()
    cursor.execute(f"select url from data where alias='{var}';")
    c = cursor.fetchall()
    # print(c)
    if c:
        print(c[0])
        return redirect(c[0][0])
    else:
        current.append(var)
        return redirect("/")


@app.route("/short/", methods=["GET"])
def short():
    if request.method == "GET":
        url = request.args.get("url")
        alias = request.args.get("alias")
    else:
        print("POST RECEIVED LOL")
        return redirect("/")

    global current, done
    db.ping(reconnect=True, attempts=1, delay=0)

    alias = alias.replace(" ", "")
    alias = alias.lower()
    cursor.execute("select alias from data;")
    c = [i[0] for i in cursor.fetchall()]

    if alias in c or alias in ["short", "final"]:
        flash("Alias Already Exists")
        return redirect("/")
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

        if alias in current:
            current.remove(alias)
        img = qrcode.make(f"smittal.tech/{alias}")

        buffered = BytesIO()
        img.save(buffered, format="png")
        img_str = base64.b64encode(buffered.getvalue())
        session["b64"] = img_str
        session["alias"] = alias
        flash(f"USE smittal.tech/{alias}/qr TO VISIT THIS PAGE")
        return redirect("/final")


@app.route("/final/")
def login():
    alias = session.get("alias", None)
    img_str = session.get("b64", None)
    if not alias:
        return redirect("/")
    else:
        return render_template("final.html", link=f"smittal.tech/{alias}", data=img_str)


if __name__ == "__main__":
    app.run(ssl_context=("cert.crt", "key.key"))
