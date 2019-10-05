<article class="h-entry post">
    <div class="e-content post__content">
        {#if !isEditing}
            {@html post.body}
            {#if post.photo_url}
                <img alt="{post.photo_alt || ""}" class="post__photo" src="{post.photo_url}">
            {/if}
            {#if post.attachments}
                {#each post.attachments as attach (attach.id) }
                    {#if attach.attach_type == 'photo'}
                        <img class="post__photo" src="{attach.url}" alt='attached photo' />
                    {/if}
                {/each}
            {/if}
        {:else}
            <textarea class="post__textarea-edit" bind:value={editedBody} name="body"></textarea>
            <button disabled={saving} on:click={saveUpdate}>обновить</button>
            <ListErrors {errors} />
            {#if saving}
            Сохраняем...
            {/if}
        {/if}
    </div>
    <div class="post__meta">
        <time class="post__posted-at" datetime="{posted_at.toISOString()}">{posted_time}</time>
        {#if editable}
            <button class="post__edit" on:click={toggleEditing} arial-label="отредактировать">🖊</button>
        {/if}
    </div>
    <img class="post__author-pic" alt="" src="https://placekitten.com/36/36">
    <a class="post__author" rel="author" href="/u/{post.author.username}">@{post.author.username}{#if post.author.display_name != post.author.username}&nbsp;{post.author.display_name}{/if}</a>
</article>

<script>
export let post
import {user, wearableHats} from '../stores.js'
import {updatePost} from '../_clientApi.js'
import ListErrors from './ListErrors.svelte'
let editedBody = ''

let posted_at = new Date(post.posted_at + 'Z')
let posted_time = posted_at.toLocaleTimeString('ru-RU').split(':').slice(0, -1).join(':')
let author = post.author

let editable = false;
let isEditing = false;
let saving = false
let errors = []
$: editable = author.username == $user.username || $wearableHats.filter(h => h.username === author.username).length > 0

function toggleEditing() {
    if (editable) {
        if (editedBody !== post.body) {
            editedBody = post.body;
        }
        isEditing = !isEditing
    }
}

async function saveUpdate() {
    errors = []
    saving = true
    try {
        post = await updatePost({
            id: post.id,
            body: editedBody
        }).then(r => r.data.post)
        author = post.author
        posted_at = new Date(post.posted_at + 'Z')

        isEditing = false
    } catch(e) {
        errors = [e]
    }
    saving = false
}

</script>
<style>
.post {
    display: grid;
    grid-template-columns: 36px 1fr 5ch;
    grid-template-rows: auto 1fr;
    grid-gap: 1rem;
    margin-bottom: 1.5rem;
    width: 100%;
}

.post + .post {
    border-top: 1px solid #eee;
    padding-top: 1.5rem;
}

.post__author {
    grid-row: 1;
    grid-column: 2 / 3;
    text-decoration: none;
}

.post__author-pic {
    grid-row: 1 / 4;
    grid-column: 1;
    vertical-align: -2px;
}

.post__content {
    grid-row: 2;
    grid-column: 2 / 4;
    word-break: break-word;
    max-width: 600px;
}

.post__meta {
    grid-row: 3;
    grid-column: 2 / 3;
}

.post__like {
    text-decoration: none;
}

.post__photo {
    display: block;
    width: 100%;
    max-width: 600px;
    object-fit: contain;
    image-orientation: from-image;
}

.post :global(img) {
    width: 100%;
    max-width: 600px;
}

.post :global(iframe) {
    max-width: 100%;
}

.post__edit {
    padding-left: 0;
    padding-right: 0;
    border: none;
    background: none;
    font-size: .86rem;
    cursor: pointer;
}

.post__textarea-edit {
    display: block;
    width: 100%;
    min-height: 3.6rem;
}
</style>