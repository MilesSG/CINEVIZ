<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">管理后台</h1>
      </div>
      <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
        <!-- 选项卡导航 -->
        <div class="mt-4 border-b border-gray-200 dark:border-gray-700">
          <nav class="-mb-px flex space-x-8">
            <button 
              @click="activeTab = 'dashboard'" 
              :class="[
                activeTab === 'dashboard' 
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-200',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
              ]"
            >
              仪表盘
            </button>
            <button 
              @click="activeTab = 'users'" 
              :class="[
                activeTab === 'users' 
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-200',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
              ]"
            >
              用户管理
            </button>
            <button 
              @click="activeTab = 'movies'" 
              :class="[
                activeTab === 'movies' 
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-200',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
              ]"
            >
              电影管理
            </button>
            <button 
              @click="activeTab = 'crawler'" 
              :class="[
                activeTab === 'crawler' 
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-200',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
              ]"
            >
              爬虫管理
            </button>
          </nav>
        </div>

        <!-- 提示消息 -->
        <div v-if="adminStore.error" class="mt-4 bg-red-50 dark:bg-red-900/30 p-4 rounded-md">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-red-800 dark:text-red-200">
                {{ adminStore.error }}
              </p>
            </div>
            <div class="ml-auto pl-3">
              <div class="-mx-1.5 -my-1.5">
                <button @click="adminStore.clearMessages()" class="inline-flex rounded-md p-1.5 text-red-500 hover:bg-red-100 dark:hover:bg-red-800">
                  <span class="sr-only">关闭</span>
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="adminStore.success" class="mt-4 bg-green-50 dark:bg-green-900/30 p-4 rounded-md">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-green-800 dark:text-green-200">
                {{ adminStore.success }}
              </p>
            </div>
            <div class="ml-auto pl-3">
              <div class="-mx-1.5 -my-1.5">
                <button @click="adminStore.clearMessages()" class="inline-flex rounded-md p-1.5 text-green-500 hover:bg-green-100 dark:hover:bg-green-800">
                  <span class="sr-only">关闭</span>
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 内容区域 -->
        <div class="py-6">
          <!-- 爬虫控制面板 -->
          <div v-if="activeTab === 'crawler'" class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">电影数据爬虫</h2>
            
            <div class="mb-6">
              <label for="pages" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">爬取页数 (最大10页)</label>
              <div class="flex items-center">
                <input 
                  v-model="crawlerPages" 
                  type="number" 
                  min="1" 
                  max="10" 
                  id="pages" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:w-40 sm:text-sm border-gray-300 rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                >
                <button 
                  @click="startCrawler" 
                  :disabled="adminStore.loading" 
                  class="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span v-if="adminStore.loading">正在爬取...</span>
                  <span v-else>开始爬取</span>
                </button>
              </div>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">每页大约爬取10部电影数据</p>
            </div>

            <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-md">
              <h3 class="text-md font-medium text-gray-900 dark:text-white mb-3">爬虫说明</h3>
              <ul class="list-disc pl-5 text-sm text-gray-600 dark:text-gray-300 space-y-1">
                <li>爬虫将从猫眼电影网站获取电影数据</li>
                <li>数据包括电影名称、导演、演员、上映日期、票房等信息</li>
                <li>为避免对网站造成压力，爬取过程会有间隔</li>
                <li>爬取完成后数据会自动保存到系统中</li>
                <li>请勿频繁爬取，以免IP被封</li>
              </ul>
            </div>
          </div>

          <!-- 仪表盘 -->
          <div v-if="activeTab === 'dashboard'" class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">数据总览</h2>
            
            <div v-if="adminStore.loading" class="py-10 text-center">
              <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
              <p class="mt-4 text-gray-600 dark:text-gray-400">加载中...</p>
            </div>
            
            <div v-else-if="!adminStore.dashboardStats" class="py-10 text-center">
              <p class="text-gray-600 dark:text-gray-400">暂无数据，请先获取数据</p>
              <button 
                @click="adminStore.fetchDashboardStats()" 
                class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                刷新数据
              </button>
            </div>
            
            <div v-else>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div class="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">电影总数</h3>
                  <p class="mt-2 text-3xl font-bold text-blue-600 dark:text-blue-400">{{ adminStore.dashboardStats.stats.total_movies }}</p>
                </div>
                <div class="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">用户总数</h3>
                  <p class="mt-2 text-3xl font-bold text-green-600 dark:text-green-400">{{ adminStore.dashboardStats.stats.total_users }}</p>
                </div>
                <div class="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-lg">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">总票房（元）</h3>
                  <p class="mt-2 text-3xl font-bold text-purple-600 dark:text-purple-400">{{ formatBoxOffice(adminStore.dashboardStats.stats.total_box_office) }}</p>
                </div>
              </div>
              
              <div class="mt-8">
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">热门电影</h3>
                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                    <thead class="bg-gray-50 dark:bg-gray-700">
                      <tr>
                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">电影名称</th>
                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">上映日期</th>
                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">票房（元）</th>
                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">评分</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                      <tr v-for="movie in adminStore.dashboardStats.top_movies" :key="movie.id">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ movie.title }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ movie.release_date }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ formatBoxOffice(movie.box_office) }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ movie.rating }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              
              <div class="mt-8">
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">电影类型分布</h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div v-for="(count, genre) in adminStore.dashboardStats.stats.genre_distribution" :key="genre" class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                    <span class="block text-gray-500 dark:text-gray-300 text-sm">{{ genre }}</span>
                    <span class="block text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ count }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 用户管理界面的内容（简化版） -->
          <div v-if="activeTab === 'users'" class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">用户管理</h2>
            <button 
              @click="fetchUsers" 
              class="mb-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              刷新用户列表
            </button>
            
            <div v-if="adminStore.loading" class="py-10 text-center">
              <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
              <p class="mt-4 text-gray-600 dark:text-gray-400">加载中...</p>
            </div>
            
            <div v-else-if="adminStore.users.length === 0" class="py-10 text-center">
              <p class="text-gray-600 dark:text-gray-400">暂无用户数据</p>
            </div>
            
            <div v-else class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead class="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">用户名</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">邮箱</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">角色</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">注册时间</th>
                    <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">操作</th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  <tr v-for="user in adminStore.users" :key="user.id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ user.username }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ user.email }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                      <span 
                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                        :class="user.role === 'admin' ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300' : 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'"
                      >
                        {{ user.role === 'admin' ? '管理员' : '普通用户' }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{{ formatDate(user.created_at) }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button 
                        v-if="user.role === 'user'"
                        @click="updateUserRole(user.id, 'admin')" 
                        class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300 mr-3"
                      >
                        设为管理员
                      </button>
                      <button 
                        v-else
                        @click="updateUserRole(user.id, 'user')" 
                        class="text-yellow-600 hover:text-yellow-900 dark:text-yellow-400 dark:hover:text-yellow-300 mr-3"
                      >
                        取消管理员
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- 电影管理界面简化版 -->
          <div v-if="activeTab === 'movies'" class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">电影管理</h2>
            <p class="text-gray-600 dark:text-gray-400 mb-4">您可以在这里管理电影数据。要增加电影数据，请使用爬虫功能</p>
            <p class="text-blue-600 dark:text-blue-400">此功能正在开发中...请先使用爬虫模块获取电影数据</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '../stores/admin'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const adminStore = useAdminStore()
const authStore = useAuthStore()

const activeTab = ref('crawler')
const crawlerPages = ref(1)

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

// 启动爬虫
const startCrawler = async () => {
  await adminStore.crawlMovieData(crawlerPages.value)
}

// 获取用户列表
const fetchUsers = async () => {
  await adminStore.fetchUsers()
}

// 更新用户角色
const updateUserRole = async (userId, role) => {
  await adminStore.updateUserRole(userId, role)
}

onMounted(async () => {
  // 检查是否有管理员权限
  if (!authStore.isAdmin) {
    router.push('/')
    return
  }
  
  // 获取仪表盘数据
  await adminStore.fetchDashboardStats()
  
  // 获取用户列表
  await adminStore.fetchUsers()
})
</script> 