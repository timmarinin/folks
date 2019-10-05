<script context="module">
    export async function preload(page, session) {
        if (!session || !session.token) {
            return this.redirect(302, '/login')
        }
    }
</script>

<svelte:head>
<title>Настройки</title>
</svelte:head>

<script>

</script>

<h2>Настройки</h2>

<li><a href="/settings/invites">Инвайты</a></li>
<li><a href="/settings/hats">Шляпы</a></li>
<li><a href="/settings/profile">Профиль</a></li>