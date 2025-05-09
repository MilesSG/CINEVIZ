<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-4 md:mb-0">电影库</h1>
      
      <!-- 搜索和筛选 -->
      <div class="w-full md:w-auto flex flex-col sm:flex-row gap-4">
        <div class="relative flex-grow">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="搜索电影..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
            @keyup.enter="handleSearch"
          />
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
        
        <select
          v-model="selectedGenre"
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
          @change="handleGenreChange"
        >
          <option value="">所有类型</option>
          <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
        </select>
        
        <button
          @click="clearFilters"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:bg-gray-600"
        >
          清除筛选
        </button>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="moviesStore.loading" class="py-20 text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">加载中...</p>
    </div>
    
    <!-- 无结果 -->
    <div v-else-if="moviesStore.movies.length === 0" class="py-20 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
      </svg>
      <p class="text-xl text-gray-600 dark:text-gray-400">没有找到电影</p>
      <p class="mt-2 text-gray-500 dark:text-gray-500">请尝试其他搜索条件或清除筛选</p>
    </div>
    
    <!-- 电影网格 -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <div v-for="movie in moviesStore.movies" :key="movie.id" class="bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300">
        <div class="relative h-64 overflow-hidden bg-gray-200 dark:bg-gray-700">
          <img 
            :src="movie.poster_url" 
            :alt="movie.title" 
            class="w-full h-full object-cover"
            @error="handleImageError($event, movie.title)"
          >
          <div class="absolute top-0 right-0 m-2 px-2 py-1 bg-yellow-500 text-white text-xs font-bold rounded">
            {{ movie.rating.toFixed(1) }}
          </div>
        </div>
        <div class="p-4">
          <router-link :to="`/movies/${movie.id}`" class="text-lg font-bold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 line-clamp-1">
            {{ movie.title }}
          </router-link>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ movie.release_date }}</p>
          <div class="flex flex-wrap gap-1 mt-2">
            <span v-for="genre in movie.genres" :key="genre" class="px-2 py-1 text-xs bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300 rounded">
              {{ genre }}
            </span>
          </div>
          <div class="mt-3 text-sm">
            <span class="text-gray-700 dark:text-gray-300">票房:</span>
            <span class="font-medium text-blue-600 dark:text-blue-400 ml-1">{{ formatBoxOffice(movie.box_office) }}元</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useMoviesStore } from '../stores/movies'

const moviesStore = useMoviesStore()

const searchQuery = ref('')
const selectedGenre = ref('')
const genres = ref([])

// 处理图片加载失败
const handleImageError = (event, title) => {
  console.error('海报加载失败:', title)
  
  // 创建文件名映射，解决特殊字符问题
  const fileNameMap = {
    '蜘蛛侠：英雄远征': '蜘蛛侠_英雄远征'
  };
  
  // 处理特殊文件名
  const fixedTitle = fileNameMap[title] || title;
  
  // 尝试直接使用本地文件
  let newSrc = `/posters/${fixedTitle}.jpg`;
  
  // 使用备用URL映射中的URL（如果有）
  const backupUrls = {
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
  
  // 如果图片加载再次失败，使用备用URL
  event.target.onerror = () => {
    // 尝试使用在线备用URL
    if (backupUrls[title]) {
      event.target.src = backupUrls[title]
      return
    }
    
    // 最后使用占位符图片
    event.target.onerror = null // 防止无限循环
    event.target.src = `https://via.placeholder.com/300x450.png?text=${encodeURIComponent(title)}`
  }
  
  event.target.src = newSrc
}

// 格式化票房数据
const formatBoxOffice = (value) => {
  if (!value) return '0'
  
  // 转换为亿或万
  if (value >= 100000000) {
    return (value / 100000000).toFixed(2) + '亿'
  } else if (value >= 10000) {
    return (value / 10000).toFixed(2) + '万'
  }
  
  return value.toString()
}

// 搜索电影
const handleSearch = () => {
  moviesStore.setSearchQuery(searchQuery.value)
  moviesStore.fetchMovies()
}

// 切换类型
const handleGenreChange = () => {
  moviesStore.setSelectedGenre(selectedGenre.value)
  moviesStore.fetchMovies()
}

// 清除筛选条件
const clearFilters = () => {
  searchQuery.value = ''
  selectedGenre.value = ''
  moviesStore.clearFilters()
  moviesStore.fetchMovies()
}

// 监听搜索词变化
watch(searchQuery, (newValue, oldValue) => {
  if (newValue === '' && oldValue !== '') {
    moviesStore.setSearchQuery('')
    moviesStore.fetchMovies()
  }
})

onMounted(async () => {
  // 获取电影列表
  if (moviesStore.movies.length === 0) {
    await moviesStore.fetchMovies()
  }
  
  // 获取所有电影类型
  if (moviesStore.genres.length === 0) {
    await moviesStore.fetchGenres()
    genres.value = moviesStore.genres
  } else {
    genres.value = moviesStore.genres
  }
})
</script> 