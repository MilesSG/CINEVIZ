import json
import os
import uuid
from datetime import datetime

MOVIES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'movies.json')

class Movie:
    def __init__(self, title, release_date, genres, director, actors, poster_url, 
                 box_office, daily_box_office=None, rating=None, description=None, movie_id=None, created_at=None):
        self.id = movie_id or str(uuid.uuid4())
        self.title = title
        self.release_date = release_date
        self.genres = genres  # 列表
        self.director = director
        self.actors = actors  # 列表
        self.poster_url = poster_url
        self.box_office = box_office  # 总票房
        self.daily_box_office = daily_box_office or {}  # 日期: 单日票房的字典
        self.rating = rating or 0.0
        self.description = description or ""
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'genres': self.genres,
            'director': self.director,
            'actors': self.actors,
            'poster_url': self.poster_url,
            'box_office': self.box_office,
            'daily_box_office': self.daily_box_office,
            'rating': self.rating,
            'description': self.description,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data['title'],
            release_date=data['release_date'],
            genres=data['genres'],
            director=data['director'],
            actors=data['actors'],
            poster_url=data['poster_url'],
            box_office=data['box_office'],
            daily_box_office=data.get('daily_box_office', {}),
            rating=data.get('rating', 0.0),
            description=data.get('description', ""),
            movie_id=data['id'],
            created_at=data['created_at']
        )
    
    @classmethod
    def get_all_movies(cls):
        if not os.path.exists(MOVIES_FILE):
            # 确保目录存在
            os.makedirs(os.path.dirname(MOVIES_FILE), exist_ok=True)
            with open(MOVIES_FILE, 'w') as f:
                json.dump([], f)
            return []
        
        with open(MOVIES_FILE, 'r') as f:
            movies_data = json.load(f)
        
        return [cls.from_dict(movie_data) for movie_data in movies_data]
    
    @classmethod
    def get_by_id(cls, movie_id):
        movies = cls.get_all_movies()
        for movie in movies:
            if movie.id == movie_id:
                return movie
        return None
    
    @classmethod
    def get_by_title(cls, title):
        movies = cls.get_all_movies()
        return [movie for movie in movies if title.lower() in movie.title.lower()]
    
    @classmethod
    def get_by_genre(cls, genre):
        movies = cls.get_all_movies()
        return [movie for movie in movies if genre in movie.genres]
    
    def save(self):
        movies = self.get_all_movies()
        
        # 检查是否已存在该电影，如果存在则更新
        for i, movie in enumerate(movies):
            if movie.id == self.id:
                movies[i] = self
                break
        else:
            # 不存在则添加
            movies.append(self)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(MOVIES_FILE), exist_ok=True)
        
        # 保存到文件
        with open(MOVIES_FILE, 'w') as f:
            json.dump([movie.to_dict() for movie in movies], f, indent=4)
        
        return self
    
    @classmethod
    def delete(cls, movie_id):
        movies = cls.get_all_movies()
        movies = [movie for movie in movies if movie.id != movie_id]
        
        with open(MOVIES_FILE, 'w') as f:
            json.dump([movie.to_dict() for movie in movies], f, indent=4)
        
        return True 