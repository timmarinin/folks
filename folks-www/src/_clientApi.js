import axios from 'axios'

export const client = axios.create({
    withCredentials: true,
    headers: {
        'X-Client-Api': '1',
    },
})

export const apiClient = axios.create({
    baseURL: process.env.NODE_ENV === 'development' ? 'http://localhost:8000/v2' : 'https://the-folks.com/api/v2',
    headers: {
        'X-Client-Api': '1',
    },
})

export const configureClientApi = token => {
    if (token) {
        apiClient.defaults.headers['Authorization'] = 'Bearer ' + token
    } else {
        if (apiClient.defaults.headers['Authorization']) {
            delete apiClient.defaults.headers['Authorization']
        }
    }
}

export const getMyHats = () => {
    return apiClient.get('/me/hats')
}

export const loadPosts = () => {
    return apiClient.get('/feed')
}

export const getHat = ({ username }) => {
    return apiClient.get('/hats/' + username)
}

export const getHats = () => apiClient.get('/hats')

export const subscribe = ({ username }) => {
    return apiClient.post('/subscriptions', {
        username
    })
}

export const updatePost = ({ id, body }) => apiClient.patch('/feed/' + id, { body })

export const unsubscribe = ({ username }) => {
    return apiClient.delete('/subscriptions/' + username)
}

export const isSubscribed = ({ username }) => {
    return apiClient.get('/subscriptions/' + username)
}

export const getSubscriptions = () => {
    return apiClient.get('/subscriptions')
}

export const getFlag = (flag) => {
    return apiClient.get('/flags/' + flag)
}