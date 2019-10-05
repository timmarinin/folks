<script context="module">
import {getHats, getSubscriptions} from '../../_clientApi.js'
export async function preload(page, session) {
    if (!session || !session.user) {
        return this.redirect(302, '/login')
    }

    return {
        hats: await getHats().then(r => r.data.hats),
        subscriptions: await getSubscriptions().then(r => r.data.subscriptions.reduce((byName, h) => {
            byName[h.username] = true
            return byName
        }, {}))
    }
}
</script>
<script>
export let hats
export let subscriptions

const random_about_mes = [
    'Не ввожу тексты о себе в странные текстовые поля в интернете',
    'Пишу буквы, жму энтер',
    'Мой настоящий дисплейнем — Бэтмен',
    'Надо будет заполнить этот текст',
    'Ещё не дошли руки заполнить это поле',
    'Это поле можно редактировать?',
    '…',
    'Самый тяжёлый вопрос',
    'Сколько ещё вопросов в этой анкете?',
    'Не лайкаю, но осуждаю',
    'Лайкаю, но осуждаю',
    'О себе — дышу воздухом.',
    '(ээээ)'
]

function pick_random() {
    return random_about_mes[Math.floor(Math.random() * random_about_mes.length)]
}
</script>

<style>
</style>

<h3>Шляпы</h3>

{#each hats as hat (hat.username)}
<article>
    <h4><a href="/u/{hat.username}">@{hat.username}</a>{#if hat.display_name != hat.username} — {hat.display_name}{/if}</h4>
    <dl>
        <dt>О себе</dt>
        <dd>{hat.about_me || pick_random() }</dd>
        <dt>С нами с</dt>
        <dd>{new Date(hat.created_at).toLocaleDateString()}</dd>
        <dt>Подписка</dt>
        <dd>
            {#if subscriptions[hat.username]}
                есть
            {:else}
                нет
            {/if}
        </dd>
    </dl>
</article>
{/each}