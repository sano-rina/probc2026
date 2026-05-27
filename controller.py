from flask import render_template, jsonify
from sqlalchemy import func
from model import db, ユーザ, ユーザ所属, 利用区分, 拾得物, 拾得物分類, 拾得物管理状況,遺失物捜索依頼

def top():
    return render_template("top.html")

def get_json(data):
    if data == "user":
        return jsonify(get_user_list())
    elif data == "item":
        return jsonify(get_item_list())
    elif data == "kubun":
        return jsonify(get_kubun_list())
    elif data == "category":
        return jsonify(get_category_list())
    elif data == "dept":
        return jsonify(get_dept_list())
    elif data == "request":
        return jsonify(get_request_list())

def get_dept_list():
    data = db.session.query(ユーザ所属).all()
    obj = []
    for i in data:
        obj.append({
            "所属ID":i.ID,
            "学部":i.学部,
            "教員":i.教員, 
            "その他":i.その他
            })
    return(obj)

def get_user_list():
   
    data = db.session.query(ユーザ,ユーザ所属).filter(ユーザ.所属ID==ユーザ所属.ID).all()
    obj = []
    for i,j in data:
        obj.append({
            "ユーザID":i.ID,
            "所属ID":i.所属ID,
            "氏名":i.氏名,
            "電話番号":i.電話番号,
            "メールアドレス":i.メールアドレス,
            "学籍番号":i.学籍番号,
            "学部":j.学部,
            })
    return(obj)

def get_kubun_list():

    data = db.session.query(利用区分).all()

    obj = []

    for i in data:
        obj.append({
            "ID": i.ID,
            "ユーザID": i.ユーザID,
            "遺失者": i.遺失者,
            "拾得者": i.拾得者,
            "管理者": i.管理者,
            "その他": i.その他
        })

    return(obj)

def get_item_list(key=""):
    lastdt = db.session.query(
        拾得物管理状況.拾得物ID.label("oid"),
        func.max(拾得物管理状況.登録日時).label("last")
    ).group_by(
        拾得物管理状況.拾得物ID
    ).subquery()
    tmp = db.session.query(
        拾得物管理状況, 
        拾得物, 
        拾得物分類, 
        ユーザ, 
        ユーザ所属,
        利用区分
    ).filter(
        拾得物管理状況.拾得物ID==拾得物.ID
    ).filter(
        拾得物.拾得物分類ID==拾得物分類.ID
    ).filter(
        利用区分.ID==拾得物管理状況.利用区分ID
    ).filter(
        ユーザ.所属ID==ユーザ所属.ID
    ).filter(
        利用区分.ユーザID==ユーザ.ID    
    ).filter(
        拾得物管理状況.登録日時==lastdt.c.last
    ).filter(
        拾得物管理状況.拾得物ID==lastdt.c.oid
    )
    if key == "":
        data = tmp.all()
    else:
        data = tmp.filter(拾得物分類.分類名.contains(key)).all()
    obj = []
    for i,j,k,l,m,n in data:
        obj.append({
            "分類名":k.分類名,
            
            "拾得物ID":j.ID,
            "拾得場所":j.拾得場所,
            "特徴":j.特徴,
            "画像":j.画像,

            "拾得物管理状況ID":i.ID,
            "登録日時":str(i.登録日時),
            "預かり日時":i.預かり日時,
            "返還日時":str(i.返還日時),

            "氏名":l.氏名,

            "学部":m.学部,

            "利用区分ID": n.ID,
            "遺失者": n.遺失者,
            "拾得者": n.拾得者,
            "管理者": n.管理者

            })
    return(obj)

def get_category_list():
    data = db.session.query(拾得物分類).all()
    obj = []
    for i in data:
        obj.append({
            "ID":i.ID,
            "分類名":i.分類名
            })
    return(obj)

def get_request_list():
    data = db.session.query(
        遺失物捜索依頼,
        利用区分,
        ユーザ,
        ユーザ所属,
        拾得物分類
    ).filter(
        遺失物捜索依頼.利用区分ID == 利用区分.ID
    ).filter(
        利用区分.ユーザID == ユーザ.ID
    ).filter(
        ユーザ.所属ID == ユーザ所属.ID
    ).filter(
        遺失物捜索依頼.拾得物分類ID == 拾得物分類.ID
    ).all()

    obj = []

    for i, j, k, l, m in data:
        obj.append({
            "依頼ID": i.ID,
            "利用区分ID": i.利用区分ID,
            "拾得物分類ID": i.拾得物分類ID,

            "分類名": m.分類名,

            "遺失場所": i.遺失場所,
            "遺失日時": str(i.遺失日時),
            "特徴": i.特徴,

            "ユーザID": k.ID,
            "氏名": k.氏名,
            "学籍番号": k.学籍番号,
            "電話番号": k.電話番号,
            "メールアドレス": k.メールアドレス,

            "学部": l.学部,

            "遺失者": j.遺失者,
            "拾得者": j.拾得者,
            "管理者": j.管理者
        })

    return(obj)
