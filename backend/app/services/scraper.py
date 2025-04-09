import requests
from bs4 import BeautifulSoup
import json
import random
import time
from datetime import datetime, timedelta
import os
from app.models.movie import Movie

class MovieScraper:
    """电影数据爬虫类"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_maoyan(self, pages=1):
        """爬取猫眼电影数据"""
        movies = []
        
        for page in range(1, pages + 1):
            try:
                # 模拟访问猫眼电影排行榜
                url = f'https://www.maoyan.com/board/4?offset={(page-1)*10}'
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                movie_items = soup.select('.board-item-content')
                
                for item in movie_items:
                    try:
                        # 提取电影信息
                        title = item.select_one('.name a').text.strip()
                        actors_text = item.select_one('.star').text.strip().replace('主演：', '')
                        actors = [actor.strip() for actor in actors_text.split(',')]
                        release_info = item.select_one('.releasetime').text.strip().replace('上映时间：', '')
                        release_date = self._extract_date(release_info)
                        
                        # 获取评分
                        rating_integers = item.select_one('.integer').text.strip()
                        rating_fraction = item.select_one('.fraction').text.strip()
                        rating = float(rating_integers + rating_fraction)
                        
                        # 获取海报URL
                        poster_url = item.select_one('img')['data-src']
                        if not poster_url.startswith('http'):
                            poster_url = 'https:' + poster_url
                        
                        # 生成随机票房数据（实际应用中应该爬取真实数据）
                        box_office = random.randint(5000, 500000) * 10000  # 5千万到5亿之间
                        daily_box_office = self._generate_daily_box_office(release_date)
                        
                        # 获取电影详情页URL
                        detail_url = 'https://www.maoyan.com' + item.select_one('.name a')['href']
                        
                        # 爬取电影详情
                        movie_detail = self._scrape_movie_detail(detail_url)
                        
                        # 创建电影对象
                        movie = Movie(
                            title=title,
                            release_date=release_date,
                            genres=movie_detail.get('genres', ['未知']),
                            director=movie_detail.get('director', '未知'),
                            actors=actors,
                            poster_url=poster_url,
                            box_office=box_office,
                            daily_box_office=daily_box_office,
                            rating=rating,
                            description=movie_detail.get('description', '')
                        )
                        
                        # 保存电影
                        movie.save()
                        movies.append(movie)
                        
                        # 休眠一段时间，避免请求过于频繁
                        time.sleep(random.uniform(1, 3))
                        
                    except Exception as e:
                        print(f"爬取电影时出错: {e}")
                
                # 翻页前休眠一段时间
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                print(f"爬取第{page}页时出错: {e}")
        
        return movies
    
    def _scrape_movie_detail(self, url):
        """爬取电影详情"""
        detail = {
            'genres': [],
            'director': '未知',
            'description': ''
        }
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 获取类型
            genre_elements = soup.select('.movie-brief-container ul li:nth-child(1) a')
            if genre_elements:
                detail['genres'] = [genre.text.strip() for genre in genre_elements]
            
            # 获取导演
            director_element = soup.select_one('.celebrity-group li:nth-child(1) .info a')
            if director_element:
                detail['director'] = director_element.text.strip()
            
            # 获取简介
            description_element = soup.select_one('.mod-content .dra')
            if description_element:
                detail['description'] = description_element.text.strip()
        
        except Exception as e:
            print(f"爬取电影详情时出错: {e}")
        
        return detail
    
    def _extract_date(self, date_text):
        """从日期文本中提取日期，格式化为YYYY-MM-DD"""
        try:
            # 尝试从文本中提取年、月、日
            year = None
            month = None
            day = None
            
            date_parts = date_text.split('-')
            if len(date_parts) >= 3:
                # 格式化为YYYY-MM-DD
                year, month, day = date_parts[:3]
            elif '年' in date_text and '月' in date_text:
                # 处理"2020年10月01日"格式
                date_parts = date_text.replace('年', '-').replace('月', '-').replace('日', '').split('-')
                if len(date_parts) >= 3:
                    year, month, day = date_parts[:3]
            
            if year and month and day:
                if len(year) == 2:
                    year = '20' + year
                if len(month) == 1:
                    month = '0' + month
                if len(day) == 1:
                    day = '0' + day
                
                return f"{year}-{month}-{day}"
            else:
                # 如果无法解析，则使用当前日期减去随机天数
                today = datetime.now()
                days_ago = random.randint(30, 365)
                random_date = today - timedelta(days=days_ago)
                return random_date.strftime('%Y-%m-%d')
        
        except Exception:
            # 默认返回随机日期
            today = datetime.now()
            days_ago = random.randint(30, 365)
            random_date = today - timedelta(days=days_ago)
            return random_date.strftime('%Y-%m-%d')
    
    def _generate_daily_box_office(self, release_date):
        """生成虚拟的日票房数据"""
        daily_box_office = {}
        
        try:
            # 将字符串日期转为日期对象
            start_date = datetime.strptime(release_date, '%Y-%m-%d')
            
            # 生成从上映日开始的30天票房数据
            for i in range(30):
                current_date = start_date + timedelta(days=i)
                date_str = current_date.strftime('%Y-%m-%d')
                
                # 模拟票房趋势：先增后减
                if i < 10:
                    # 前10天票房上升
                    daily_amount = random.randint(1000, 5000) * 10000 * (1 + i * 0.1)
                else:
                    # 后面票房逐渐下降
                    decay_factor = (30 - i) / 20  # 衰减系数
                    daily_amount = random.randint(1000, 5000) * 10000 * decay_factor
                
                daily_box_office[date_str] = int(daily_amount)
        
        except Exception as e:
            print(f"生成日票房数据时出错: {e}")
        
        return daily_box_office 