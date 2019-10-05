<script context="module">
    import {getMyHats} from '../../_clientApi.js'
    export async function preload(page, session) {
        if (!session || !session.token) {
            return this.redirect(302, '/login')
        }

        let hats = await getMyHats()
        return {
            hats: hats.data.hats
        }
    }
</script>

<svelte:head>
<title>Настройки шляп</title>
</svelte:head>

<script>
import EditHatForm from '../../forms/EditHatForm.svelte'
export let hats = []

async function reload() {
    let resp = await getMyHats()
    hats = resp.data.hats;
}
</script>

<h2>Настройки шляп</h2>

{#each hats as hat (hat.username)}
    <EditHatForm hat={hat} />
{:else}
Такого быть не должно… <button on:click={reload}>попробовать ещё раз</button>
{/each}
<EditHatForm new_hat={true} />
