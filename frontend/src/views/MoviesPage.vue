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
          <img :src="movie.poster_url" :alt="movie.title" class="w-full h-full object-cover">
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