import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// 路由懒加载
const HomePage = () => import('../views/HomePage.vue')
const LoginPage = () => import('../views/LoginPage.vue')
const RegisterPage = () => import('../views/RegisterPage.vue')
const MoviesPage = () => import('../views/MoviesPage.vue')
const MovieDetailPage = () => import('../views/MovieDetailPage.vue')
const ChartsPage = () => import('../views/ChartsPage.vue')
const ProfilePage = () => import('../views/ProfilePage.vue')
const AdminPage = () => import('../views/AdminPage.vue')
const NotFoundPage = () => import('../views/NotFoundPage.vue')

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
    meta: { title: '首页 - CineViz' }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
    meta: { title: '登录 - CineViz', guest: true }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage,
    meta: { title: '注册 - CineViz', guest: true }
  },
  {
    path: '/movies',
    name: 'movies',
    component: MoviesPage,
    meta: { title: '影片列表 - CineViz' }
  },
  {
    path: '/movies/:id',
    name: 'movie-detail',
    component: MovieDetailPage,
    props: true,
    meta: { title: '影片详情 - CineViz' }
  },
  {
    path: '/charts',
    name: 'charts',
    component: ChartsPage,
    meta: { title: '数据分析 - CineViz' }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage,
    meta: { title: '个人中心 - CineViz', requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminPage,
    meta: { title: '管理后台 - CineViz', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundPage,
    meta: { title: '页面未找到 - CineViz' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 导航守卫
router.beforeEach((to, from, next) => {
  // 更新页面标题
  document.title = to.meta.title || 'CineViz - 影视票房数据可视化系统'
  
  const authStore = useAuthStore()
  
  // 检查身份验证要求
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    // 需要登录但未登录，重定向到登录页
    next({ name: 'login', query: { redirect: to.fullPath } })
  } 
  // 检查管理员权限要求
  else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    // 需要管理员权限但不是管理员，重定向到首页
    next({ name: 'home' })
  }
  // 已登录用户访问游客页面
  else if (to.meta.guest && authStore.isLoggedIn) {
    // 已登录用户不应访问登录/注册页，重定向到首页
    next({ name: 'home' })
  }
  else {
    // 正常导航
    next()
  }
})

export default router 