<script context="module">
import {getFlag} from '../_clientApi.js'
export async function preload(page, session) {
	if (session && session.user) {
		return this.redirect(302, '/feed')
	}

	try {
		let flag = await getFlag('maintenance')
		return {
			maintenance: flag.data.flag.value != 0
		}
	} catch (e) {
		console.log(e)
		return {
			maintenance: true
		}
	}
}
</script>
<script>
export let maintenance = true;
</script>

<svelte:head>
	<title>Фолкс</title>
</svelte:head>

<h1>Folks</h1>

{#if maintenance}
	<p>Сейчас нельзя залогиниться, Тим обновляет сервис</p>
{/if}

<p>Зачем твиттер, если есть мы?</p>

<p>Официально лучше Инстаграма на айпаде&trade;</p>