<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-8">票房数据分析</h1>
    
    <!-- 加载状态 -->
    <div v-if="visualizationStore.loading" class="py-20 text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">加载中...</p>
    </div>
    
    <!-- 无数据提示 -->
    <div v-else-if="!hasData" class="py-20 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
      <p class="text-xl text-gray-600 dark:text-gray-400">暂无分析数据</p>
      <p class="mt-2 text-gray-500 dark:text-gray-500">请先获取电影数据</p>
    </div>
    
    <!-- 数据可视化图表 -->
    <div v-else>
      <!-- 票房走势 -->
      <section class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">电影票房走势</h2>
          
          <div class="mt-4 md:mt-0">
            <select
              v-model="selectedMovieId"
              class="px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              @change="updateBoxOfficeTrend"
            >
              <option value="">所有电影总票房</option>
              <option v-for="movie in movies" :key="movie.id" :value="movie.id">{{ movie.title }}</option>
            </select>
          </div>
        </div>
        
        <div class="h-64 sm:h-80">
          <!-- 票房走势图将在后续实现 -->
          <div class="h-full flex items-center justify-center">
            <p class="text-center text-gray-500 dark:text-gray-400">票房走势图组件将在此处显示</p>
          </div>
        </div>
      </section>
      
      <!-- 类型对比 -->
      <section class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">电影类型票房对比</h2>
        
        <div class="h-64 sm:h-80">
          <!-- 电影类型对比图将在后续实现 -->
          <div class="h-full flex items-center justify-center">
            <p class="text-center text-gray-500 dark:text-gray-400">电影类型对比图组件将在此处显示</p>
          </div>
        </div>
        
        <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <div v-for="(value, index) in genreBoxOfficeData" :key="index" class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
            <span class="text-sm text-gray-600 dark:text-gray-400">{{ value.genre }}</span>
            <div class="flex items-baseline space-x-2 mt-1">
              <span class="text-lg font-bold text-gray-900 dark:text-white">{{ formatBoxOffice(value.total) }}</span>
              <span class="text-xs text-gray-500 dark:text-gray-400">平均: {{ formatBoxOffice(value.average) }}/部</span>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 发行时间热力图 -->
      <section class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">电影发行时间分布</h2>
        
        <div class="h-64 sm:h-96">
          <!-- 发行时间热力图将在后续实现 -->
          <div class="h-full flex items-center justify-center">
            <p class="text-center text-gray-500 dark:text-gray-400">电影发行时间热力图组件将在此处显示</p>
          </div>
        </div>
      </section>
      
      <!-- 票房分布 -->
      <section class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">票房分布区间</h2>
        
        <div class="h-64 sm:h-80">
          <!-- 票房分布图将在后续实现 -->
          <div class="h-full flex items-center justify-center">
            <p class="text-center text-gray-500 dark:text-gray-400">票房分布图组件将在此处显示</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useVisualizationStore } from '../stores/visualization'
import { useMoviesStore } from '../stores/movies'

const visualizationStore = useVisualizationStore()
const moviesStore = useMoviesStore()
const selectedMovieId = ref('')
const movies = ref([])

// 判断是否有数据
const hasData = computed(() => {
  return !!(
    visualizationStore.boxOfficeTrendData && 
    visualizationStore.genreComparisonData &&
    visualizationStore.releaseHeatmapData &&
    visualizationStore.boxOfficeDistributionData
  )
})

// 获取电影类型票房数据
const genreBoxOfficeData = computed(() => {
  if (!visualizationStore.genreComparisonData) return []
  
  const { genres, total_box_offices, avg_box_offices } = visualizationStore.genreComparisonData
  
  return genres.map((genre, index) => ({
    genre,
    total: total_box_offices[index],
    average: avg_box_offices[index]
  }))
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

// 更新票房走势数据
const updateBoxOfficeTrend = async () => {
  await visualizationStore.fetchBoxOfficeTrend(selectedMovieId.value || null)
}

onMounted(async () => {
  // 初始化所有数据
  await visualizationStore.initAllData()
  
  // 获取电影列表（用于选择器）
  if (moviesStore.movies.length === 0) {
    await moviesStore.fetchMovies()
  }
  movies.value = moviesStore.movies
})
</script> 