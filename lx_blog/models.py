from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from lx_blog import constants


class BaseModel(object):
    #base class,to provide create time and update time for the article.
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class User(BaseModel, db.Model):

    __tablename__ = "user_profile"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(11), unique=True, nullable=False)
    real_name = db.Column(db.String(32))
    id_card = db.Column(db.String(20))
    #photo of user
    avatar_url = db.Column(db.String(128))
    articles = db.relationship("Article", backref="user")

    # @property:to make a func to the attribute,so the name of attribute equels to the func name
    @property
    def password(self):
        #getter
        raise AttributeError("不能读取")

    # setter
    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, passwd):
        return check_password_hash(self.password_hash, passwd)

    def to_dict(self):
        """将对象转换为字典数据"""
        user_dict = {
            "user_id": self.id,
            "name": self.name,
            "mobile": self.mobile,
            "avatar": constants.QINIU_URL_DOMAIN + self.avatar_url if self.avatar_url else "",
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return user_dict

    def auth_to_dict(self):
        """将实名信息转换为字典数据"""
        auth_dict = {
            "user_id": self.id,
            "real_name": self.real_name,
            "id_card": self.id_card
        }
        return auth_dict

class Category(BaseModel, db.Model):
    __tablename__ = "category_info"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    articles = db.relationship("Article", backref="category")

    def to_dict(self):
        """将对象转换为字典"""
        d = {
            "aid": self.id,
            "aname": self.name
        }
        return d



class Article(BaseModel, db.Model):
    __tablename__ = "article_info"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_profile.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category_info.id"), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    content =db.Column(db.Text,nullable=True)
    #the main pic of the article
    index_image_url = db.Column(db.String(256), default="")
    images = db.relationship("ArticleImage")

    def to_basic_dict(self):
        """将基本信息转换为字典数据"""
        article_dict = {
            "article_id": self.id,
            "title": self.title,
            "content": self.content,
            "category_name": self.category.name
        }
        return article_dict

    def to_full_dict(self):
        """将详细信息转换为字典数据"""
        article_dict = {
            "aid": self.id,
            "user_id": self.user_id,
            "user_name": self.user.name,
            "title": self.title,
            "content": self.content,
            "category_name": self.category.name

        }
        return article_dict




class ArticleImage(BaseModel, db.Model):
    __tablename__ = "article_image"
    id = db.Column(db.Integer, primary_key=True)
    artcile_id = db.Column(db.Integer, db.ForeignKey("article_info.id"), nullable=False)
    url = db.Column(db.String(256), nullable=False)


