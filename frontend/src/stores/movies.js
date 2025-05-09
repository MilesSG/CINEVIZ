import { defineStore } from 'pinia'
import { getMoviePosterUrl } from './moviePosters'

// 模拟数据生成
const mockGenres = ['科幻', '动作', '剧情', '喜剧', '爱情', '恐怖', '动画', '冒险', '悬疑', '奇幻']

// 实际已下载的电影海报列表（所有海报都已下载成功）
const availablePosters = [
  '星际迷航', '赛博朋克', '流浪地球', '复仇者联盟', '速度与激情', 
  '蜘蛛侠：英雄远征', '哥斯拉', '金刚', '泰坦尼克号', '阿凡达', 
  '黑客帝国', '指环王', '哈利波特', '变形金刚', '加勒比海盗',
  '疯狂动物城', '寻梦环游记', '千与千寻', '龙猫', '你的名字',
  '楚门的世界', '肖申克的救赎', '盗梦空间', '星球大战', '霸王别姬',
  '这个杀手不太冷', '头号玩家', '鬼灭之刃', '未来水世界', '异形',
  '中国机长', '战狼', '长津湖', '我和我的祖国', '囧妈',
  '哪吒之魔童降世', '唐人街探案', '红海行动', '建国大业', '夏洛特烦恼'
]

// 备用在线URL
const backupImageUrls = {
  '星际迷航': 'https://img.enmuo.com/2017/12/27/15142736012633.jpg',
  '赛博朋克': 'https://img.enmuo.com/2018/11/29/15435179617654.jpg',
  '流浪地球': 'https://img.enmuo.com/2019/05/08/15573069518151.jpg',
  '复仇者联盟': 'https://img.enmuo.com/2018/05/24/15271560895430.jpg',
  '速度与激情': 'https://img.enmuo.com/2017/05/17/14950303417844.jpg',
  '蜘蛛侠：英雄远征': 'https://img.enmuo.com/2019/08/28/15669641326232.jpg',
  '哥斯拉': 'https://img.enmuo.com/2019/08/01/15647119728834.jpg',
  '金刚': 'https://img.enmuo.com/2018/05/16/15264986517911.jpg',
  '泰坦尼克号': 'https://img.enmuo.com/2018/03/27/15221658885967.jpg',
  '阿凡达': 'https://img.enmuo.com/2018/02/08/15180898513661.jpg',
  '黑客帝国': 'https://img.enmuo.com/2018/05/23/15270637717450.jpg',
  '指环王': 'https://img.enmuo.com/2018/05/16/15264999128559.jpg',
  '哈利波特': 'https://img.enmuo.com/2018/05/15/15264129327661.jpg',
  '变形金刚': 'https://img.enmuo.com/2018/05/15/15264068555830.jpg',
  '加勒比海盗': 'https://img.enmuo.com/2018/05/22/15269808197279.jpg',
  '疯狂动物城': 'https://img.enmuo.com/2018/05/22/15269764126640.jpg',
  '寻梦环游记': 'https://img.enmuo.com/2018/05/22/15269746025909.jpg',
  '千与千寻': 'https://img.enmuo.com/2018/03/06/15203315535687.jpg',
  '龙猫': 'https://img.enmuo.com/2018/05/22/15269742016639.jpg',
  '你的名字': 'https://img.enmuo.com/2017/08/22/15033963008466.jpg',
  '楚门的世界': 'https://img.enmuo.com/2017/12/12/15130351396026.jpg',
  '肖申克的救赎': 'https://img.enmuo.com/2018/05/16/15264938317142.jpg',
  '盗梦空间': 'https://img.enmuo.com/2018/05/15/15264118225780.jpg',
  '星球大战': 'https://img.enmuo.com/2018/05/30/15276673535711.jpg',
  '霸王别姬': 'https://img.enmuo.com/2018/03/27/15221650626325.jpg',
  '这个杀手不太冷': 'https://img.enmuo.com/2018/05/15/15264061876339.jpg',
  '头号玩家': 'https://img.enmuo.com/2018/05/15/15264069325892.jpg',
  '鬼灭之刃': 'https://img.enmuo.com/2020/11/05/16045848315344.jpg',
  '未来水世界': 'https://img.enmuo.com/2017/09/10/15049938205954.jpg',
  '异形': 'https://img.enmuo.com/2018/05/16/15264966517177.jpg',
  '中国机长': 'https://img.enmuo.com/2019/12/30/15776988816455.jpg',
  '战狼': 'https://img.enmuo.com/2018/05/15/15263999026175.jpg',
  '长津湖': 'https://img.enmuo.com/2022/02/15/16448691726673.jpg',
  '我和我的祖国': 'https://img.enmuo.com/2019/11/14/15736753718234.jpg',
  '囧妈': 'https://img.enmuo.com/2020/05/04/15886031913343.jpg',
  '哪吒之魔童降世': 'https://img.enmuo.com/2019/09/26/15695055018732.jpg',
  '唐人街探案': 'https://img.enmuo.com/2018/05/15/15264000696278.jpg',
  '红海行动': 'https://img.enmuo.com/2018/05/15/15264000116229.jpg',
  '建国大业': 'https://img.enmuo.com/2018/05/15/15263999726150.jpg',
  '夏洛特烦恼': 'https://img.enmuo.com/2018/05/15/15264000666273.jpg'
}

// 优化的海报URL获取函数
function getOptimizedPosterUrl(title) {
  // 创建文件名映射，解决特殊字符问题
  const fileNameMap = {
    '蜘蛛侠：英雄远征': '蜘蛛侠_英雄远征'
  };
  
  // 处理特殊文件名
  const fixedTitle = fileNameMap[title] || title;
  
  // 首先尝试使用本地海报路径
  const localPath = `/posters/${fixedTitle}.jpg`
  
  // 其次使用在线备用URL
  if (backupImageUrls[title]) {
    return backupImageUrls[title]
  }
  
  // 最后使用默认海报
  return localPath
}

// 创建电影标题到海报路径的映射
const posterMap = {}
availablePosters.forEach(title => {
  posterMap[title] = getOptimizedPosterUrl(title)
})

// 使用fetch API来动态获取json文件
let dynamicPosterMap = { ...posterMap }
fetch('/posters/poster_map.json')
  .then(response => {
    if (!response.ok) {
      throw new Error('海报映射文件加载失败')
    }
    return response.json()
  })
  .then(data => {
    // 与备用URL合并，优先使用备用URL
    const mergedData = { ...data, ...backupImageUrls }
    dynamicPosterMap = { ...posterMap, ...mergedData }
    console.log('海报映射文件加载成功', Object.keys(dynamicPosterMap).length)
  })
  .catch(error => {
    console.error('加载海报映射文件失败，使用默认映射', error)
  })

// 模拟电影数据生成函数
function generateMockMovies(count = 30) {
  const movies = []
  
  // 使用所有有海报的电影名称
  const movieTitles = [
    // 原有电影
    '复仇者联盟', '阿凡达', '黑客帝国', '肖申克的救赎', '星球大战',
    '流浪地球', '速度与激情', '哥斯拉', '泰坦尼克号', '指环王',
    '哈利波特', '变形金刚', '加勒比海盗', '疯狂动物城', '寻梦环游记',
    '龙猫', '盗梦空间', '这个杀手不太冷', '头号玩家', '未来水世界',
    // 新增电影
    '星际迷航', '赛博朋克', '金刚', '蜘蛛侠：英雄远征', '千与千寻',
    '你的名字', '楚门的世界', '霸王别姬', '鬼灭之刃', '异形',
    '中国机长', '战狼', '长津湖', '我和我的祖国', '囧妈',
    '哪吒之魔童降世', '唐人街探案', '红海行动', '建国大业', '夏洛特烦恼'
  ]
  
  for (let i = 0; i < count; i++) {
    // 随机生成1-3个类型
    const genreCount = Math.floor(Math.random() * 3) + 1
    const genres = []
    for (let j = 0; j < genreCount; j++) {
      const genre = mockGenres[Math.floor(Math.random() * mockGenres.length)]
      if (!genres.includes(genre)) {
        genres.push(genre)
      }
    }
    
    // 随机生成日期（过去5年内）
    const date = new Date()
    date.setFullYear(date.getFullYear() - Math.floor(Math.random() * 5))
    date.setMonth(Math.floor(Math.random() * 12))
    date.setDate(Math.floor(Math.random() * 28) + 1)
    
    // 随机生成票房（1千万到10亿之间）
    const boxOffice = Math.floor(Math.random() * 990000000) + 10000000
    
    // 随机生成评分（6.0到9.5之间）
    const rating = (Math.random() * 3.5 + 6.0).toFixed(1)
    
    // 获取电影标题（确保不超过电影数量）
    const title = movieTitles[i % movieTitles.length]
    
    // 获取海报URL - 使用优化后的海报URL获取函数
    const posterUrl = getOptimizedPosterUrl(title)
    
    // 随机生成演员列表
    const actors = ['演员A', '演员B', '演员C']
    
    // 创建电影对象
    movies.push({
      id: i + 1,
      title,
      release_date: date.toISOString().split('T')[0],
      genres,
      box_office: boxOffice,
      rating: parseFloat(rating),
      director: '导演' + (i + 1),
      description: '这是一部精彩的电影，讲述了一个引人入胜的故事。',
      poster_url: posterUrl,
      actors
    })
  }
  
  return movies
}

export const useMoviesStore = defineStore('movies', {
  state: () => ({
    movies: [],
    movie: null,
    genres: mockGenres,
    topMovies: [],
    latestMovies: [],
    loading: false,
    error: null,
    searchQuery: '',
    selectedGenre: '',
    totalCount: 0
  }),
  
  getters: {
    getMovieById: (state) => (id) => {
      return state.movies.find(movie => movie.id === parseInt(id)) || null
    }
  },
  
  actions: {
    async fetchMovies(params = {}) {
      this.loading = true
      this.error = null
      
      try {
        // 延迟模拟网络请求
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // 如果电影列表为空，则生成模拟数据
        if (this.movies.length === 0) {
          this.movies = generateMockMovies(30)
        }
        
        let filteredMovies = [...this.movies]
        
        // 应用搜索过滤
        const searchTerm = params.title || this.searchQuery
        if (searchTerm) {
          filteredMovies = filteredMovies.filter(movie => 
            movie.title.toLowerCase().includes(searchTerm.toLowerCase())
          )
        }
        
        // 应用类型过滤
        const genreFilter = params.genre || this.selectedGenre
        if (genreFilter) {
          filteredMovies = filteredMovies.filter(movie => 
            movie.genres.includes(genreFilter)
          )
        }
        
        this.totalCount = filteredMovies.length
        
        return filteredMovies
      } catch (error) {
        this.error = '获取电影列表失败'
        console.error('获取电影列表失败:', error)
        return []
      } finally {
        this.loading = false
      }
    },
    
    async fetchMovie(id) {
      this.loading = true
      this.error = null
      
      try {
        // 延迟模拟网络请求
        await new Promise(resolve => setTimeout(resolve, 300))
        
        // 如果电影列表为空，则生成模拟数据
        if (this.movies.length === 0) {
          await this.fetchMovies()
        }
        
        const movie = this.getMovieById(id)
        
        if (movie) {
          this.movie = movie
          return movie
        } else {
          throw new Error(`未找到ID为${id}的电影`)
        }
      } catch (error) {
        this.error = '获取电影详情失败'
        console.error('获取电影详情失败:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async fetchGenres() {
      this.loading = true
      
      try {
        // 延迟模拟网络请求
        await new Promise(resolve => setTimeout(resolve, 200))
        
        // 已在state中定义了固定的类型列表
        return this.genres
      } catch (error) {
        this.error = '获取电影类型失败'
        console.error('获取电影类型失败:', error)
        return []
      } finally {
        this.loading = false
      }
    },
    
    async fetchTopMovies(limit = 10) {
      this.loading = true
      
      try {
        // 延迟模拟网络请求
        await new Promise(resolve => setTimeout(resolve, 300))
        
        // 如果电影列表为空，则生成模拟数据
        if (this.movies.length === 0) {
          await this.fetchMovies()
        }
        
        // 按票房排序获取前limit部电影
        this.topMovies = [...this.movies]
          .sort((a, b) => b.box_office - a.box_office)
          .slice(0, limit)
        
        return this.topMovies
      } catch (error) {
        this.error = '获取热门电影失败'
        console.error('获取热门电影失败:', error)
        return []
      } finally {
        this.loading = false
      }
    },
    
    async fetchLatestMovies(limit = 8) {
      this.loading = true
      
      try {
        // 延迟模拟网络请求
        await new Promise(resolve => setTimeout(resolve, 300))
        
        // 如果电影列表为空，则生成模拟数据
        if (this.movies.length === 0) {
          await this.fetchMovies()
        }
        
        // 按发行日期排序获取前limit部电影
        this.latestMovies = [...this.movies]
          .sort((a, b) => new Date(b.release_date) - new Date(a.release_date))
          .slice(0, limit)
        
        return this.latestMovies
      } catch (error) {
        this.error = '获取最新电影失败'
        console.error('获取最新电影失败:', error)
        return []
      } finally {
        this.loading = false
      }
    },
    
    setSearchQuery(query) {
      this.searchQuery = query
    },
    
    setSelectedGenre(genre) {
      this.selectedGenre = genre
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.selectedGenre = ''
    }
  }
}) 