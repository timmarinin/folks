<script>
  import { createEventDispatcher } from "svelte";
  import { stores } from "@sapper/app";
  import { client } from "../_clientApi.js";
  const { session } = stores();
  let token = $session.token;
  let dispatch = createEventDispatcher();

  import ListErrors from "../components/ListErrors.svelte";
  export let action;
  let className = 'ajax-form'
  export let formValue = () => {
    throw new Error("Укажи formValue");
  };

  let isProgress = false;
  let errors = [];

export {
  className as class
}
  async function submit() {
    console.log('AjaxForm.submit.start');
    errors = []
    try {
      isProgress = true;
      let val = formValue()
      console.log('AjaxForm.submit.value', val)
      const json = await client.post(action, val);
      if (json.data.errors) {
        console.log('AjaxForm.submit.json.errors', json.data.errors);
        isProgress = false;
        errors = json.data.errors;
        dispatch("error", errors);
      } else {
        isProgress = false;
        console.log('AjaxForm.submit.json.data', json.data);
        dispatch("success", json.data);
      }
    } catch (e) {
      isProgress = false;
      console.log('AjaxForm.submit.error', e);
      errors = Array.isArray(e) ? errors.concat(e) : [e];
      dispatch("error", errors);
    }
    console.log('AjaxForm.submit.end')
  }
</script>

<form method="POST" class={className} {action} on:submit|preventDefault={submit}>
  <slot name="fields" {isProgress}>Пустая форма, так быть не должно.</slot>
  {#if isProgress}
    <slot name="loading">Отправляем...</slot>
  {:else if errors.length}
    <slot error={errors} name="error">
      <ListErrors {errors} />
    </slot>
  {/if}
</form>
