from flask import Flask, request, jsonify
import asyncio
from crawler.crawler import crawl_site
from core.checker import check_urls

app = Flask(__name__)

@app.route("/scan", methods=["POST"])
def scan():
    url = request.json["url"]

    urls = asyncio.run(crawl_site(url))
    results = asyncio.run(check_urls(urls))

    return jsonify(results)
from config import *
from database.db import db
from flask_jwt_extended import JWTManager
from api.routes import register

app = Flask(__name__)
app.config.from_object("config")

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

register(app)

if __name__ == "__main__":
    app.run(debug=True)
