<script>
    import Post from './Post.svelte'
    import NewPostForm from '../forms/NewPostForm.svelte'
    import Introduction from './Introduction.svelte'
    export let posts = []
    export let readOnly = false;
</script>

<style>
.feed {
    display: grid;
    grid-template-columns: 1fr;
    grid-gap: .5rem;
    width: 100%;
}

</style>


<div class="feed">
    {#if !readOnly}
        <NewPostForm on:posted='{(e) => { posts = [e.detail.post, ...posts] } }' action="/feed" />
    {/if}

    {#each posts as post (post.id)}
        <Post {post} />
    {:else}
        <Introduction />
    {/each}
</div>