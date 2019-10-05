<script context="module">
    import { loadPosts } from '../../_clientApi.js'
    export async function preload(page, session) {
        if (!session || !session.user) {
            console.error('redirecting', session)
            return this.redirect(302, '/login')
        }

        let response = await loadPosts()
            
        return {
            posts: response.data.posts || [],
        }
    }
</script>

<script>
import FeedContainer from '../../components/FeedContainer.svelte'
import { feed } from '../../stores.js'
export let posts = []

feed.update(feed => {
    feed.posts = posts
    return feed
})

feed.subscribe(feed => {
    if (feed && feed.posts.length > 0) {
        posts = feed.posts
    }
})

</script>

<FeedContainer {posts} />

<svelte:head>
    <title>Фид</title>
</svelte:head>