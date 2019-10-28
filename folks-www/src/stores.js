import { writable, readable } from 'svelte/store'
import { getMyHats } from './_clientApi.js'

export const hats = writable({})

export const wearableHats = writable([])

export const me = writable({
    username: '', display_name: ''
})
export const user = writable({})

export const feed = writable({ posts: [] })
