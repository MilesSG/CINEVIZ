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
      
      if (response.status === 200) {
        boxOfficeTrendData.value = response.data
        selectedMovieId.value = movieId
      } else {
        error.value = '获取票房走势数据失败'
        console.error('API 返回非200状态码:', response.status)
      }
      
      return boxOfficeTrendData.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取票房走势数据失败'
      console.error('获取票房走势数据出错:', err)
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
      
      if (response.status === 200) {
        genreComparisonData.value = response.data
      } else {
        error.value = '获取类型比较数据失败'
        console.error('API 返回非200状态码:', response.status)
      }
      
      return genreComparisonData.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取类型比较数据失败'
      console.error('获取类型比较数据出错:', err)
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
      
      if (response.status === 200) {
        releaseHeatmapData.value = response.data
      } else {
        error.value = '获取发行时间热力图数据失败'
        console.error('API 返回非200状态码:', response.status)
      }
      
      return releaseHeatmapData.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取发行时间热力图数据失败'
      console.error('获取发行时间热力图数据出错:', err)
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
      
      if (response.status === 200) {
        boxOfficeDistributionData.value = response.data
      } else {
        error.value = '获取票房分布数据失败'
        console.error('API 返回非200状态码:', response.status)
      }
      
      return boxOfficeDistributionData.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取票房分布数据失败'
      console.error('获取票房分布数据出错:', err)
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
    loading.value = true;
    error.value = null;
    
    try {
      // 使用Promise.allSettled确保即使某些请求失败，其他请求仍然能够继续
      const results = await Promise.allSettled([
        fetchBoxOfficeTrend(),
        fetchGenreComparison(),
        fetchReleaseHeatmap(),
        fetchBoxOfficeDistribution()
      ]);
      
      // 检查各个请求的结果
      const failedRequests = results.filter(result => result.status === 'rejected');
      if (failedRequests.length > 0) {
        console.warn(`${failedRequests.length} 个数据请求失败`);
        failedRequests.forEach(failure => console.error(failure.reason));
      }
      
      return {
        boxOfficeTrend: results[0].status === 'fulfilled' ? results[0].value : null,
        genreComparison: results[1].status === 'fulfilled' ? results[1].value : null,
        releaseHeatmap: results[2].status === 'fulfilled' ? results[2].value : null,
        boxOfficeDistribution: results[3].status === 'fulfilled' ? results[3].value : null
      };
    } catch (err) {
      error.value = '初始化数据失败';
      console.error('初始化数据出错:', err);
      return null;
    } finally {
      loading.value = false;
    }
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