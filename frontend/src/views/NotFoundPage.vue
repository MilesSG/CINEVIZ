<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full text-center">
      <h1 class="text-9xl font-extrabold text-blue-600 dark:text-blue-500">404</h1>
      <h2 class="mt-4 text-3xl font-bold text-gray-900 dark:text-white">页面未找到</h2>
      <p class="mt-2 text-lg text-gray-600 dark:text-gray-400">
        抱歉，您访问的页面不存在或已被移除。
      </p>
      <div class="mt-6">
        <router-link to="/" class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">
          返回首页
        </router-link>
      </div>
    </div>
  </div>
</template> 