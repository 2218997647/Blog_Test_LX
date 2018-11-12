from . import api
from flask import g, current_app, jsonify, request, session
from lx_blog.utils.response_code import RET
from lx_blog.models import Category, Article, ArticleImage, User
from lx_blog import db, constants, redis_store
from lx_blog.utils.commons import login_required
from datetime import datetime
import json
import random


@api.route("/category")
def get_category_info():
    """获取类别信息"""
    # 尝试从redis中读取数据
    try:
        resp_json = redis_store.get("category_info")
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json is not None:
            # redis有缓存数据
            current_app.logger.info("hit redis category_info")
            return resp_json, 200, {"Content-Type": "application/json"}

    # 查询数据库，读取类别信息
    try:
        category_li = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    category_dict_li = []
    # 将对象转换为字典
    for categ in category_li:
        category_dict_li.append(categ.to_dict())

    # 将数据转换为json字符串
    resp_dict = dict(errno=RET.OK, errmsg="OK", data=category_dict_li)
    resp_json = json.dumps(resp_dict)

    # 将数据保存到redis中
    try:
        redis_store.setex("category_info", constants.AREA_INFO_REDIS_CACHE_EXPIRES, resp_json)
    except Exception as e:
        current_app.logger.error(e)

    return resp_json, 200, {"Content-Type": "application/json"}


@api.route("/articles/info", methods=["POST"])
@login_required
def save_article_info():

    # 获取数据
    user_id = g.user_id
    article_data = request.get_json()

    title = article_data.get("title")  # 标题
    category_id = article_data.get("category_id")
    article_content=article_data.get("content")


    # 校验参数
    if not all([title,article_content,category_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 判断id是否存在
    try:
        category = Category.query.get(category_id)
        print(category)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    if category is None:
        return jsonify(errno=RET.NODATA, errmsg="类别信息有误")

    # 保存信息
    article = Article(
        user_id=user_id,
        category_id=category_id,
        title=title,
        content=article_content

    )

    try:
        db.session.add(article)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存数据失败")

    # 保存数据成功
    return jsonify(errno=RET.OK, errmsg="OK", data={"article_id": article.id})



@api.route("/user/articles", methods=["GET"])
@login_required
def get_user_articles():
    """获取发布的文章条目"""
    user_id = g.user_id

    try:

        user = User.query.get(user_id)
        articles = user.articles
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取数据失败")

    # 将查询到的文章转换为字典存放到列表中
    articles_list = []
    if articles:
        for article in articles:
            articles_list.append(article.to_basic_dict())
    return jsonify(errno=RET.OK, errmsg="OK", data={"articles": articles_list})


@api.route("/articles/<int:id>", methods=["GET"])
def get_article_detail(id):
    user_id = session.get("user_id", "-1")
    print("user_id",user_id)
    print("id",id)

    # 校验参数
    if not id:
        return jsonify(errno=RET.PARAMERR, errmsg="参数确实")

    # 先从redis缓存中获取信息

    # try:
    #     ret = redis_store.get("article_info_%s" % id)
    # except Exception as e:
    #     current_app.logger.error(e)
    #     ret = None
    # if ret:
    #     current_app.logger.info("hit article info redis")
    #     return '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "article":%s}}' % (user_id, ret), \
    #            200, {"Content-Type": "application/json"}

    # 查询数据库
    try:
        article = Article.query.get(id)
        print("article",article.content)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not article:
        return jsonify(errno=RET.NODATA, errmsg="文章不存在")

    # 将对象数据转换为字典
    try:
        article_data = article.to_full_dict()
        print("art_data",article_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="数据出错")

    # 存入到redis中
    json_article = json.dumps(article_data)
    print("json_article",json_article)
    try:
        redis_store.setex("article_info_%s" % id, constants.ARTICLE_DETAIL_REDIS_EXPIRE_SECOND, json_article)
    except Exception as e:
        current_app.logger.error(e)

    resp = '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "article":%s}}' % (user_id, json_article), \
           200, {"Content-Type": "application/json"}
    return resp



@api.route("/guest/articles", methods=["GET"])
def get_guest_articles():

    try:
        article_num=Article.query.filter().count()
        print("article_num",article_num)
        random_num=random.randint(1,article_num)-1
        print("random_num",random_num)
        offset_num=random_num
        limit_num=article_num-random_num
        print("limit_num",limit_num)
        articles = Article.query.offset(offset_num).limit(limit_num)

        print("articles",articles)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取数据失败")

    # 将查询到的文章转换为字典存放到列表中
    articles_list = []
    if articles:
        for article in articles:
            articles_list.append(article.to_full_dict())
    return jsonify(errno=RET.OK, errmsg="OK", data={"articles": articles_list})






