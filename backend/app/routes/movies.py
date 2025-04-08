from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.movie import Movie
from app.models.user import User

movies_bp = Blueprint('movies', __name__, url_prefix='/api/movies')

@movies_bp.route('', methods=['GET'])
def get_movies():
    # 获取查询参数
    title = request.args.get('title')
    genre = request.args.get('genre')
    
    # 获取所有电影
    if title:
        movies = Movie.get_by_title(title)
    elif genre:
        movies = Movie.get_by_genre(genre)
    else:
        movies = Movie.get_all_movies()
    
    # 格式化响应
    movies_data = [movie.to_dict() for movie in movies]
    
    return jsonify({
        'movies': movies_data,
        'count': len(movies_data)
    }), 200

@movies_bp.route('/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.get_by_id(movie_id)
    
    if not movie:
        return jsonify({'message': '电影不存在'}), 404
    
    return jsonify(movie.to_dict()), 200

@movies_bp.route('/top', methods=['GET'])
def get_top_movies():
    # 获取限制数量，默认为10
    limit = int(request.args.get('limit', 10))
    
    # 获取所有电影并按票房排序
    movies = Movie.get_all_movies()
    movies.sort(key=lambda movie: movie.box_office, reverse=True)
    
    # 截取指定数量
    top_movies = movies[:limit]
    
    # 格式化响应
    movies_data = [movie.to_dict() for movie in top_movies]
    
    return jsonify({
        'movies': movies_data,
        'count': len(movies_data)
    }), 200

@movies_bp.route('/latest', methods=['GET'])
def get_latest_movies():
    # 获取限制数量，默认为10
    limit = int(request.args.get('limit', 10))
    
    # 获取所有电影并按发布日期排序
    movies = Movie.get_all_movies()
    movies.sort(key=lambda movie: movie.release_date, reverse=True)
    
    # 截取指定数量
    latest_movies = movies[:limit]
    
    # 格式化响应
    movies_data = [movie.to_dict() for movie in latest_movies]
    
    return jsonify({
        'movies': movies_data,
        'count': len(movies_data)
    }), 200

@movies_bp.route('/genres', methods=['GET'])
def get_genres():
    # 获取所有电影
    movies = Movie.get_all_movies()
    
    # 提取所有类型并去重
    all_genres = set()
    for movie in movies:
        all_genres.update(movie.genres)
    
    return jsonify({
        'genres': list(all_genres)
    }), 200 