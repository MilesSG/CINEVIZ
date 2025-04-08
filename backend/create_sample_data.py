import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.movie import Movie
import random
from datetime import datetime, timedelta

def create_sample_movies():
    # 清空现有数据
    movies = Movie.get_all_movies()
    for movie in movies:
        Movie.delete(movie.id)
        print(f"删除电影: {movie.title}")
    
    # 示例电影标题
    titles = [
        "星际迷航", "赛博朋克", "流浪地球", "复仇者联盟", "速度与激情",
        "蜘蛛侠：英雄远征", "哥斯拉", "金刚", "泰坦尼克号", "阿凡达",
        "黑客帝国", "指环王", "哈利波特", "变形金刚", "加勒比海盗"
    ]
    
    # 示例导演
    directors = ["詹姆斯·卡梅隆", "克里斯托弗·诺兰", "彼得·杰克逊", "罗伯特·泽米吉斯", "史蒂文·斯皮尔伯格"]
    
    # 示例演员
    actors_pool = ["汤姆·克鲁斯", "布拉德·皮特", "莱昂纳多·迪卡普里奥", "罗伯特·唐尼", "克里斯·埃文斯", 
                 "斯嘉丽·约翰逊", "娜塔莉·波特曼", "安妮·海瑟薇", "凯特·布兰切特", "艾玛·沃森"]
    
    # 示例电影类型
    genres_options = [
        ["动作", "科幻"], 
        ["喜剧", "爱情"], 
        ["动画", "家庭"], 
        ["恐怖", "惊悚"], 
        ["剧情", "历史"]
    ]
    
    # 创建15部示例电影
    for i in range(15):
        # 随机选择标题
        title = titles[i % len(titles)]
        
        # 随机设置上映日期
        days_ago = random.randint(1, 365)
        release_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # 随机设置导演
        director = random.choice(directors)
        
        # 随机选择2-3名演员
        num_actors = random.randint(2, 3)
        actors = random.sample(actors_pool, num_actors)
        
        # 随机选择类型
        genres = random.choice(genres_options)
        
        # 随机设置票房（1千万 到 5亿之间）
        box_office = random.randint(10000000, 500000000)
        
        # 随机设置评分（7.0-9.5之间）
        rating = round(random.uniform(7.0, 9.5), 1)
        
        # 设置海报URL
        poster_url = f"https://picsum.photos/300/450?random={i+1}"
        
        # 创建电影对象
        movie = Movie(
            title=title,
            release_date=release_date,
            genres=genres,
            director=director,
            actors=actors,
            poster_url=poster_url,
            box_office=box_office,
            rating=rating
        )
        
        # 保存电影数据
        movie.save()
        print(f"已创建电影: {movie.title}")

if __name__ == "__main__":
    create_sample_movies()
    print("样本数据创建完成！") 