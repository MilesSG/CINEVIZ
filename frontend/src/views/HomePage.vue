<template>
  <div>
    <!-- 英雄区域 -->
    <section class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
      <div class="container mx-auto px-4 flex flex-col md:flex-row items-center">
        <div class="md:w-1/2 mb-10 md:mb-0">
          <h1 class="text-4xl md:text-5xl font-bold mb-4">影视票房数据可视化平台</h1>
          <p class="text-xl mb-8">通过数据可视化探索电影票房趋势，获取深度分析洞察</p>
          <div class="flex flex-wrap gap-4">
            <router-link to="/movies" class="bg-white text-blue-600 hover:bg-blue-50 px-6 py-3 rounded-lg font-medium transition-colors">
              浏览电影
            </router-link>
            <router-link to="/charts" class="bg-transparent border-2 border-white hover:bg-white/10 px-6 py-3 rounded-lg font-medium transition-colors">
              查看数据分析
            </router-link>
          </div>
        </div>
        <div class="md:w-1/2 flex justify-center">
          <div class="w-full max-w-md rounded-lg bg-white/10 backdrop-blur-sm p-6 shadow-lg">
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-xl font-bold">热门电影排行</h3>
              <router-link to="/movies" class="text-sm hover:underline">查看更多</router-link>
            </div>
            <div v-if="moviesStore.loading" class="py-10 text-center">
              <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white mx-auto"></div>
              <p class="mt-4">加载中...</p>
            </div>
            <div v-else-if="moviesStore.topMovies.length === 0" class="py-10 text-center">
              <p>暂无电影数据</p>
            </div>
            <ul v-else class="space-y-4">
              <li v-for="(movie, index) in moviesStore.topMovies.slice(0, 5)" :key="movie.id" class="flex items-center gap-4 p-2 rounded-lg hover:bg-white/10 transition-colors">
                <span class="text-lg font-bold w-5">{{ index + 1 }}</span>
                <img :src="movie.poster_url" :alt="movie.title" class="h-16 w-12 object-cover rounded">
                <div class="flex-1 min-w-0">
                  <router-link :to="`/movies/${movie.id}`" class="text-white hover:text-blue-200 font-medium block truncate">
                    {{ movie.title }}
                  </router-link>
                  <div class="text-sm text-blue-200 flex items-center gap-2">
                    <span>票房: {{ formatBoxOffice(movie.box_office) }}元</span>
                    <span>|</span>
                    <span>评分: {{ movie.rating }}</span>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- 功能特点 -->
    <section class="py-16 bg-white dark:bg-gray-800">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12 text-gray-900 dark:text-white">平台特色</h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div class="bg-blue-50 dark:bg-gray-700 rounded-xl p-6 shadow-sm">
            <div class="text-blue-600 dark:text-blue-400 text-3xl mb-4">📊</div>
            <h3 class="text-xl font-bold mb-2 text-gray-900 dark:text-white">多维数据可视化</h3>
            <p class="text-gray-600 dark:text-gray-300">通过图表、热力图等方式直观展示电影票房数据，帮助您快速把握市场趋势</p>
          </div>
          <div class="bg-purple-50 dark:bg-gray-700 rounded-xl p-6 shadow-sm">
            <div class="text-purple-600 dark:text-purple-400 text-3xl mb-4">🔍</div>
            <h3 class="text-xl font-bold mb-2 text-gray-900 dark:text-white">深度数据分析</h3>
            <p class="text-gray-600 dark:text-gray-300">对电影类型、发行日期等因素进行关联分析，发现票房影响因素</p>
          </div>
          <div class="bg-green-50 dark:bg-gray-700 rounded-xl p-6 shadow-sm">
            <div class="text-green-600 dark:text-green-400 text-3xl mb-4">🎬</div>
            <h3 class="text-xl font-bold mb-2 text-gray-900 dark:text-white">最新电影数据</h3>
            <p class="text-gray-600 dark:text-gray-300">及时更新的电影票房数据，让您掌握最新的电影市场动态</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 最新电影区域 -->
    <section class="py-16 bg-gray-50 dark:bg-gray-900">
      <div class="container mx-auto px-4">
        <div class="flex justify-between items-center mb-10">
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white">最新电影</h2>
          <router-link to="/movies" class="text-blue-600 dark:text-blue-400 hover:underline">查看全部</router-link>
        </div>
        
        <div v-if="moviesStore.loading" class="py-20 text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
          <p class="mt-4 text-gray-600 dark:text-gray-400">加载中...</p>
        </div>
        <div v-else-if="moviesStore.latestMovies.length === 0" class="py-20 text-center">
          <p class="text-gray-600 dark:text-gray-400">暂无电影数据</p>
        </div>
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <div v-for="movie in moviesStore.latestMovies.slice(0, 8)" :key="movie.id" class="bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow-md transition-transform hover:scale-105">
            <div class="h-64 overflow-hidden bg-gray-200 dark:bg-gray-700">
              <img :src="movie.poster_url" :alt="movie.title" class="w-full h-full object-cover">
            </div>
            <div class="p-4">
              <router-link :to="`/movies/${movie.id}`" class="text-lg font-bold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 line-clamp-1">
                {{ movie.title }}
              </router-link>
              <div class="flex items-center text-sm text-gray-600 dark:text-gray-300 mt-2 space-x-2">
                <span>{{ movie.release_date }}</span>
                <span>|</span>
                <span class="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-yellow-500 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  {{ movie.rating }}
                </span>
              </div>
              <div class="mt-2 text-sm">
                <span class="text-gray-700 dark:text-gray-300">票房:</span>
                <span class="font-medium text-blue-600 dark:text-blue-400 ml-1">{{ formatBoxOffice(movie.box_office) }}元</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 号召性区域 -->
    <section class="py-16 bg-blue-600 text-white">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold mb-6">开始探索电影票房数据</h2>
        <p class="text-xl mb-8 max-w-2xl mx-auto">注册账号，获取更多个性化功能和数据分析工具</p>
        <div class="flex justify-center gap-4">
          <router-link v-if="!authStore.isLoggedIn" to="/register" class="bg-white text-blue-600 hover:bg-blue-50 px-6 py-3 rounded-lg font-medium transition-colors">
            立即注册
          </router-link>
          <router-link to="/charts" class="bg-transparent border-2 border-white hover:bg-white/10 px-6 py-3 rounded-lg font-medium transition-colors">
            查看数据分析
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useMoviesStore } from '../stores/movies'
import { useAuthStore } from '../stores/auth'

const moviesStore = useMoviesStore()
const authStore = useAuthStore()

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

onMounted(async () => {
  if (moviesStore.topMovies.length === 0) {
    await moviesStore.fetchTopMovies(5)
  }
  
  if (moviesStore.latestMovies.length === 0) {
    await moviesStore.fetchLatestMovies(8)
  }
})
</script> 