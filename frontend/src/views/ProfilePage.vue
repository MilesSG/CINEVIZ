<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-8">个人中心</h1>
    
    <!-- 加载状态 -->
    <div v-if="authStore.loading" class="py-20 text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">加载中...</p>
    </div>
    
    <!-- 内容区域 -->
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <!-- 左侧用户信息 -->
      <div class="md:col-span-1">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
          <div class="text-center mb-6">
            <div class="w-24 h-24 mx-auto bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center text-blue-600 dark:text-blue-400 text-2xl font-bold mb-4">
              {{ userInitials }}
            </div>
            <h2 class="text-xl font-bold text-gray-900 dark:text-white">{{ authStore.user?.username }}</h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ authStore.user?.email }}</p>
            <div class="mt-2">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium" :class="roleClass">
                {{ authStore.user?.role === 'admin' ? '管理员' : '普通用户' }}
              </span>
            </div>
          </div>
          
          <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
            <div class="text-sm text-gray-600 dark:text-gray-400">
              <div class="flex justify-between py-2">
                <span>账号创建于</span>
                <span class="text-gray-900 dark:text-white">{{ formatDate(authStore.user?.created_at) }}</span>
              </div>
              <div class="flex justify-between py-2">
                <span>收藏电影数</span>
                <span class="text-gray-900 dark:text-white">{{ authStore.user?.favorites.length || 0 }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 修改资料卡片 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mt-6">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">修改个人资料</h3>
          
          <form @submit.prevent="updateProfile">
            <div class="mb-4">
              <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">电子邮箱</label>
              <input 
                v-model="profileForm.email" 
                type="email" 
                id="email" 
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              >
            </div>
            
            <div class="mb-6">
              <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">新密码 (留空则不修改)</label>
              <input 
                v-model="profileForm.password" 
                type="password" 
                id="password" 
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              >
            </div>
            
            <div>
              <button 
                type="submit" 
                :disabled="profileUpdateLoading"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ profileUpdateLoading ? '保存中...' : '保存修改' }}
              </button>
            </div>
            
            <div v-if="updateError" class="mt-3 text-sm text-red-600 dark:text-red-400">
              {{ updateError }}
            </div>
            
            <div v-if="updateSuccess" class="mt-3 text-sm text-green-600 dark:text-green-400">
              个人资料更新成功
            </div>
          </form>
        </div>
      </div>
      
      <!-- 右侧收藏列表 -->
      <div class="md:col-span-2">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">我的收藏</h3>
          </div>
          
          <!-- 加载状态 -->
          <div v-if="favoriteMoviesLoading" class="py-20 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
            <p class="mt-4 text-gray-600 dark:text-gray-400">加载中...</p>
          </div>
          
          <!-- 无收藏 -->
          <div v-else-if="favoriteMovies.length === 0" class="py-20 text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            <p class="text-xl text-gray-600 dark:text-gray-400">暂无收藏电影</p>
            <div class="mt-6">
              <router-link to="/movies" class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">
                浏览电影
              </router-link>
            </div>
          </div>
          
          <!-- 收藏列表 -->
          <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
            <div v-for="movie in favoriteMovies" :key="movie.id" class="p-4 sm:px-6 hover:bg-gray-50 dark:hover:bg-gray-700">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-16 w-12">
                  <img :src="movie.poster_url" :alt="movie.title" class="h-full w-full object-cover rounded">
                </div>
                <div class="ml-4 flex-1">
                  <div class="flex items-center justify-between">
                    <div>
                      <router-link :to="`/movies/${movie.id}`" class="text-lg font-medium text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400">
                        {{ movie.title }}
                      </router-link>
                      <p class="text-sm text-gray-500 dark:text-gray-400">{{ movie.release_date }} | 评分: {{ movie.rating }}</p>
                    </div>
                    <button @click="removeFavorite(movie.id)" class="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                  <div class="mt-1">
                    <span class="text-sm text-gray-700 dark:text-gray-300">票房:</span>
                    <span class="ml-1 text-sm font-medium text-blue-600 dark:text-blue-400">{{ formatBoxOffice(movie.box_office) }}元</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useMoviesStore } from '../stores/movies'

const router = useRouter()
const authStore = useAuthStore()
const moviesStore = useMoviesStore()

const favoriteMovies = ref([])
const favoriteMoviesLoading = ref(false)
const profileUpdateLoading = ref(false)
const updateError = ref('')
const updateSuccess = ref(false)

const profileForm = ref({
  email: '',
  password: ''
})

// 获取用户首字母
const userInitials = computed(() => {
  if (!authStore.user?.username) return '?'
  return authStore.user.username.substring(0, 2).toUpperCase()
})

// 角色样式
const roleClass = computed(() => {
  return authStore.user?.role === 'admin'
    ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
    : 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
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

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 更新个人资料
const updateProfile = async () => {
  updateError.value = ''
  updateSuccess.value = false
  
  // 如果没有修改任何内容，则不发送请求
  if (!profileForm.value.email && !profileForm.value.password) {
    updateError.value = '请至少修改一项内容'
    return
  }
  
  profileUpdateLoading.value = true
  
  try {
    const userData = {}
    
    if (profileForm.value.email) {
      userData.email = profileForm.value.email
    }
    
    if (profileForm.value.password) {
      userData.password = profileForm.value.password
    }
    
    const success = await authStore.updateProfile(userData)
    
    if (success) {
      updateSuccess.value = true
      profileForm.value.password = '' // 清空密码字段
    }
  } catch (error) {
    updateError.value = '更新个人资料失败'
  } finally {
    profileUpdateLoading.value = false
  }
}

// 移除收藏
const removeFavorite = async (movieId) => {
  await authStore.toggleFavorite(movieId)
  // 从本地列表中移除
  favoriteMovies.value = favoriteMovies.value.filter(movie => movie.id !== movieId)
}

// 获取收藏的电影
const fetchFavoriteMovies = async () => {
  if (!authStore.user?.favorites.length) return
  
  favoriteMoviesLoading.value = true
  
  try {
    const favoriteIds = authStore.user.favorites
    // 获取所有电影
    await moviesStore.fetchMovies()
    
    // 筛选出收藏的电影
    favoriteMovies.value = moviesStore.movies.filter(movie => favoriteIds.includes(movie.id))
  } catch (error) {
    console.error('Failed to fetch favorite movies:', error)
  } finally {
    favoriteMoviesLoading.value = false
  }
}

onMounted(async () => {
  // 检查是否已登录
  if (!authStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  // 获取最新用户信息
  await authStore.fetchUserProfile()
  
  // 初始化表单值
  if (authStore.user) {
    profileForm.value.email = authStore.user.email
  }
  
  // 获取收藏的电影
  await fetchFavoriteMovies()
})
</script> 