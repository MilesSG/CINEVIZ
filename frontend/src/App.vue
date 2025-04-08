<template>
  <div class="min-h-screen font-sans antialiased text-gray-900 dark:text-gray-100">
    <header v-if="!isLoginPage" class="bg-gradient-to-r from-blue-600 to-purple-600 shadow-md">
      <nav class="container mx-auto px-4 py-4 flex items-center justify-between">
        <router-link to="/" class="text-white font-bold text-2xl flex items-center">
          <span class="mr-2">🎬</span>
          <span>CineViz</span>
        </router-link>
        
        <div class="flex items-center space-x-6">
          <!-- 导航链接 -->
          <router-link to="/" class="text-white hover:text-blue-200 transition-colors">首页</router-link>
          <router-link to="/movies" class="text-white hover:text-blue-200 transition-colors">电影</router-link>
          <router-link to="/charts" class="text-white hover:text-blue-200 transition-colors">数据分析</router-link>
          
          <!-- 用户菜单 -->
          <div v-if="authStore.isLoggedIn" class="relative">
            <button @click="toggleUserMenu" class="flex items-center text-white hover:text-blue-200 transition-colors focus:outline-none">
              <span class="mr-1">{{ authStore.user?.username }}</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
            
            <!-- 下拉菜单 -->
            <div v-if="showUserMenu" class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-md shadow-lg py-1 z-10">
              <router-link to="/profile" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">个人中心</router-link>
              <router-link v-if="authStore.isAdmin" to="/admin" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700">管理后台</router-link>
              <button @click="logout" class="block w-full text-left px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700">退出登录</button>
            </div>
          </div>
          
          <!-- 登录/注册按钮 -->
          <div v-else class="flex items-center space-x-2">
            <router-link to="/login" class="text-white hover:text-blue-200 transition-colors">登录</router-link>
            <span class="text-white">|</span>
            <router-link to="/register" class="text-white hover:text-blue-200 transition-colors">注册</router-link>
          </div>
          
          <!-- 深色模式切换 -->
          <button @click="toggleDarkMode" class="text-white hover:text-blue-200 transition-colors focus:outline-none">
            <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
        </div>
      </nav>
    </header>
    
    <main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <footer v-if="!isLoginPage" class="bg-gray-800 text-white py-8 mt-auto">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="mb-4 md:mb-0">
            <div class="text-2xl font-bold mb-2 flex items-center">
              <span class="mr-2">🎬</span>
              <span>CineViz</span>
            </div>
            <p class="text-gray-400">影视票房数据可视化系统</p>
          </div>
          
          <div class="flex flex-col text-center md:text-right">
            <p class="text-gray-400">© {{ new Date().getFullYear() }} CineViz. 保留所有权利</p>
            <p class="text-gray-500 mt-1 text-sm">数据来源于猫眼电影</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const showUserMenu = ref(false)
const isDarkMode = ref(false)

// 检查是否是登录/注册页面
const isLoginPage = computed(() => {
  return route.path === '/login' || route.path === '/register'
})

// 切换用户菜单
function toggleUserMenu() {
  showUserMenu.value = !showUserMenu.value
}

// 切换深色模式
function toggleDarkMode() {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

// 退出登录
function logout() {
  authStore.logout()
  router.push('/login')
  showUserMenu.value = false
}

// 初始化主题
onMounted(() => {
  const theme = localStorage.getItem('theme')
  isDarkMode.value = theme === 'dark'
  
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  }
  
  // 点击其他地方关闭用户菜单
  document.addEventListener('click', (e) => {
    if (showUserMenu.value && !e.target.closest('.relative')) {
      showUserMenu.value = false
    }
  })
})

// 路由变化时关闭用户菜单
watch(route, () => {
  showUserMenu.value = false
})
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 