<script>
import {createEventDispatcher} from 'svelte'
export let src = ''

const dispatch = createEventDispatcher()
</script>
<style>
img {
    width: 100%;
}
button {
    background: var(--main-color);
    color: var(--button-text-color);
    padding: .3rem .7rem;
}
div {
    padding: .3rem;
}
</style>
<div>
    <button on:click={() => dispatch('delete')}>убрать</button>
    <img {src} alt="" />
</div>