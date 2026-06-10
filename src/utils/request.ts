import axios, { type AxiosInstance, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'

const request: AxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
})

request.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

request.interceptors.response.use(
    (response: AxiosResponse) => {
        return response.data
    },
    (error) => {
        const msg = error.response?.data?.message || error.message || '请求失败'
        console.error('[API Error]', msg)
        return Promise.reject(error)
    }
)

export default request