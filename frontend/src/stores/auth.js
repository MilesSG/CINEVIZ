import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin'
  },
  
  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/auth/login', {
          username,
          password
        })
        
        const { access_token, user } = response.data
        
        this.token = access_token
        this.user = user
        
        // 保存到本地存储
        localStorage.setItem('token', access_token)
        
        // 设置 axios 默认头部
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        
        return true
      } catch (error) {
        this.error = error.response?.data?.message || '登录失败，请检查用户名和密码'
        return false
      } finally {
        this.loading = false
      }
    },
    
    async register(username, email, password) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post('/api/auth/register', {
          username,
          email,
          password
        })
        
        return true
      } catch (error) {
        this.error = error.response?.data?.message || '注册失败，请稍后重试'
        return false
      } finally {
        this.loading = false
      }
    },
    
    async fetchUserProfile() {
      if (!this.token) return
      
      this.loading = true
      
      try {
        const response = await axios.get('/api/auth/profile', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        
        this.user = response.data.user
        return this.user
      } catch (error) {
        // 如果是 401 未授权错误，则登出
        if (error.response?.status === 401) {
          this.logout()
        }
        
        this.error = error.response?.data?.message || '获取用户信息失败'
        return null
      } finally {
        this.loading = false
      }
    },
    
    async updateProfile(userData) {
      if (!this.token) return false
      
      this.loading = true
      
      try {
        const response = await axios.put('/api/auth/update-profile', userData, {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        
        this.user = response.data.user
        return true
      } catch (error) {
        this.error = error.response?.data?.message || '更新个人资料失败'
        return false
      } finally {
        this.loading = false
      }
    },
    
    async toggleFavorite(movieId) {
      if (!this.token || !this.user) return false
      
      this.loading = true
      
      try {
        const isFavorited = this.user.favorites.includes(movieId)
        
        let response
        if (isFavorited) {
          // 如果已收藏，则取消收藏
          response = await axios.delete(`/api/auth/favorites/${movieId}`, {
            headers: {
              Authorization: `Bearer ${this.token}`
            }
          })
        } else {
          // 如果未收藏，则添加收藏
          response = await axios.post(`/api/auth/favorites/${movieId}`, {}, {
            headers: {
              Authorization: `Bearer ${this.token}`
            }
          })
        }
        
        // 更新用户收藏列表
        this.user.favorites = response.data.favorites
        
        return true
      } catch (error) {
        this.error = error.response?.data?.message || '操作收藏失败'
        return false
      } finally {
        this.loading = false
      }
    },
    
    logout() {
      // 清除用户信息和令牌
      this.user = null
      this.token = null
      
      // 清除本地存储
      localStorage.removeItem('token')
      
      // 清除 axios 默认头部
      delete axios.defaults.headers.common['Authorization']
    },
    
    // 初始化 auth 状态
    init() {
      if (this.token) {
        // 设置 axios 默认头部
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        
        // 获取用户信息
        this.fetchUserProfile()
      }
    }
  }
}) 