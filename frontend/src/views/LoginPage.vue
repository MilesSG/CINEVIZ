<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">登录到CineViz</h2>
        <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
          探索电影票房数据的可视化世界
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="username" class="sr-only">用户名</label>
            <input v-model="username" id="username" name="username" type="text" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm dark:bg-gray-800 dark:border-gray-700 dark:text-white" placeholder="用户名" />
          </div>
          <div>
            <label for="password" class="sr-only">密码</label>
            <input v-model="password" id="password" name="password" type="password" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm dark:bg-gray-800 dark:border-gray-700 dark:text-white" placeholder="密码" />
          </div>
        </div>

        <div v-if="authStore.error" class="text-red-500 text-center text-sm">
          {{ authStore.error }}
        </div>

        <div>
          <button type="submit" :disabled="authStore.loading" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed">
            <span v-if="authStore.loading">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              登录中...
            </span>
            <span v-else>登录</span>
          </button>
        </div>
        
        <div class="flex items-center justify-between">
          <div class="text-sm">
            <router-link to="/register" class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400">
              没有账号？立即注册
            </router-link>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')

const handleLogin = async () => {
  if (username.value && password.value) {
    const success = await authStore.login(username.value, password.value)
    
    if (success) {
      // 登录成功后重定向
      const redirectPath = route.query.redirect || '/'
      router.push(redirectPath)
    }
  }
}

onMounted(() => {
  // 如果已登录，重定向到首页
  if (authStore.isLoggedIn) {
    router.push('/')
  }
})
</script> 