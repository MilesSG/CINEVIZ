from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.services.scraper import MovieScraper

crawl_bp = Blueprint('crawl', __name__, url_prefix='/api/crawl')

# 管理员权限检查装饰器
def admin_required(func):
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.get_by_id(current_user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'message': '需要管理员权限'}), 403
        
        return func(*args, **kwargs)
    
    wrapper.__name__ = func.__name__
    return jwt_required()(wrapper)

@crawl_bp.route('/maoyan', methods=['POST'])
@admin_required
def crawl_maoyan():
    """触发猫眼电影数据爬取"""
    data = request.get_json() or {}
    pages = data.get('pages', 1)
    
    # 限制最大页数
    if pages > 10:
        pages = 10
    
    scraper = MovieScraper()
    try:
        movies = scraper.scrape_maoyan(pages=pages)
        return jsonify({
            'message': f'成功爬取{len(movies)}部电影',
            'count': len(movies)
        }), 200
    except Exception as e:
        return jsonify({
            'message': f'爬取数据时出错: {str(e)}'
        }), 500 