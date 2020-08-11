#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template, request

from models.models import TaskContent, User

from models.database import db_session
from datetime import datetime
from flask import session,redirect,url_for
from app import key
from hashlib import sha256

#Flaskオブジェクトの生成
app = Flask(__name__)
app.secret_key = key.SECRET_KEY

@app.route("/")
#「/index」へアクセスがあった場合に、「index.html」を返す
# ログイン情報がなければログアウトにリダイレクト
@app.route("/index")
def index():
    if "user_name" in session:
        name = session["user_name"]
        # 以下でTaskContentの内容を全て取り出している
        tasks = TaskContent.query.filter_by(user_Name=name)
        return render_template("index.html",name=name,user_task=tasks)
    else:
        return redirect(url_for("top",status="logout"))

@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html",status=status)


@app.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html",status=status)


@app.route("/add",methods=["post"])
def add():
    name = session["user_name"]
    title = request.form["title"]
    register_date = datetime.now()
    update_date = datetime.now()
    status = request.form["status"]
    free = request.form["free"]
    content = TaskContent(name, title, register_date, update_date, status, free)
    db_session.add(content)
    db_session.commit()
    return redirect(url_for("index") )


@app.route("/update",methods=["post"])
def update():
    content = TaskContent.query.filter_by(id=request.form["update"]).first()
    content.title = request.form["title"]
    content.update_date = datetime.now()
    content.status = request.form["status"]
    content.free = request.form["free"]
    print(content.register_date)
    db_session.commit()
    return redirect(url_for("index") )


@app.route("/delete",methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = TaskContent.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return redirect(url_for("index") )


@app.route("/login",methods=["post"])
def login():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        if user.hashed_password == hashed_password:
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top",status="wrong_password"))
    else:
        return redirect(url_for("top",status="user_notfound"))


@app.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top",status="logout"))


@app.route("/registar",methods=["post"])
def registar():
    user_name = request.form["user_name"]
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        return redirect(url_for("newcomer",status="exist_user"))
    else:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name, hashed_password)
        db_session.add(user)
        db_session.commit()
        session["user_name"] = user_name
        # db_session.close()
        return redirect(url_for("index"))


#おまじない
if __name__ == "__main__":
    app.run(debug=True)
