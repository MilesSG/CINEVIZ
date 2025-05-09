import os
import requests
import json
import time

# 电影名称和对应的海报URL（使用固定的免费电影海报）
MOVIE_POSTERS = {
    # 已有海报的电影，使用百度图片的稳定URL
    '星际迷航': 'https://img0.baidu.com/it/u=3594259173,1810583199&fm=253&fmt=auto&app=138&f=JPEG',
    '赛博朋克': 'https://img1.baidu.com/it/u=2069119965,1991726058&fm=253&fmt=auto&app=138&f=JPEG',
    '流浪地球': 'https://img0.baidu.com/it/u=2150359035,2022815417&fm=253&fmt=auto&app=138&f=JPEG',
    '复仇者联盟': 'https://img0.baidu.com/it/u=2947473013,935097662&fm=253&fmt=auto&app=138&f=JPEG',
    '速度与激情': 'https://img2.baidu.com/it/u=3482389333,286386604&fm=253&fmt=auto&app=138&f=JPEG',
    '蜘蛛侠：英雄远征': 'https://img2.baidu.com/it/u=2142116236,1280835564&fm=253&fmt=auto&app=138&f=JPEG',
    '哥斯拉': 'https://img1.baidu.com/it/u=3290906231,4150989133&fm=253&fmt=auto&app=120&f=JPEG',
    '金刚': 'https://img1.baidu.com/it/u=1633061516,1728751475&fm=253&fmt=auto&app=138&f=JPEG',
    '泰坦尼克号': 'https://img2.baidu.com/it/u=1239733638,2544093761&fm=253&fmt=auto&app=138&f=JPEG',
    '阿凡达': 'https://img1.baidu.com/it/u=2452311496,2590543232&fm=253&fmt=auto&app=138&f=JPEG',
    '黑客帝国': 'https://img0.baidu.com/it/u=2947522482,4212854693&fm=253&fmt=auto&app=138&f=JPEG',
    '指环王': 'https://img0.baidu.com/it/u=663865102,1793825488&fm=253&fmt=auto&app=138&f=JPEG',
    '哈利波特': 'https://img2.baidu.com/it/u=1505944318,1743179317&fm=253&fmt=auto&app=138&f=JPEG',
    '变形金刚': 'https://img0.baidu.com/it/u=2913455198,2387172547&fm=253&fmt=auto&app=138&f=JPEG',
    '加勒比海盗': 'https://img2.baidu.com/it/u=1273221633,3364387294&fm=253&fmt=auto&app=138&f=JPEG',
    '疯狂动物城': 'https://img1.baidu.com/it/u=3538088461,4153752156&fm=253&fmt=auto&app=138&f=JPEG',
    '寻梦环游记': 'https://img2.baidu.com/it/u=3626444295,1205655564&fm=253&fmt=auto&app=138&f=JPEG',
    '千与千寻': 'https://img0.baidu.com/it/u=367133725,3606407286&fm=253&fmt=auto&app=138&f=JPEG',
    '龙猫': 'https://img1.baidu.com/it/u=1307135071,3093290605&fm=253&fmt=auto&app=138&f=JPEG',
    '你的名字': 'https://img1.baidu.com/it/u=2960302410,1606366633&fm=253&fmt=auto&app=138&f=JPEG',
    '楚门的世界': 'https://img0.baidu.com/it/u=1202511879,1695938052&fm=253&fmt=auto&app=138&f=JPEG',
    '肖申克的救赎': 'https://img1.baidu.com/it/u=3178833115,3706232922&fm=253&fmt=auto&app=138&f=JPEG',
    '盗梦空间': 'https://img1.baidu.com/it/u=2987323214,3693118789&fm=253&fmt=auto&app=138&f=JPEG',
    '星球大战': 'https://img1.baidu.com/it/u=2123888639,3738621483&fm=253&fmt=auto&app=138&f=JPEG',
    '霸王别姬': 'https://img0.baidu.com/it/u=3268222082,2313011080&fm=253&fmt=auto&app=120&f=JPEG',
    '这个杀手不太冷': 'https://img1.baidu.com/it/u=3953407776,1781685932&fm=253&fmt=auto&app=138&f=JPEG',
    '头号玩家': 'https://img1.baidu.com/it/u=2635070306,4179841456&fm=253&fmt=auto&app=138&f=JPEG',
    '鬼灭之刃': 'https://img2.baidu.com/it/u=1782376139,1103625768&fm=253&fmt=auto&app=138&f=JPEG',
    '未来水世界': 'https://img0.baidu.com/it/u=3272407199,3405578601&fm=253&fmt=auto&app=138&f=JPEG',
    '异形': 'https://img0.baidu.com/it/u=984462264,234321979&fm=253&fmt=auto&app=138&f=JPEG',
    # 添加更多常见电影
    '中国机长': 'https://img0.baidu.com/it/u=3583476011,2813215227&fm=253&fmt=auto&app=138&f=JPEG',
    '战狼': 'https://img2.baidu.com/it/u=1395980100,2775174872&fm=253&fmt=auto&app=120&f=JPEG',
    '长津湖': 'https://img2.baidu.com/it/u=159394734,690522195&fm=253&fmt=auto&app=138&f=JPEG',
    '我和我的祖国': 'https://img1.baidu.com/it/u=4223471627,3987326421&fm=253&fmt=auto&app=138&f=JPEG',
    '囧妈': 'https://img0.baidu.com/it/u=1051426642,2519583608&fm=253&fmt=auto&app=138&f=JPEG',
    '哪吒之魔童降世': 'https://img1.baidu.com/it/u=1823583302,3518913515&fm=253&fmt=auto&app=138&f=JPEG',
    '唐人街探案': 'https://img1.baidu.com/it/u=3264901532,1375302991&fm=253&fmt=auto&app=138&f=JPEG',
    '红海行动': 'https://img0.baidu.com/it/u=1434863262,2391328588&fm=253&fmt=auto&app=138&f=JPEG',
    '建国大业': 'https://img0.baidu.com/it/u=3414549688,3303865009&fm=253&fmt=auto&app=138&f=JPEG',
    '夏洛特烦恼': 'https://img0.baidu.com/it/u=2832348802,4153779224&fm=253&fmt=auto&app=138&f=JPEG'
}

# 创建保存路径
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

# 确保目录存在
os.makedirs(SAVE_DIR, exist_ok=True)

# 下载图片
def download_image(title, image_url):
    try:
        # 处理文件名
        file_name = f"{title.replace(':', '_').replace(' ', '_').replace('：', '_')}.jpg"
        image_path = os.path.join(SAVE_DIR, file_name)
        
        # 检查文件是否已存在
        if os.path.exists(image_path):
            print(f"图片已存在: {title}")
            return {
                'title': title,
                'local_path': f"/posters/{file_name}"
            }
        
        # 添加请求头，模拟浏览器行为
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 下载图片
        response = requests.get(image_url, headers=headers, timeout=15)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"下载成功: {title}")
            return {
                'title': title,
                'local_path': f"/posters/{file_name}"
            }
        else:
            print(f"下载失败: {title} - 状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"下载出错: {title} - {str(e)}")
        return None

# 创建默认海报
def create_default_poster():
    default_path = os.path.join(SAVE_DIR, "default-poster.jpg")
    
    # 如果默认海报已存在，跳过
    if os.path.exists(default_path):
        print("默认海报已存在")
        return
    
    # 使用一个通用的电影图标URL
    default_url = "https://img0.baidu.com/it/u=3113421026,688445206&fm=253&fmt=auto&app=138&f=JPEG"
    
    try:
        response = requests.get(default_url, timeout=15)
        if response.status_code == 200:
            with open(default_path, 'wb') as f:
                f.write(response.content)
            print("创建默认海报成功")
        else:
            print(f"创建默认海报失败: 状态码 {response.status_code}")
    except Exception as e:
        print(f"创建默认海报出错: {str(e)}")

# 主函数
def main():
    movie_posters = {}
    
    # 创建默认海报
    create_default_poster()
    
    # 下载每个电影的海报
    for title, poster_url in MOVIE_POSTERS.items():
        result = download_image(title, poster_url)
        if result:
            movie_posters[result['title']] = result['local_path']
        
        # 请求间隔，避免被网站封锁
        time.sleep(0.5)
    
    # 保存映射关系到JSON文件
    with open(os.path.join(SAVE_DIR, 'poster_map.json'), 'w', encoding='utf-8') as f:
        json.dump(movie_posters, f, ensure_ascii=False, indent=2)
    
    print(f"完成! 已下载 {len(movie_posters)} 张海报。")
    print(f"海报映射文件已保存到 {os.path.join(SAVE_DIR, 'poster_map.json')}")

if __name__ == "__main__":
    main() 