import { writable, readable } from 'svelte/store'
import { getMyHats } from './_clientApi.js'

export const hats = writable({})

export const wearableHats = writable([])

export const me = writable({
    username: '', display_name: ''
})
export const user = writable({})

export const feed = writable({ posts: [] })

export const setupFaye = (client) => {
    user.subscribe(u => {
        if (!u) {
            return;
        }
        if (!u.reader_feed) {
            return
        }
        client.subscribe('/reader_feed/' + u.reader_feed, (msg) => {
            console.log('msg', msg)
            feed.update(f => {
                console.log(f, msg)

                f.posts = [msg.post, ...f.posts]
                return f
            })
        })
    })
}