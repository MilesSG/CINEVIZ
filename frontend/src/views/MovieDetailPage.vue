<template>
  <div class="container mx-auto px-4 py-8">
    <!-- 加载状态 -->
    <div v-if="moviesStore.loading" class="py-20 text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">加载中...</p>
    </div>
    
    <!-- 无数据 -->
    <div v-else-if="!movie" class="py-20 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-xl text-gray-600 dark:text-gray-400">未找到电影信息</p>
      <div class="mt-6">
        <router-link to="/movies" class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">
          返回电影列表
        </router-link>
      </div>
    </div>
    
    <!-- 电影详情 -->
    <div v-else>
      <!-- 返回链接 -->
      <div class="mb-6">
        <router-link to="/movies" class="inline-flex items-center text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
          </svg>
          返回电影列表
        </router-link>
      </div>
      
      <!-- 电影基本信息 -->
      <div class="flex flex-col md:flex-row gap-8 mb-12">
        <!-- 电影海报 -->
        <div class="w-full md:w-1/3 lg:w-1/4">
          <div class="rounded-lg overflow-hidden bg-gray-200 dark:bg-gray-700 shadow-md">
            <img :src="movie.poster_url" :alt="movie.title" class="w-full h-auto">
          </div>
          
          <!-- 收藏按钮 -->
          <div v-if="authStore.isLoggedIn" class="mt-4">
            <button 
              @click="toggleFavorite"
              :disabled="favoriteLoading"
              class="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              :class="isFavorite ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'"
            >
              <svg v-if="isFavorite" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              {{ isFavorite ? "已收藏" : "收藏电影" }}
            </button>
          </div>
        </div>
        
        <!-- 电影信息 -->
        <div class="flex-1">
          <div class="flex justify-between items-start">
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">{{ movie.title }}</h1>
            <div class="bg-yellow-500 text-white px-3 py-1 rounded-full text-sm font-bold">
              {{ movie.rating.toFixed(1) }}
            </div>
          </div>
          
          <div class="mt-4 space-y-4">
            <div>
              <span class="text-gray-600 dark:text-gray-400">上映日期：</span>
              <span class="text-gray-900 dark:text-white">{{ movie.release_date }}</span>
            </div>
            
            <div>
              <span class="text-gray-600 dark:text-gray-400">导演：</span>
              <span class="text-gray-900 dark:text-white">{{ movie.director }}</span>
            </div>
            
            <div>
              <span class="text-gray-600 dark:text-gray-400">主演：</span>
              <span class="text-gray-900 dark:text-white">{{ movie.actors.join('、') }}</span>
            </div>
            
            <div>
              <span class="text-gray-600 dark:text-gray-400">类型：</span>
              <div class="inline-flex flex-wrap gap-2 mt-1">
                <span v-for="genre in movie.genres" :key="genre" class="px-2 py-1 text-xs bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300 rounded">
                  {{ genre }}
                </span>
              </div>
            </div>
            
            <div>
              <span class="text-gray-600 dark:text-gray-400">总票房：</span>
              <span class="text-xl font-bold text-blue-600 dark:text-blue-400">{{ formatBoxOffice(movie.box_office) }}元</span>
            </div>
            
            <div v-if="movie.description">
              <p class="text-gray-600 dark:text-gray-400 mt-4">{{ movie.description }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 票房趋势图 -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">票房走势</h2>
        <div class="h-64 sm:h-80">
          <!-- 这里放入票房走势图表 -->
          <div v-if="!hasDailyBoxOffice" class="h-full flex items-center justify-center">
            <p class="text-gray-500 dark:text-gray-400">暂无日票房数据</p>
          </div>
          <div v-else class="h-full">
            <!-- 票房趋势图将在后续实现 -->
            <p class="text-center text-gray-500 dark:text-gray-400">票房趋势图组件将在此处显示</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useMoviesStore } from '../stores/movies'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const moviesStore = useMoviesStore()
const authStore = useAuthStore()
const favoriteLoading = ref(false)

// 从路由参数中获取电影ID
const movieId = route.params.id

// 获取电影信息
const movie = computed(() => moviesStore.movie)

// 判断是否已收藏
const isFavorite = computed(() => {
  if (!authStore.isLoggedIn || !authStore.user) return false
  return authStore.user.favorites.includes(movieId)
})

// 检查是否有日票房数据
const hasDailyBoxOffice = computed(() => {
  if (!movie.value) return false
  return Object.keys(movie.value.daily_box_office || {}).length > 0
})

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

// 切换收藏状态
const toggleFavorite = async () => {
  if (!authStore.isLoggedIn) return
  
  favoriteLoading.value = true
  await authStore.toggleFavorite(movieId)
  favoriteLoading.value = false
}

onMounted(async () => {
  // 加载电影详情
  await moviesStore.fetchMovie(movieId)
})
</script> 