<script>
	import { stores } from '@sapper/app'
	const { session } = stores()
	let is_logged_in = Boolean($session.user)
	let username = $session.user && $session.user.username
	export let segment
</script>

<style>
	nav {
		margin: -1rem;
		margin-bottom: 0;
		padding: 1rem;
		background: var(--main-color);
		color: var(--button-text-color);
	}
	ul {
		list-style: none;
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		padding: 0;
		margin: 0;
	}

	li {
		margin: 0;
		padding-right: .3rem;
	}

	a {
		text-decoration: none;
		color: inherit;
	}
</style>

<nav>
	<ul>  
		{#if ! is_logged_in}
			<li>
				<a href="{'/'}">Folks</a>
			</li>
			<li>
				<a href="{'/register'}">зарегистрироваться</a>
			</li>
			<li>
				<a href="{'/login'}">войти</a>
			</li>
		{:else}
			<li>
				<a href="{'/feed'}">Folks</a>
			</li>
			<li>
				<a href="{'/settings'}">настройки</a>
			</li>
			<li>
				<a href="{'/new-post'}">новый пост</a>
			</li>
		{/if}
	</ul>
</nav>
