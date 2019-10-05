<script context="module">
    import { configureClientApi, getMyHats } from '../_clientApi.js'
    export async function preload(page, session) {
        if (session) {
            if (session.token) {
                configureClientApi(session.token)
                try {
                    let resp = await getMyHats()
                    console.log('Запрос: ' + page.path)
                    return {
                        user: session.user,
                        hats: resp.data.hats || [ { username: session.user.username }]
                    }
                } catch (e) {
                    console.log('Не получилось получить шляпы для пользователя', session.user, e)
                }
            } else {
                configureClientApi(null)
            }
        }
        return {
            user: null,
            hats: []
        }
    }
</script>

<script>
    import { onMount } from 'svelte'
    import Nav from '../components/Nav.svelte'
    import FlashMessages from '../components/FlashMessages.svelte'
    import { wearableHats, setupFaye , user as userStore} from '../stores.js'
    export let segment
    export let user = {}
    export let hats = []
    userStore.set(user)
    if (hats && hats.length) {
        wearableHats.set(hats)
    }
    onMount(() => {
        if (typeof window.Faye !== 'undefined') {
            var client = new Faye.Client('/faye');
            setupFaye(client);
        } else {
            console.log('no faye')
        }
    })


</script>

<style>
header, footer, .content {
    grid-column: 2;
}
</style>

<header class="site-header">
    <Nav {segment} />
</header>
<div class="content">
    <FlashMessages />
    <slot />
</div>

{#if user && user.reader_feed }
    <script src="/faye/client.js"></script>
{/if}
<footer>Folks. 2019-20xx. s v e l t e</footer>
