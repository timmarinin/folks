<script context="module">
    export async function preload(page, session) {
        if (!session || !session.user) {
            console.error('redirecting', session)
            return this.redirect(302, '/login')
        }
    }
</script>

<script>
import {goto} from '@sapper/app';
import NewPostForm from '../forms/NewPostForm.svelte'

</script>

<NewPostForm on:posted='{(e) => { goto('/feed') } }' action="/feed"/>

<svelte:head>
    <title>Фид :: новый пост</title>
</svelte:head>