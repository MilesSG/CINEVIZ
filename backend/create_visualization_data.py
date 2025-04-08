import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.movie import Movie
from datetime import datetime, timedelta
import random
import json

def ensure_visualization_data():
    """确保生成了可视化所需的所有数据"""
    # 1. 检查是否有足够的电影数据
    movies = Movie.get_all_movies()
    
    if len(movies) < 10:
        print(f"警告: 电影数量不足 ({len(movies)}部)，推荐运行 create_sample_data.py 创建更多样本数据")
    
    # 2. 确保每部电影都有日票房数据
    movies_without_daily_data = []
    for movie in movies:
        if not movie.daily_box_office or len(movie.daily_box_office) == 0:
            movies_without_daily_data.append(movie)
    
    if movies_without_daily_data:
        print(f"发现 {len(movies_without_daily_data)} 部电影缺少日票房数据，正在生成...")
        for movie in movies_without_daily_data:
            # 生成日票房数据
            daily_box_office = generate_daily_box_office(movie.release_date)
            
            # 更新电影对象
            movie.daily_box_office = daily_box_office
            movie.save()
            
            print(f"已添加日票房数据: {movie.title}")
    else:
        print("所有电影均有日票房数据")
    
    # 3. 检查电影类型分布
    genres = {}
    for movie in movies:
        for genre in movie.genres:
            if genre in genres:
                genres[genre] += 1
            else:
                genres[genre] = 1
    
    print("\n电影类型分布:")
    for genre, count in genres.items():
        print(f"{genre}: {count}部")
    
    # 4. 检查发行日期分布
    months = {}
    for movie in movies:
        try:
            date = datetime.strptime(movie.release_date, "%Y-%m-%d")
            month = date.month
            if month in months:
                months[month] += 1
            else:
                months[month] = 1
        except Exception as e:
            print(f"解析发行日期出错 ({movie.title}): {e}")
    
    print("\n电影发行月份分布:")
    for month in range(1, 13):
        count = months.get(month, 0)
        print(f"{month}月: {count}部")
    
    # 5. 检查票房分布
    box_office_ranges = {
        "1千万以下": 0,
        "1千万-5千万": 0,
        "5千万-1亿": 0,
        "1亿-5亿": 0,
        "5亿-10亿": 0,
        "10亿以上": 0
    }
    
    for movie in movies:
        box_office = movie.box_office
        if box_office < 10_000_000:
            box_office_ranges["1千万以下"] += 1
        elif box_office < 50_000_000:
            box_office_ranges["1千万-5千万"] += 1
        elif box_office < 100_000_000:
            box_office_ranges["5千万-1亿"] += 1
        elif box_office < 500_000_000:
            box_office_ranges["1亿-5亿"] += 1
        elif box_office < 1_000_000_000:
            box_office_ranges["5亿-10亿"] += 1
        else:
            box_office_ranges["10亿以上"] += 1
    
    print("\n票房分布区间:")
    for range_name, count in box_office_ranges.items():
        print(f"{range_name}: {count}部")
    
    print("\n数据检查和生成完成!")
    print(f"共有 {len(movies)} 部电影，可用于可视化分析")

def generate_daily_box_office(release_date):
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

if __name__ == "__main__":
    ensure_visualization_data() 