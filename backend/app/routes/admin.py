from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.movie import Movie
from app.models.user import User
import os
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

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

@admin_bp.route('/movies', methods=['POST'])
@admin_required
def create_movie():
    data = request.get_json()
    
    required_fields = ['title', 'release_date', 'genres', 'director', 'actors', 'poster_url', 'box_office']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'缺少必要字段: {field}'}), 400
    
    # 创建电影
    movie = Movie(
        title=data['title'],
        release_date=data['release_date'],
        genres=data['genres'],
        director=data['director'],
        actors=data['actors'],
        poster_url=data['poster_url'],
        box_office=data['box_office'],
        daily_box_office=data.get('daily_box_office', {}),
        rating=data.get('rating', 0.0),
        description=data.get('description', '')
    )
    
    movie.save()
    
    return jsonify({
        'message': '电影创建成功',
        'movie': movie.to_dict()
    }), 201

@admin_bp.route('/movies/<movie_id>', methods=['PUT'])
@admin_required
def update_movie(movie_id):
    movie = Movie.get_by_id(movie_id)
    
    if not movie:
        return jsonify({'message': '电影不存在'}), 404
    
    data = request.get_json()
    
    # 更新电影信息
    if 'title' in data:
        movie.title = data['title']
    if 'release_date' in data:
        movie.release_date = data['release_date']
    if 'genres' in data:
        movie.genres = data['genres']
    if 'director' in data:
        movie.director = data['director']
    if 'actors' in data:
        movie.actors = data['actors']
    if 'poster_url' in data:
        movie.poster_url = data['poster_url']
    if 'box_office' in data:
        movie.box_office = data['box_office']
    if 'daily_box_office' in data:
        movie.daily_box_office = data['daily_box_office']
    if 'rating' in data:
        movie.rating = data['rating']
    if 'description' in data:
        movie.description = data['description']
    
    movie.save()
    
    return jsonify({
        'message': '电影更新成功',
        'movie': movie.to_dict()
    }), 200

@admin_bp.route('/movies/<movie_id>', methods=['DELETE'])
@admin_required
def delete_movie(movie_id):
    movie = Movie.get_by_id(movie_id)
    
    if not movie:
        return jsonify({'message': '电影不存在'}), 404
    
    Movie.delete(movie_id)
    
    return jsonify({
        'message': '电影删除成功'
    }), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.get_all_users()
    
    # 格式化响应
    users_data = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at
    } for user in users]
    
    return jsonify({
        'users': users_data,
        'count': len(users_data)
    }), 200

@admin_bp.route('/users/<user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    user = User.get_by_id(user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'favorites': user.favorites,
            'created_at': user.created_at
        }
    }), 200

@admin_bp.route('/users/<user_id>/role', methods=['PUT'])
@admin_required
def update_user_role(user_id):
    user = User.get_by_id(user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    data = request.get_json()
    
    if 'role' not in data:
        return jsonify({'message': '缺少角色信息'}), 400
    
    role = data['role']
    if role not in ['user', 'admin']:
        return jsonify({'message': '角色无效'}), 400
    
    user.role = role
    user.save()
    
    return jsonify({
        'message': '用户角色更新成功',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200

@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.get_by_id(user_id)
    
    if not user:
        return jsonify({'message': '用户不存在'}), 404
    
    # 不允许删除当前用户
    current_user_id = get_jwt_identity()
    if user_id == current_user_id:
        return jsonify({'message': '不能删除当前用户'}), 400
    
    User.delete(user_id)
    
    return jsonify({
        'message': '用户删除成功'
    }), 200

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard_stats():
    # 获取所有电影和用户
    movies = Movie.get_all_movies()
    users = User.get_all_users()
    
    # 计算总票房
    total_box_office = sum(movie.box_office for movie in movies)
    
    # 统计类型分布
    genre_stats = {}
    for movie in movies:
        for genre in movie.genres:
            if genre in genre_stats:
                genre_stats[genre] += 1
            else:
                genre_stats[genre] = 1
    
    # 获取热门电影（按票房排序）
    top_movies = sorted(movies, key=lambda movie: movie.box_office, reverse=True)[:5]
    
    return jsonify({
        'stats': {
            'total_movies': len(movies),
            'total_users': len(users),
            'total_box_office': total_box_office,
            'genre_distribution': genre_stats
        },
        'top_movies': [movie.to_dict() for movie in top_movies]
    }), 200 