from flask import request, jsonify
from database.db import db
from models.user import User
from models.scan import Scan
from auth.auth import generate_token
import asyncio
from crawler.crawler import crawl
from core.checker import check

def register(app):

    @app.route("/register", methods=["POST"])
    def register_user():
        data = request.json
        user = User(username=data["username"], password=data["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "created"})

    @app.route("/login", methods=["POST"])
    def login():
        data = request.json
        user = User.query.filter_by(username=data["username"], password=data["password"]).first()
        token = generate_token(user.id)
        return jsonify({"token": token})

    @app.route("/scan", methods=["POST"])
    def scan():
        url = request.json["url"]

        urls = asyncio.run(crawl(url))
        results = asyncio.run(check(urls))

        scan = Scan(url=url, result=str(results))
        db.session.add(scan)
        db.session.commit()

        return jsonify(results)
