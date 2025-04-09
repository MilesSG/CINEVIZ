from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.models.movie import Movie
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json

visualization_bp = Blueprint('visualization', __name__, url_prefix='/api/visualization')

@visualization_bp.route('/box-office-trend', methods=['GET'])
def box_office_trend():
    """获取票房走势数据"""
    movie_id = request.args.get('movie_id')
    
    # 如果指定了电影ID，则获取单部电影的票房走势
    if movie_id:
        movie = Movie.get_by_id(movie_id)
        if not movie:
            return jsonify({'message': '电影不存在'}), 404
        
        # 从日票房数据中提取日期和票房
        dates = list(movie.daily_box_office.keys())
        box_offices = list(movie.daily_box_office.values())
        
        return jsonify({
            'movie_title': movie.title,
            'dates': dates,
            'box_offices': box_offices
        }), 200
    
    # 如果没有指定电影ID，则获取所有电影的累计票房走势
    movies = Movie.get_all_movies()
    
    # 按上映日期排序
    movies.sort(key=lambda movie: movie.release_date)
    
    # 提取电影标题和总票房
    titles = [movie.title for movie in movies]
    box_offices = [movie.box_office for movie in movies]
    release_dates = [movie.release_date for movie in movies]
    
    return jsonify({
        'titles': titles,
        'release_dates': release_dates,
        'box_offices': box_offices
    }), 200

@visualization_bp.route('/genre-comparison', methods=['GET'])
def genre_comparison():
    """获取不同类型电影的票房比较数据"""
    movie_id = request.args.get('movie_id')
    
    # 如果指定了电影ID，则只返回该电影的类型数据
    if movie_id:
        movie = Movie.get_by_id(movie_id)
        if not movie:
            return jsonify({'message': '电影不存在'}), 404
        
        # 针对单部电影，只返回其类型的数据
        genres = movie.genres
        # 每个类型的票房都是该电影的票房
        total_box_offices = [movie.box_office] * len(genres)
        avg_box_offices = [movie.box_office] * len(genres)
        counts = [1] * len(genres)
        
        return jsonify({
            'genres': genres,
            'total_box_offices': total_box_offices,
            'avg_box_offices': avg_box_offices,
            'counts': counts
        }), 200
    
    # 如果没有指定电影ID，则获取所有电影的类型比较数据
    movies = Movie.get_all_movies()
    
    # 统计每种类型的总票房和电影数量
    genre_stats = {}
    for movie in movies:
        for genre in movie.genres:
            if genre not in genre_stats:
                genre_stats[genre] = {
                    'total_box_office': 0,
                    'count': 0,
                    'avg_box_office': 0
                }
            
            genre_stats[genre]['total_box_office'] += movie.box_office
            genre_stats[genre]['count'] += 1
    
    # 计算平均票房
    for genre in genre_stats:
        if genre_stats[genre]['count'] > 0:
            genre_stats[genre]['avg_box_office'] = genre_stats[genre]['total_box_office'] / genre_stats[genre]['count']
    
    # 准备返回数据
    genres = list(genre_stats.keys())
    total_box_offices = [genre_stats[genre]['total_box_office'] for genre in genres]
    avg_box_offices = [genre_stats[genre]['avg_box_office'] for genre in genres]
    counts = [genre_stats[genre]['count'] for genre in genres]
    
    return jsonify({
        'genres': genres,
        'total_box_offices': total_box_offices,
        'avg_box_offices': avg_box_offices,
        'counts': counts
    }), 200

@visualization_bp.route('/release-heatmap', methods=['GET'])
def release_heatmap():
    """获取电影发行时间热力图数据"""
    movie_id = request.args.get('movie_id')
    
    # 如果指定了电影ID，则只返回该电影的发行时间数据
    if movie_id:
        movie = Movie.get_by_id(movie_id)
        if not movie:
            return jsonify({'message': '电影不存在'}), 404
        
        try:
            release_date = datetime.strptime(movie.release_date, '%Y-%m-%d')
            data = [{
                'month': release_date.month,
                'day': release_date.day,
                'count': 1
            }]
            
            return jsonify({
                'data': data
            }), 200
        except ValueError:
            return jsonify({'message': '电影发行日期格式不正确'}), 400
    
    # 如果没有指定电影ID，则获取所有电影的发行时间热力图数据
    movies = Movie.get_all_movies()
    
    # 提取每部电影的上映月份和日期
    months = []
    days = []
    
    for movie in movies:
        try:
            release_date = datetime.strptime(movie.release_date, '%Y-%m-%d')
            months.append(release_date.month)
            days.append(release_date.day)
        except ValueError:
            # 跳过日期格式不正确的电影
            continue
    
    # 统计每个月份-日期组合的电影数量
    date_counts = {}
    for i in range(len(months)):
        key = f"{months[i]}-{days[i]}"
        if key in date_counts:
            date_counts[key] += 1
        else:
            date_counts[key] = 1
    
    # 准备返回数据
    data = []
    for key, count in date_counts.items():
        month, day = map(int, key.split('-'))
        data.append({
            'month': month,
            'day': day,
            'count': count
        })
    
    return jsonify({
        'data': data
    }), 200

@visualization_bp.route('/box-office-distribution', methods=['GET'])
def box_office_distribution():
    """获取票房分布数据"""
    movie_id = request.args.get('movie_id')
    
    # 如果指定了电影ID，则只返回该电影的票房分布数据
    if movie_id:
        movie = Movie.get_by_id(movie_id)
        if not movie:
            return jsonify({'message': '电影不存在'}), 404
        
        # 对于单部电影，我们创建一个只包含该电影票房的分布
        box_office = movie.box_office
        
        # 创建一个区间，使电影票房正好在中间
        lower = max(0, box_office - 10000000)  # 假设向下偏移1000万
        upper = box_office + 10000000  # 向上偏移1000万
        
        intervals = [f"{int(lower)}-{int(upper)}"]
        counts = [1]
        
        return jsonify({
            'intervals': intervals,
            'counts': counts,
            'movies': {
                'titles': [movie.title],
                'box_offices': [box_office]
            }
        }), 200
    
    # 如果没有指定电影ID，则获取所有电影的票房分布数据
    movies = Movie.get_all_movies()
    
    # 提取票房数据
    box_offices = [movie.box_office for movie in movies]
    titles = [movie.title for movie in movies]
    
    # 计算票房分布区间
    min_box_office = min(box_offices) if box_offices else 0
    max_box_office = max(box_offices) if box_offices else 0
    
    # 创建10个区间
    interval = (max_box_office - min_box_office) / 10 if max_box_office > min_box_office else 1
    intervals = []
    for i in range(10):
        lower = min_box_office + i * interval
        upper = min_box_office + (i + 1) * interval
        intervals.append({
            'range': f"{int(lower)}-{int(upper)}",
            'lower': lower,
            'upper': upper,
            'count': 0
        })
    
    # 统计每个区间的电影数量
    for box_office in box_offices:
        for interval in intervals:
            if interval['lower'] <= box_office < interval['upper'] or (box_office == max_box_office and interval['upper'] == max_box_office):
                interval['count'] += 1
                break
    
    return jsonify({
        'intervals': [interval['range'] for interval in intervals],
        'counts': [interval['count'] for interval in intervals],
        'movies': {
            'titles': titles,
            'box_offices': box_offices
        }
    }), 200 