<script>
    import RegisterForm from '../forms/RegisterForm.svelte'

    function onSuccess() {
        setTimeout(() => {
            window.location.href = '/'
        }, 50)
    }
</script>

<svelte:head>
    <title>Регистрация</title>
</svelte:head>

<p>Внутри: Моне vs. Мане, котики, нытьё про работу.</p>

<RegisterForm on:success={onSuccess} action="/register" method="POST" />