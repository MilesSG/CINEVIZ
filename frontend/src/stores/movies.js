import { defineStore } from 'pinia'
import axios from 'axios'

export const useMoviesStore = defineStore('movies', {
  state: () => ({
    movies: [],
    movie: null,
    genres: [],
    topMovies: [],
    latestMovies: [],
    loading: false,
    error: null,
    searchQuery: '',
    selectedGenre: '',
    totalCount: 0
  }),
  
  getters: {
    getMovieById: (state) => (id) => {
      return state.movies.find(movie => movie.id === id) || null
    }
  },
  
  actions: {
    async fetchMovies(params = {}) {
      this.loading = true
      this.error = null
      
      try {
        const queryParams = new URLSearchParams()
        
        if (params.title || this.searchQuery) {
          queryParams.append('title', params.title || this.searchQuery)
        }
        
        if (params.genre || this.selectedGenre) {
          queryParams.append('genre', params.genre || this.selectedGenre)
        }
        
        const response = await axios.get(`/api/movies?${queryParams.toString()}`)
        
        this.movies = response.data.movies
        this.totalCount = response.data.count
        
        return this.movies
      } catch (error) {
        this.error = error.response?.data?.message || '获取电影列表失败'
        return []
      } finally {
        this.loading = false
      }
    },
    
    async fetchMovie(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`/api/movies/${id}`)
        
        this.movie = response.data
        return this.movie
      } catch (error) {
        this.error = error.response?.data?.message || '获取电影详情失败'
        return null
      } finally {
        this.loading = false
      }
    },
    
    async fetchTopMovies(limit = 10) {
      this.loading = true
      
      try {
        const response = await axios.get(`/api/movies/top?limit=${limit}`)
        
        this.topMovies = response.data.movies
        return this.topMovies
      } catch (error) {
        this.error = error.response?.data?.message || '获取热门电影失败'
        return []
      } finally {
        this.loading = false
      }
    },
    
    async fetchLatestMovies(limit = 10) {
      this.loading = true
      
      try {
        const response = await axios.get(`/api/movies/latest?limit=${limit}`)
        
        this.latestMovies = response.data.movies
        return this.latestMovies
      } catch (error) {
        this.error = error.response?.data?.message || '获取最新电影失败'
        return []
      } finally {
        this.loading = false
      }
    },
    
    async fetchGenres() {
      try {
        const response = await axios.get('/api/movies/genres')
        
        this.genres = response.data.genres
        return this.genres
      } catch (error) {
        this.error = error.response?.data?.message || '获取电影类型失败'
        return []
      }
    },
    
    setSearchQuery(query) {
      this.searchQuery = query
    },
    
    setSelectedGenre(genre) {
      this.selectedGenre = genre
    },
    
    clearFilters() {
      this.searchQuery = ''
      this.selectedGenre = ''
    }
  }
}) 