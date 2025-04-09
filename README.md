# 🎬 CineViz - 影视票房数据可视化系统

CineViz是一个基于Python和Vue.js的影视票房数据可视化系统，提供电影数据采集、存储、分析和展示功能，支持用户管理、数据可视化和管理员后台等多种功能。

![系统运行截图](frontend/imgs/image.png)

## ✨ 功能特点

- 🎨 现代美观的网页应用，支持深色模式
- 💾 使用本地JSON文件进行数据存储，无需数据库
- 📊 丰富的数据可视化功能：票房走势、类型对比、发布热图等
- 👤 用户系统：登录、注册、个人中心、收藏功能
- 🔧 管理员后台：数据管理、用户管理、爬虫控制等

## 🛠️ 技术栈

### 后端
- 🐍 Python 3.8+
- 🌶️ Flask
- 🔑 JWT认证
- 🕸️ BeautifulSoup4（数据爬虫）
- 📈 Plotly/Pandas（数据处理）

### 前端
- ⚡ Vue 3
- 🚀 Vite
- 🧭 Vue Router
- 📦 Pinia
- 🎨 Tailwind CSS
- 📊 ECharts/Chart.js（可视化图表）

## 🚀 快速开始

### 环境准备
确保已安装Python 3.8+和Node.js 14+

### 后端设置
```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建数据（首次运行时需要）
python create_sample_data.py

# 运行服务器（必须在backend目录下运行）
python run.py
```

### 前端设置
```bash
# 新开一个终端，进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 注意事项
- 后端服务器必须在backend目录下运行，不能在项目根目录运行
- 首次使用需要创建示例数据，否则前端将无法显示数据
- 前后端需要同时运行，建议使用两个终端窗口

## 📁 项目结构

```
CineViz/
├── backend/               # 后端文件夹
│   ├── app/               # Flask应用
│   │   ├── models/        # 数据模型
│   │   ├── routes/        # API路由
│   │   ├── services/      # 业务逻辑服务
│   │   ├── static/        # 静态文件
│   │   ├── templates/     # 模板文件
│   │   └── utils/         # 工具函数
│   ├── data/              # JSON数据存储
│   └── requirements.txt   # Python依赖
│
├── frontend/              # 前端文件夹
│   ├── public/            # 公共资源
│   ├── src/               # 源代码
│   │   ├── assets/        # 静态资源
│   │   ├── components/    # 通用组件
│   │   ├── router/        # 路由配置
│   │   ├── stores/        # 状态管理
│   │   ├── services/      # API服务
│   │   ├── utils/         # 工具函数
│   │   └── views/         # 页面视图
│   ├── package.json       # NPM配置
│   └── vite.config.js     # Vite配置
│
└── README.md              # 项目说明
```

## 📌 主要功能模块

### 1. 🕷️ 数据采集模块
- 从猫眼电影等网站爬取电影数据
- 数据清洗和标准化处理
- 存储为JSON格式文件

### 2. 🖥️ 用户界面
- 现代化仪表盘设计
- 响应式布局，适配各种设备
- 深色/浅色模式切换

### 3. 📊 可视化组件
- 票房走势折线图
- 不同类别电影对比柱状图
- 电影发行时间热力图
- 票房分布图

### 4. 👥 用户系统
- 注册和登录功能
- 个人信息管理
- 电影收藏功能

### 5. 👨‍💼 管理员功能
- 电影数据管理（增删改查）
- 用户管理
- 爬虫控制
- 统计报表

## 📝 数据来源
系统通过爬虫从猫眼电影等网站获取公开的电影信息和票房数据，仅用于学习和研究目的。

## 📄 许可
本项目仅供个人学习和研究使用，不得用于商业目的。 
