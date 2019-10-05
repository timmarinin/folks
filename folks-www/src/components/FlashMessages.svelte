<script>
    import { stores } from '@sapper/app';
	const { session } = stores();
    let flash = $session.flash;
</script>

{#if flash && flash.length}
    <ul class="flash">
        {#each flash as f}
            <li class="flash__message">{f}</li>
        {/each}
    </ul>
{/if}

<style>
.flash {
    list-style: none;
    padding-left: 0;
}

.flash__message {
    background: var(--accent-color);
    padding: 1rem;
    border-radius: .5rem;
    margin-top: 1rem;
}
</style>