import os
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

# 电影名称列表 - 与电影库页面中的电影标题对应
MOVIE_TITLES = [
    '星际迷航', '赛博朋克', '流浪地球', '复仇者联盟', '速度与激情', 
    '蜘蛛侠：英雄远征', '哥斯拉', '金刚', '泰坦尼克号', '阿凡达', 
    '黑客帝国', '指环王', '哈利波特', '变形金刚', '加勒比海盗',
    '疯狂动物城', '寻梦环游记', '千与千寻', '龙猫', '你的名字',
    '楚门的世界', '肖申克的救赎', '盗梦空间', '星球大战', '霸王别姬',
    '这个杀手不太冷', '头号玩家', '鬼灭之刃', '未来水世界', '异形'
]

# 电影英文名称映射（辅助搜索）
MOVIE_EN_NAMES = {
    '星际迷航': 'Star Trek',
    '赛博朋克': 'Cyberpunk',
    '流浪地球': 'The Wandering Earth',
    '复仇者联盟': 'Avengers',
    '速度与激情': 'Fast and Furious',
    '蜘蛛侠：英雄远征': 'Spider-Man: Far From Home',
    '哥斯拉': 'Godzilla',
    '金刚': 'King Kong',
    '泰坦尼克号': 'Titanic',
    '阿凡达': 'Avatar',
    '黑客帝国': 'The Matrix',
    '指环王': 'The Lord of the Rings',
    '哈利波特': 'Harry Potter',
    '变形金刚': 'Transformers',
    '加勒比海盗': 'Pirates of the Caribbean',
    '疯狂动物城': 'Zootopia',
    '寻梦环游记': 'Coco',
    '千与千寻': 'Spirited Away',
    '龙猫': 'My Neighbor Totoro',
    '你的名字': 'Your Name',
    '楚门的世界': 'The Truman Show',
    '肖申克的救赎': 'The Shawshank Redemption',
    '盗梦空间': 'Inception',
    '星球大战': 'Star Wars',
    '霸王别姬': 'Farewell My Concubine',
    '这个杀手不太冷': 'Léon: The Professional',
    '头号玩家': 'Ready Player One',
    '鬼灭之刃': 'Demon Slayer',
    '未来水世界': 'Waterworld',
    '异形': 'Alien'
}

# TMDB API配置（如果你有API Key可以替换这个）
TMDB_API_KEY = "3e937c74a80af3ff53567527d379ebed"  # 请替换成你自己的API Key
TMDB_API_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"  # 海报尺寸w500

# 创建保存路径
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

# 确保目录存在
os.makedirs(SAVE_DIR, exist_ok=True)

# 搜索电影并获取海报URL
def search_movie_and_get_poster(movie_title):
    # 先尝试中文搜索
    search_url = f"{TMDB_API_URL}/search/movie?api_key={TMDB_API_KEY}&language=zh-CN&query={movie_title}&page=1&include_adult=false"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            # 找到匹配的电影
            movie = results[0]
            poster_path = movie.get('poster_path')
            if poster_path:
                return {
                    'title': movie_title,
                    'poster_url': f"{TMDB_IMAGE_BASE_URL}{poster_path}",
                    'file_name': f"{movie_title.replace(':', '_').replace(' ', '_').replace('：', '_')}.jpg"
                }
    
    # 如果中文搜索失败，尝试英文搜索
    if movie_title in MOVIE_EN_NAMES:
        en_title = MOVIE_EN_NAMES[movie_title]
        search_url = f"{TMDB_API_URL}/search/movie?api_key={TMDB_API_KEY}&language=en-US&query={en_title}&page=1&include_adult=false"
        response = requests.get(search_url)
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                # 找到匹配的电影
                movie = results[0]
                poster_path = movie.get('poster_path')
                if poster_path:
                    return {
                        'title': movie_title,
                        'poster_url': f"{TMDB_IMAGE_BASE_URL}{poster_path}",
                        'file_name': f"{movie_title.replace(':', '_').replace(' ', '_').replace('：', '_')}.jpg"
                    }
    
    # 都失败了，返回空
    return None

# 下载图片
def download_image(poster_info):
    if not poster_info:
        return None
    
    try:
        image_path = os.path.join(SAVE_DIR, poster_info['file_name'])
        
        # 检查文件是否已存在
        if os.path.exists(image_path):
            print(f"图片已存在: {poster_info['title']}")
            return {
                'title': poster_info['title'],
                'local_path': f"/posters/{poster_info['file_name']}"
            }
        
        # 下载图片
        response = requests.get(poster_info['poster_url'])
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"下载成功: {poster_info['title']}")
            return {
                'title': poster_info['title'],
                'local_path': f"/posters/{poster_info['file_name']}"
            }
        else:
            print(f"下载失败: {poster_info['title']} - 状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"下载出错: {poster_info['title']} - {str(e)}")
        return None

# 使用备用图片（如果API获取失败）
def get_backup_poster_map():
    # 这里使用一些免费的电影海报链接作为备用
    backup_map = {
        '星际迷航': 'https://www.themoviedb.org/t/p/w500/2sTGKIKK4qNnoHPFR3RFg2kWvRp.jpg',
        '复仇者联盟': 'https://www.themoviedb.org/t/p/w500/qMxAmzGQO722q0UlssCOPhrXmvX.jpg',
        '阿凡达': 'https://www.themoviedb.org/t/p/w500/kyeqWdyUXW608qlYkRqosgbbJyK.jpg',
        '黑客帝国': 'https://www.themoviedb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg',
        '肖申克的救赎': 'https://www.themoviedb.org/t/p/w500/lyQBXzOQSuE59IsHyhrp0qIiPAz.jpg',
        '星球大战': 'https://www.themoviedb.org/t/p/w500/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg',
    }
    return backup_map

# 主函数
def main():
    movie_posters = {}
    backup_map = get_backup_poster_map()
    
    # 使用线程池加速下载
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 搜索并获取海报信息
        poster_infos = []
        for title in MOVIE_TITLES:
            poster_info = search_movie_and_get_poster(title)
            if poster_info:
                poster_infos.append(poster_info)
            else:
                # 尝试使用备用海报
                if title in backup_map:
                    poster_infos.append({
                        'title': title,
                        'poster_url': backup_map[title],
                        'file_name': f"{title.replace(':', '_').replace(' ', '_').replace('：', '_')}.jpg"
                    })
                    print(f"使用备用海报: {title}")
                else:
                    print(f"未找到海报: {title}")
            
            # 请求间隔，避免API限制
            time.sleep(0.5)
        
        # 下载海报
        results = list(executor.map(download_image, poster_infos))
        
        # 生成映射关系
        for result in results:
            if result:
                movie_posters[result['title']] = result['local_path']
    
    # 保存映射关系到JSON文件
    with open(os.path.join(SAVE_DIR, 'poster_map.json'), 'w', encoding='utf-8') as f:
        json.dump(movie_posters, f, ensure_ascii=False, indent=2)
    
    print(f"完成! 已下载 {len(movie_posters)} 张海报。")
    print(f"海报映射文件已保存到 {os.path.join(SAVE_DIR, 'poster_map.json')}")

if __name__ == "__main__":
    main() 