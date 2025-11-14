import api from '../lib/api'

export const authService = {
  async login(email, password) {
    console.log(email, password)
    const response = await api.post('/auth/login/', { email, password })
    console.log(response.data)
    const { access, refresh, user } = response.data
    
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('user', JSON.stringify(user))
    
    return { access, refresh, user }
  },

  async refreshToken() {
    const refresh = localStorage.getItem('refresh_token')
    if (!refresh) throw new Error('No refresh token')
    
    const response = await api.post('/auth/refresh/', { refresh })
    const { access } = response.data
    localStorage.setItem('access_token', access)
    return access
  },

  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  },

  getCurrentUser() {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  },

  isAuthenticated() {
    return !!localStorage.getItem('access_token')
  },
}

