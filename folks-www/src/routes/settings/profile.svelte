<script context="module">
import {subscribe, unsubscribe, getSubscriptions} from '../../_clientApi.js'
export async function preload(page, session) {
    if (!session || !session.user) {
        return this.redirect(302, '/login')
    }

    const resp = await getSubscriptions()
    return {
        subscriptions: resp.data.subscriptions
    }
}
</script>
<script>
export let subscriptions = [{}]
</script>

<h3>Подписки</h3>

<ul>
{#each subscriptions as subscription (subscription.username) }
    <li><a rel="prefetch" href="{'/u/' + subscription.username}">@{subscription.username}</a> {subscription.display_name}</li>
{/each}
</ul>