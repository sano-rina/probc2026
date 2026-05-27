from flask_sqlalchemy import SQLAlchemy

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        "{db}://{user}:{password}@{host}/{dbName}?charset=utf8".format(
            db = "mysql",
            user = "probc2026",
            password = "probc2026",
            host = "localhost",
            dbName = "probc2026"
        )
    db.init_app(app)
    return db

db = SQLAlchemy()
class ユーザ(db.Model):
    __tablename__ = "ユーザ"
    ID = db.Column(db.Integer, primary_key = True)
    氏名 = db.Column(db.String(50))
    所属ID = db.Column(db.Integer)
    電話番号 = db.Column("電話番号(ハイフンなし)",db.String(50))
    メールアドレス = db.Column(db.String(100))
    学籍番号 = db.Column(db.String(9))
class ユーザ所属(db.Model):
    __tablename__ = "ユーザ所属"
    ID = db.Column(db.Integer, primary_key = True)
    学部 = db.Column(db.String(20))
    教員 = db.Column(db.String(10))
    その他 = db.Column(db.String(100))

class 利用区分(db.Model):
    __tablename__ = "利用区分"
    ID = db.Column(db.Integer, primary_key = True)
    ユーザID = db.Column(db.Integer)
    遺失者 = db.Column(db.Boolean)
    拾得者 = db.Column(db.Boolean)
    管理者 = db.Column(db.Boolean)
    その他 = db.Column(db.String(100))

class 拾得物(db.Model):
    __tablename__ = "拾得物"
    ID = db.Column(db.Integer, primary_key = True)
    拾得物分類ID = db.Column(db.Integer)
    拾得場所 = db.Column(db.String(100))
    拾得日時 = db.Column(db.DateTime)
    特徴 = db.Column(db.String(100))
    画像 = db.Column(db.String(100))

class 拾得物分類(db.Model):
    __tablename__ = "拾得物分類"
    ID = db.Column(db.Integer, primary_key = True)
    分類名 = db.Column(db.String(100))

class 拾得物管理状況(db.Model):
    __tablename__ = "拾得物管理状況"
    ID = db.Column(db.Integer, primary_key = True)
    利用区分ID = db.Column(db.Integer)
    拾得物ID = db.Column(db.Integer)
    登録日時 = db.Column(db.DateTime)
    預かり日時 = db.Column(db.String(100))
    返還日時 = db.Column(db.DateTime)
    拾得者持ち = db.Column(db.Boolean)
    預かり中 = db.Column(db.Boolean)
    返還済み = db.Column(db.Boolean)

class 遺失物捜索依頼(db.Model):
    __tablename__ = "遺失物捜索依頼"
    ID = db.Column(db.Integer, primary_key = True)
    利用区分ID = db.Column(db.Integer)
    拾得物分類ID = db.Column(db.Integer)
    遺失場所 = db.Column(db.String(100))
    遺失日時 = db.Column(db.DateTime)
    特徴 = db.Column(db.String(100))
    
