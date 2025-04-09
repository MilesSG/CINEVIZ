import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.movie import Movie
import random
from datetime import datetime, timedelta

def update_movies_with_daily_box_office():
    """为现有电影添加日票房数据"""
    movies = Movie.get_all_movies()
    updated_count = 0
    
    for movie in movies:
        # 如果电影已有日票房数据且不为空，则跳过
        if movie.daily_box_office and len(movie.daily_box_office) > 0:
            print(f"跳过已有日票房数据的电影: {movie.title}")
            continue
        
        # 生成日票房数据
        daily_box_office = generate_daily_box_office(movie.release_date)
        
        # 更新电影对象
        movie.daily_box_office = daily_box_office
        movie.save()
        
        updated_count += 1
        print(f"已添加日票房数据: {movie.title}")
    
    print(f"更新完成! 共更新了 {updated_count} 部电影的日票房数据。")

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
    update_movies_with_daily_box_office() 