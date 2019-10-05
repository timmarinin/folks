<script context="module">
    import {getHat, isSubscribed} from '../../_clientApi.js'
    export async function preload(page, session) {
        if (!session || !session.user) {
            return this.redirect(302, '/login')
        }
        const username = page.params.username
        const r = await getHat({ username })
        return {
            hat: r.data.hat,
            posts: r.data.posts,
            subscribed: await isSubscribed({ username }).then(r => r.data.subscribed)
        }
    }
</script>

<script>
import Profile from './_Profile.svelte'
export let hat
export let subscribed
export let posts
</script>

<Profile {hat} {subscribed} {posts} />