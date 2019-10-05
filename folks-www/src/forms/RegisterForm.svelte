<script>
    import { onMount } from 'svelte'
  import AjaxForm from "./AjaxForm.svelte";
  export let action = "/";
  export let method = "POST";
  let username = "";
  let password = "";
  let invite = ""

    onMount(() => {
        let params = new URLSearchParams(window.location.search)
        if (params.has('invite')) {
            invite = invite || params.get('invite')
        }
    })

  let formValue = () => {
    return {
      username,
      password,
      invite
    };
  };
</script>

<style>
  input {
    display: block;
  }
</style>

<AjaxForm on:success on:error {action} {formValue}>
  <div slot="fields">
    <label for="username">Юзернейм:</label>
    <input bind:value={username} id="username" type="text" name="username" />
    <label for="password">Пароль:</label>
    <input
      bind:value={password}
      id="password"
      type="password"
      name="password" />
    <label for="invite">Инвайт</label>
    <input bind:value={invite} id="invite" type="text" name="invite" />
    <button type="submit">Зарегистрироваться</button>
  </div>
  <div slot="loading">...пытаемся зарегистрироваться</div>
</AjaxForm>
