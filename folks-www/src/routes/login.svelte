<script context="module">
    export function preload(page, session) {
        if (session && session.token) {
            return this.redirect(302, '/feed')
        } else {
            return {}
        }
    }
</script>

<script>
    import LoginForm from "../forms/LoginForm.svelte";
  	import { stores, goto } from '@sapper/app';
    const { session } = stores();
    let isLoggedIn = false;
    function goToFeed() {
        isLoggedIn = true;
        setTimeout(() => {
            window.location.href = '/feed'
        }, 50);
    }
</script>

<svelte:head>
  <title>Логин</title>
</svelte:head>

<h2>Войти</h2>

<LoginForm on:success={goToFeed} action="/login"></LoginForm>
{#if isLoggedIn}
Логинимся…
{/if}