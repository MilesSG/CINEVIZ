<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-8">票房数据分析</h1>
    
    <!-- 加载状态 -->
    <div v-if="visualizationStore.loading" class="py-20 text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
      <p class="mt-4 text-gray-600 dark:text-gray-400">加载中...</p>
    </div>
    
    <!-- 无数据提示 -->
    <div v-else-if="!hasData" class="py-20 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
      <p class="text-xl text-gray-600 dark:text-gray-400">暂无分析数据</p>
      <p class="mt-2 text-gray-500 dark:text-gray-500">请先获取电影数据</p>
      <button 
        @click="reloadAllData" 
        class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
      >
        重新加载数据
      </button>
    </div>
    
    <!-- 数据可视化图表 -->
    <div v-else>
      <!-- 操作按钮 -->
      <div class="mb-4 flex justify-end">
        <button 
          @click="reloadAllData" 
          class="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          刷新图表
        </button>
      </div>
      
      <!-- 票房走势 -->
      <section class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">电影票房走势</h2>
          
          <div class="mt-4 md:mt-0">
            <select
              v-model="selectedMovieId"
              class="px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              @change="updateBoxOfficeTrend"
            >
              <option value="">所有电影总票房</option>
              <option v-for="movie in movies" :key="movie.id" :value="movie.id">{{ movie.title }}</option>
            </select>
          </div>
        </div>
        
        <div class="h-64 sm:h-80">
          <div ref="boxOfficeTrendChart" class="w-full h-full"></div>
        </div>
      </section>
      
      <!-- 类型对比 -->
      <section class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">电影类型票房对比</h2>
        
        <div class="h-64 sm:h-80">
          <div ref="genreComparisonChart" class="w-full h-full"></div>
        </div>
        
        <div class="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <div v-for="(value, index) in genreBoxOfficeData" :key="index" class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
            <span class="text-sm text-gray-600 dark:text-gray-400">{{ value.genre }}</span>
            <div class="flex items-baseline space-x-2 mt-1">
              <span class="text-lg font-bold text-gray-900 dark:text-white">{{ formatBoxOffice(value.total) }}</span>
              <span class="text-xs text-gray-500 dark:text-gray-400">平均: {{ formatBoxOffice(value.average) }}/部</span>
            </div>
          </div>
        </div>
      </section>
      
      <!-- 发行时间热力图 -->
      <section class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">电影发行时间分布</h2>
        
        <div class="h-64 sm:h-96">
          <div ref="releaseHeatmapChart" class="w-full h-full"></div>
        </div>
      </section>
      
      <!-- 票房分布 -->
      <section class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-6">票房分布区间</h2>
        
        <div class="h-64 sm:h-80">
          <div ref="boxOfficeDistributionChart" class="w-full h-full"></div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useVisualizationStore } from '../stores/visualization'
import { useMoviesStore } from '../stores/movies'
import * as echarts from 'echarts'

const visualizationStore = useVisualizationStore()
const moviesStore = useMoviesStore()
const selectedMovieId = ref('')
const movies = ref([])

// 图表DOM引用
const boxOfficeTrendChart = ref(null)
const genreComparisonChart = ref(null)
const releaseHeatmapChart = ref(null)
const boxOfficeDistributionChart = ref(null)

// 图表实例
let boxOfficeTrendInstance = null
let genreComparisonInstance = null
let releaseHeatmapInstance = null
let boxOfficeDistributionInstance = null

// 判断是否有数据
const hasData = computed(() => {
  return !!(
    visualizationStore.boxOfficeTrendData && 
    visualizationStore.genreComparisonData &&
    visualizationStore.releaseHeatmapData &&
    visualizationStore.boxOfficeDistributionData
  )
})

// 获取电影类型票房数据
const genreBoxOfficeData = computed(() => {
  if (!visualizationStore.genreComparisonData) return []
  
  const { genres, total_box_offices, avg_box_offices } = visualizationStore.genreComparisonData
  
  if (!genres || !total_box_offices || !avg_box_offices) return []
  
  return genres.map((genre, index) => ({
    genre,
    total: total_box_offices[index],
    average: avg_box_offices[index]
  }))
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

// 重新加载所有数据
const reloadAllData = async () => {
  try {
    await visualizationStore.initAllData(selectedMovieId.value)
    
    // 获取电影列表（用于选择器）
    if (moviesStore.movies.length === 0) {
      await moviesStore.fetchMovies()
    }
    movies.value = moviesStore.movies
    
    await nextTick()
    initAllCharts()
  } catch (error) {
    console.error('重新加载数据出错:', error)
  }
}

// 显示后端连接错误提示
const showConnectionError = (instance, title = '连接错误') => {
  if (!instance) return
  
  const option = {
    title: {
      text: title,
      left: 'center',
      textStyle: {
        color: '#333'
      }
    },
    graphic: {
      type: 'text',
      left: 'center',
      top: 'middle',
      style: {
        text: '无法连接到后端服务，请检查服务是否启动',
        fontSize: 16,
        fill: '#999'
      }
    }
  }
  
  instance.setOption(option)
}

// 初始化票房走势图
const initBoxOfficeTrendChart = () => {
  if (!visualizationStore.boxOfficeTrendData || !boxOfficeTrendChart.value) return
  
  // 销毁之前的实例
  if (boxOfficeTrendInstance) {
    boxOfficeTrendInstance.dispose()
  }
  
  // 初始化新实例
  boxOfficeTrendInstance = echarts.init(boxOfficeTrendChart.value)
  
  let option = {}
  
  try {
    if (selectedMovieId.value) {
      // 单部电影日票房数据
      const { movie_title, dates, box_offices } = visualizationStore.boxOfficeTrendData
      
      // 验证数据是否完整
      if (!dates || !box_offices || dates.length === 0) {
        // 显示无数据的提示
        option = {
          title: {
            text: movie_title ? `${movie_title} 票房走势` : '电影票房走势',
            left: 'center',
            textStyle: {
              color: '#333'
            }
          },
          graphic: {
            type: 'text',
            left: 'center',
            top: 'middle',
            style: {
              text: '暂无该电影的日票房数据',
              fontSize: 16,
              fill: '#999'
            }
          }
        }
      } else {
        option = {
          title: {
            text: `${movie_title || '电影'} 票房走势`,
            left: 'center',
            textStyle: {
              color: '#333'
            }
          },
          tooltip: {
            trigger: 'axis',
            formatter: function(params) {
              return `${params[0].name}<br>${params[0].seriesName}: ${formatBoxOffice(params[0].value)}元`
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: dates,
            axisLabel: {
              rotate: 45,
              interval: 0,
              fontSize: 11,
              margin: 15
            }
          },
          yAxis: {
            type: 'value',
            axisLabel: {
              formatter: value => formatBoxOffice(value) + '元'
            }
          },
          series: [
            {
              name: '日票房',
              type: 'line',
              data: box_offices,
              smooth: true,
              lineStyle: {
                width: 3
              },
              symbolSize: 8,
              areaStyle: {
                opacity: 0.3
              }
            }
          ],
          color: ['#3B82F6']
        }
      }
    } else {
      // 所有电影累计票房
      const { titles, release_dates, box_offices } = visualizationStore.boxOfficeTrendData
      
      // 验证数据是否完整
      if (!titles || !release_dates || !box_offices || titles.length === 0) {
        // 显示无数据的提示
        option = {
          title: {
            text: '电影票房总览',
            left: 'center', 
            textStyle: {
              color: '#333'
            }
          },
          graphic: {
            type: 'text',
            left: 'center',
            top: 'middle',
            style: {
              text: '暂无电影票房数据',
              fontSize: 16,
              fill: '#999'
            }
          }
        }
      } else {
        const seriesData = titles.map((title, index) => ({
          name: title,
          release_date: release_dates[index],
          box_office: box_offices[index]
        }))
        
        // 按上映日期排序
        seriesData.sort((a, b) => new Date(a.release_date) - new Date(b.release_date))
        
        option = {
          title: {
            text: '电影票房总览',
            left: 'center',
            textStyle: {
              color: '#333'
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            },
            formatter: function(params) {
              return `${params[0].name}<br>上映日期: ${seriesData[params[0].dataIndex].release_date}<br>总票房: ${formatBoxOffice(params[0].value)}元`
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '25%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: seriesData.map(item => item.name),
            axisLabel: {
              rotate: 45,
              interval: 0,
              fontSize: 11,
              margin: 15,
              width: 120,
              overflow: 'break',
              align: 'right'
            }
          },
          yAxis: {
            type: 'value',
            axisLabel: {
              formatter: value => formatBoxOffice(value) + '元'
            }
          },
          series: [
            {
              type: 'bar',
              data: seriesData.map(item => item.box_office),
              label: {
                show: true,
                position: 'top',
                formatter: params => formatBoxOffice(params.value)
              }
            }
          ],
          color: ['#3B82F6']
        }
      }
    }
  } catch (error) {
    console.error('初始化票房走势图出错:', error)
    
    // 显示错误提示
    option = {
      title: {
        text: '票房数据加载失败',
        left: 'center',
        textStyle: {
          color: '#333'
        }
      },
      graphic: {
        type: 'text',
        left: 'center',
        top: 'middle',
        style: {
          text: '加载图表数据时出错，请稍后再试',
          fontSize: 16,
          fill: '#999'
        }
      }
    }
  }
  
  boxOfficeTrendInstance.setOption(option)
  
  // 响应式调整
  window.addEventListener('resize', () => boxOfficeTrendInstance?.resize())
}

// 初始化类型比较图
const initGenreComparisonChart = () => {
  if (!visualizationStore.genreComparisonData || !genreComparisonChart.value) return
  
  // 销毁之前的实例
  if (genreComparisonInstance) {
    genreComparisonInstance.dispose()
  }
  
  // 初始化新实例
  genreComparisonInstance = echarts.init(genreComparisonChart.value)
  
  try {
    const { genres, total_box_offices, avg_box_offices, counts } = visualizationStore.genreComparisonData
    
    // 验证数据是否完整
    if (!genres || !total_box_offices || !avg_box_offices || genres.length === 0) {
      // 显示无数据的提示
      const option = {
        title: {
          text: '电影类型票房对比',
          left: 'center',
          textStyle: {
            color: '#333'
          }
        },
        graphic: {
          type: 'text',
          left: 'center',
          top: 'middle',
          style: {
            text: '暂无电影类型对比数据',
            fontSize: 16,
            fill: '#999'
          }
        }
      }
      genreComparisonInstance.setOption(option)
      return
    }
    
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function(params) {
          const genreIndex = params[0].dataIndex
          return `${genres[genreIndex]}<br>总票房: ${formatBoxOffice(total_box_offices[genreIndex])}元<br>平均票房: ${formatBoxOffice(avg_box_offices[genreIndex])}元<br>电影数量: ${counts[genreIndex]}部`
        }
      },
      legend: {
        data: ['总票房', '平均票房'],
        top: 10
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '20%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: genres,
        axisLabel: {
          rotate: 45,
          interval: 0,
          fontSize: 12,
          margin: 15
        }
      },
      yAxis: [
        {
          type: 'value',
          name: '总票房',
          position: 'left',
          axisLabel: {
            formatter: value => formatBoxOffice(value) + '元'
          }
        },
        {
          type: 'value',
          name: '平均票房',
          position: 'right',
          axisLabel: {
            formatter: value => formatBoxOffice(value) + '元'
          }
        }
      ],
      series: [
        {
          name: '总票房',
          type: 'bar',
          data: total_box_offices
        },
        {
          name: '平均票房',
          type: 'line',
          yAxisIndex: 1,
          data: avg_box_offices,
          symbol: 'circle',
          symbolSize: 8,
          lineStyle: {
            width: 2
          }
        }
      ],
      color: ['#3B82F6', '#10B981']
    }
    
    genreComparisonInstance.setOption(option)
  } catch (error) {
    console.error('初始化电影类型票房对比图出错:', error)
    
    // 显示错误提示
    const option = {
      title: {
        text: '类型票房数据加载失败',
        left: 'center',
        textStyle: {
          color: '#333'
        }
      },
      graphic: {
        type: 'text',
        left: 'center',
        top: 'middle',
        style: {
          text: '加载图表数据时出错，请稍后再试',
          fontSize: 16,
          fill: '#999'
        }
      }
    }
    genreComparisonInstance.setOption(option)
  }
  
  // 响应式调整
  window.addEventListener('resize', () => genreComparisonInstance?.resize())
}

// 初始化发行时间热力图
const initReleaseHeatmapChart = () => {
  if (!visualizationStore.releaseHeatmapData || !releaseHeatmapChart.value) return
  
  // 销毁之前的实例
  if (releaseHeatmapInstance) {
    releaseHeatmapInstance.dispose()
  }
  
  // 初始化新实例
  releaseHeatmapInstance = echarts.init(releaseHeatmapChart.value)
  
  try {
    const { data } = visualizationStore.releaseHeatmapData
    
    // 验证数据是否完整
    if (!data || data.length === 0) {
      // 显示无数据的提示
      const option = {
        title: {
          text: '电影发行时间分布',
          left: 'center',
          textStyle: {
            color: '#333'
          }
        },
        graphic: {
          type: 'text',
          left: 'center',
          top: 'middle',
          style: {
            text: '暂无电影发行时间数据',
            fontSize: 16,
            fill: '#999'
          }
        }
      }
      releaseHeatmapInstance.setOption(option)
      return
    }
    
    // 处理数据
    const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    const days = Array.from({ length: 31 }, (_, i) => i + 1)
    
    // 准备热力图数据
    const heatmapData = data.map(item => [item.month - 1, item.day - 1, item.count])
    
    const maxCount = Math.max(...data.map(item => item.count))
    
    const option = {
      title: {
        top: 10,
        left: 'center',
        text: '电影发行时间分布热力图'
      },
      tooltip: {
        position: 'top',
        formatter: function(params) {
          return `${months[params.data[0]]}${params.data[1] + 1}日<br>电影数量: ${params.data[2]}部`
        }
      },
      grid: {
        top: 60,
        left: 40,
        right: 40,
        bottom: 40
      },
      xAxis: {
        type: 'category',
        data: days,
        splitArea: {
          show: true
        }
      },
      yAxis: {
        type: 'category',
        data: months,
        splitArea: {
          show: true
        }
      },
      visualMap: {
        min: 0,
        max: maxCount || 1,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: 10,
        inRange: {
          color: ['#e0f7fa', '#4dd0e1', '#0097a7', '#006064']
        }
      },
      series: [
        {
          type: 'heatmap',
          data: heatmapData,
          label: {
            show: false
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
    
    releaseHeatmapInstance.setOption(option)
  } catch (error) {
    console.error('初始化电影发行时间热力图出错:', error)
    
    // 显示错误提示
    const option = {
      title: {
        text: '发行时间数据加载失败',
        left: 'center',
        textStyle: {
          color: '#333'
        }
      },
      graphic: {
        type: 'text',
        left: 'center',
        top: 'middle',
        style: {
          text: '加载图表数据时出错，请稍后再试',
          fontSize: 16,
          fill: '#999'
        }
      }
    }
    releaseHeatmapInstance.setOption(option)
  }
  
  // 响应式调整
  window.addEventListener('resize', () => releaseHeatmapInstance?.resize())
}

// 初始化票房分布图
const initBoxOfficeDistributionChart = () => {
  if (!visualizationStore.boxOfficeDistributionData || !boxOfficeDistributionChart.value) return
  
  // 销毁之前的实例
  if (boxOfficeDistributionInstance) {
    boxOfficeDistributionInstance.dispose()
  }
  
  // 初始化新实例
  boxOfficeDistributionInstance = echarts.init(boxOfficeDistributionChart.value)
  
  try {
    const { intervals, counts, movies } = visualizationStore.boxOfficeDistributionData
    
    // 验证数据是否完整
    if (!intervals || !counts || intervals.length === 0) {
      // 显示无数据的提示
      const option = {
        title: {
          text: '票房分布区间',
          left: 'center',
          textStyle: {
            color: '#333'
          }
        },
        graphic: {
          type: 'text',
          left: 'center',
          top: 'middle',
          style: {
            text: '暂无票房分布数据',
            fontSize: 16,
            fill: '#999'
          }
        }
      }
      boxOfficeDistributionInstance.setOption(option)
      return
    }
    
    const option = {
      title: {
        text: '电影票房分布',
        left: 'center',
        textStyle: {
          color: '#333'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function(params) {
          return `${params[0].name}<br>电影数量: ${params[0].value}部`
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: intervals,
        axisLabel: {
          rotate: 45,
          interval: 0,
          fontSize: 11,
          margin: 15
        }
      },
      yAxis: {
        type: 'value',
        name: '电影数量'
      },
      series: [
        {
          type: 'bar',
          data: counts,
          barWidth: '60%',
          itemStyle: {
            color: '#6366F1'
          }
        }
      ]
    }
    
    boxOfficeDistributionInstance.setOption(option)
  } catch (error) {
    console.error('初始化票房分布图出错:', error)
    
    // 显示错误提示
    const option = {
      title: {
        text: '票房分布数据加载失败',
        left: 'center',
        textStyle: {
          color: '#333'
        }
      },
      graphic: {
        type: 'text',
        left: 'center',
        top: 'middle',
        style: {
          text: '加载图表数据时出错，请稍后再试',
          fontSize: 16,
          fill: '#999'
        }
      }
    }
    boxOfficeDistributionInstance.setOption(option)
  }
  
  // 响应式调整
  window.addEventListener('resize', () => boxOfficeDistributionInstance?.resize())
}

// 更新票房走势数据
const updateBoxOfficeTrend = async () => {
  try {
    // 更新所有可视化数据，而不仅仅是票房走势
    await visualizationStore.fetchBoxOfficeTrend(selectedMovieId.value || null)
    
    // 如果有选择电影ID，也更新其他三个图表的数据
    if (selectedMovieId.value) {
      await Promise.all([
        visualizationStore.fetchGenreComparison(selectedMovieId.value),
        visualizationStore.fetchReleaseHeatmap(selectedMovieId.value),
        visualizationStore.fetchBoxOfficeDistribution(selectedMovieId.value)
      ])
    } else {
      // 如果没有选择电影ID（即选择"所有电影"），则加载所有默认数据
      await Promise.all([
        visualizationStore.fetchGenreComparison(),
        visualizationStore.fetchReleaseHeatmap(),
        visualizationStore.fetchBoxOfficeDistribution()
      ])
    }
    
    await nextTick()
    // 更新所有图表
    initAllCharts()
  } catch (error) {
    console.error('更新可视化数据出错:', error)
  }
}

// 初始化所有图表
const initAllCharts = () => {
  initBoxOfficeTrendChart()
  initGenreComparisonChart()
  initReleaseHeatmapChart()
  initBoxOfficeDistributionChart()
}

// 监听数据变化
watch(() => visualizationStore.boxOfficeTrendData, () => nextTick(() => initBoxOfficeTrendChart()), { deep: true })
watch(() => visualizationStore.genreComparisonData, () => nextTick(() => initGenreComparisonChart()), { deep: true })
watch(() => visualizationStore.releaseHeatmapData, () => nextTick(() => initReleaseHeatmapChart()), { deep: true })
watch(() => visualizationStore.boxOfficeDistributionData, () => nextTick(() => initBoxOfficeDistributionChart()), { deep: true })

onMounted(async () => {
  // 初始化所有数据
  await visualizationStore.initAllData(selectedMovieId.value)
  
  // 获取电影列表（用于选择器）
  if (moviesStore.movies.length === 0) {
    await moviesStore.fetchMovies()
  }
  movies.value = moviesStore.movies
  
  // 初始化图表
  nextTick(() => {
    initAllCharts()
  })
})
</script> 