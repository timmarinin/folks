<script>
import Post from '../../components/Post.svelte'
import ListErrors from '../../components/ListErrors.svelte'
import FeedContainer from '../../components/FeedContainer.svelte'

import {subscribe, unsubscribe} from '../../_clientApi.js'
export let hat
let errors = []
export let subscribed
export let posts
let inProgress = false
async function onSubscribe() {
    inProgress = true
    errors = []
    try {
        await subscribe({
            username: hat.username
        })
        subscribed = true
    } catch(e) {
        errors = [e]
    }
    inProgress = false
}
async function onUnsubscribe() {
    inProgress = true
    errors = []
    try {
        await unsubscribe({
            username: hat.username
        })
        subscribed = false
    } catch(e) {
        errors = [e]
    }
    inProgress = false
}
</script>

<h2>{hat.username}</h2>
<p>{hat.display_name}</p>

{#if subscribed}
Подписка есть!

<button on:click={onUnsubscribe}>Отписаться</button>
{:else}
Нет подписки
<button on:click='{onSubscribe}'>Подписаться</button>
{/if}


<p>{hat.about_me}</p>


{#if errors.length}
<ListErrors {errors} />
{/if}

{#if inProgress}
Работаем...
{/if}

<h3>Посты</h3>

<FeedContainer readOnly={true} posts={posts} />