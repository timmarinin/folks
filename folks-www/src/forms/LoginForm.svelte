<script>
    import AjaxForm from './AjaxForm.svelte'
    export let action
    let username = ''
    let password = ''

    let formValue = () => {
        return {
            username,
            password,
        }
    }
</script>

<style>
    input {
        display: block;
        font-size: 16px;
    }
</style>

<AjaxForm on:success {action} {formValue}>
    <div slot="fields">
        <label for="username">Юзернейм:</label>
        <input
            bind:value={username}
            id="username"
            type="text"
            name="username" />
        <label for="password">Пароль:</label>
        <input
            bind:value={password}
            id="password"
            type="password"
            name="password" />
        <button type="submit">Залогиниться</button>
    </div>
    <div slot="loading">...пытаемся залогиниться</div>
</AjaxForm>
