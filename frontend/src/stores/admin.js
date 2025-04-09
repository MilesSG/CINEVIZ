import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'

export const useAdminStore = defineStore('admin', () => {
  // 状态
  const users = ref([])
  const dashboardStats = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const success = ref(null)
  
  // 获取所有用户
  async function fetchUsers() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/admin/users')
      users.value = response.data.users
      return users.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取用户列表失败'
      return []
    } finally {
      loading.value = false
    }
  }
  
  // 获取仪表盘统计数据
  async function fetchDashboardStats() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get('/api/admin/dashboard')
      dashboardStats.value = response.data
      return dashboardStats.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取仪表盘统计数据失败'
      return null
    } finally {
      loading.value = false
    }
  }
  
  // 更新用户角色
  async function updateUserRole(userId, role) {
    loading.value = true
    error.value = null
    success.value = null
    
    try {
      const response = await axios.put(`/api/admin/users/${userId}/role`, { role })
      
      // 更新本地用户列表
      const userIndex = users.value.findIndex(user => user.id === userId)
      if (userIndex !== -1) {
        users.value[userIndex] = response.data.user
      }
      
      success.value = '用户角色更新成功'
      return true
    } catch (err) {
      error.value = err.response?.data?.message || '更新用户角色失败'
      return false
    } finally {
      loading.value = false
    }
  }
  
  // 删除用户
  async function deleteUser(userId) {
    loading.value = true
    error.value = null
    success.value = null
    
    try {
      await axios.delete(`/api/admin/users/${userId}`)
      
      // 从本地用户列表中移除
      users.value = users.value.filter(user => user.id !== userId)
      
      success.value = '用户删除成功'
      return true
    } catch (err) {
      error.value = err.response?.data?.message || '删除用户失败'
      return false
    } finally {
      loading.value = false
    }
  }
  
  // 创建电影
  async function createMovie(movieData) {
    loading.value = true
    error.value = null
    success.value = null
    
    try {
      const response = await axios.post('/api/admin/movies', movieData)
      
      success.value = '电影创建成功'
      return response.data.movie
    } catch (err) {
      error.value = err.response?.data?.message || '创建电影失败'
      return null
    } finally {
      loading.value = false
    }
  }
  
  // 更新电影
  async function updateMovie(movieId, movieData) {
    loading.value = true
    error.value = null
    success.value = null
    
    try {
      const response = await axios.put(`/api/admin/movies/${movieId}`, movieData)
      
      success.value = '电影更新成功'
      return response.data.movie
    } catch (err) {
      error.value = err.response?.data?.message || '更新电影失败'
      return null
    } finally {
      loading.value = false
    }
  }
  
  // 删除电影
  async function deleteMovie(movieId) {
    loading.value = true
    error.value = null
    success.value = null
    
    try {
      await axios.delete(`/api/admin/movies/${movieId}`)
      
      success.value = '电影删除成功'
      return true
    } catch (err) {
      error.value = err.response?.data?.message || '删除电影失败'
      return false
    } finally {
      loading.value = false
    }
  }
  
  // 爬取电影数据
  async function crawlMovieData(pages = 1) {
    loading.value = true
    error.value = null
    success.value = null
    
    try {
      const response = await axios.post('/api/crawl/maoyan', { pages })
      
      success.value = response.data.message
      return true
    } catch (err) {
      error.value = err.response?.data?.message || '爬取电影数据失败'
      return false
    } finally {
      loading.value = false
    }
  }
  
  // 清除消息
  function clearMessages() {
    error.value = null
    success.value = null
  }
  
  return {
    // 状态
    users,
    dashboardStats,
    loading,
    error,
    success,
    
    // 方法
    fetchUsers,
    fetchDashboardStats,
    updateUserRole,
    deleteUser,
    createMovie,
    updateMovie,
    deleteMovie,
    crawlMovieData,
    clearMessages
  }
}) 