<script>
    import { createEventDispatcher, onMount } from 'svelte'
    let dispatch = createEventDispatcher()
    import { wearableHats, me } from '../stores.js'

    let hat_name = ""

    wearableHats.subscribe((hats) => {
        if (hat_name === "" && hats.length) {
            hat_name = me.username // || hats[0].username
            onChange()
        }
    })

    function onChange() {
        dispatch('choose', hat_name)
    }

    export let value = ""
</script>

<select on:change={onChange} bind:value name="username">
    {#each $wearableHats as hat (hat.username)}
        <option value={hat.username}>{hat.display_name || hat.username}</option>
    {/each}
</select>
