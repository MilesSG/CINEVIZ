from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    
    # 配置跨域
    CORS(app)
    
    # 配置JWT
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-key")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    jwt = JWTManager(app)
    
    # 注册路由
    from app.routes.auth import auth_bp
    from app.routes.movies import movies_bp
    from app.routes.admin import admin_bp
    from app.routes.visualization import visualization_bp
    from app.routes.crawl import crawl_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(visualization_bp)
    app.register_blueprint(crawl_bp)
    
    return app 