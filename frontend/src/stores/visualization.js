import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'

export const useVisualizationStore = defineStore('visualization', () => {
  // 状态
  const boxOfficeTrendData = ref(null)
  const genreComparisonData = ref(null)
  const releaseHeatmapData = ref(null)
  const boxOfficeDistributionData = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const selectedMovieId = ref(null)
  
  // 加载票房走势数据
  async function fetchBoxOfficeTrend(movieId = null) {
    loading.value = true
    error.value = null
    
    try {
      const url = movieId 
        ? `/api/visualization/box-office-trend?movie_id=${movieId}`
        : '/api/visualization/box-office-trend'
      
      const response = await axios.get(url)
      boxOfficeTrendData.value = response.data
      selectedMovieId.value = movieId
      
      return boxOfficeTrendData.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取票房走势数据失败'
      return null
    } finally {
      loading.value = false
    }
  }
  
  // 加载类型比较数据
  async function fetchGenreComparison() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/visualization/genre-comparison')
      genreComparisonData.value = response.data
      
      return genreComparisonData.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取类型比较数据失败'
      return null
    } finally {
      loading.value = false
    }
  }
  
  // 加载发行时间热力图数据
  async function fetchReleaseHeatmap() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/visualization/release-heatmap')
      releaseHeatmapData.value = response.data
      
      return releaseHeatmapData.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取发行时间热力图数据失败'
      return null
    } finally {
      loading.value = false
    }
  }
  
  // 加载票房分布数据
  async function fetchBoxOfficeDistribution() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/visualization/box-office-distribution')
      boxOfficeDistributionData.value = response.data
      
      return boxOfficeDistributionData.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取票房分布数据失败'
      return null
    } finally {
      loading.value = false
    }
  }
  
  // 清除选中的电影
  function clearSelectedMovie() {
    selectedMovieId.value = null
  }
  
  // 初始化所有数据
  async function initAllData() {
    await Promise.all([
      fetchBoxOfficeTrend(),
      fetchGenreComparison(),
      fetchReleaseHeatmap(),
      fetchBoxOfficeDistribution()
    ])
  }
  
  return {
    // 状态
    boxOfficeTrendData,
    genreComparisonData,
    releaseHeatmapData,
    boxOfficeDistributionData,
    loading,
    error,
    selectedMovieId,
    
    // 方法
    fetchBoxOfficeTrend,
    fetchGenreComparison,
    fetchReleaseHeatmap,
    fetchBoxOfficeDistribution,
    clearSelectedMovie,
    initAllData
  }
}) 