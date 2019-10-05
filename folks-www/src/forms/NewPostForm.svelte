
<script>
    import { stores } from "@sapper/app";
    import { client } from "../_clientApi.js";
    import ListErrors from "../components/ListErrors.svelte";
    import { createEventDispatcher } from 'svelte'
    import AjaxForm from './AjaxForm.svelte'
    import HatSelect from '../components/HatSelect.svelte'
    import ImageUploader from '../components/ImageUploader.svelte'
    
    let body = ''
    let username = ''
    let attachments = []
    let hasOtherContent = false

    let dispatch = createEventDispatcher()
    let uploader

    function onSuccess(event) {
        dispatch('posted', event.detail)
        body = ''
    }
    function changeHat(h) {
      username = h.detail
    }

    let submitBtn

    function submitOnCtrlEnter(e) {
      if (e.keyCode == 13 && (e.metaKey || e.ctrlKey)) {
        submitBtn.click() 
      }
    }

    function setAttachments({detail}) {
        attachments = detail;
    }

    let isProgress = false;
    let errors = [];

    async function submit() {
        console.log('NewPostForm.submit.start');
        errors = []
        try {
            isProgress = true;

            attachments = await uploader.upload()

            let val = {
                username,
                body,
                attachments
            }
            console.log('NewPostForm.submit.value', val)
            const json = await client.post('/feed', val);
            if (json.data.errors) {
                console.log('NewPostForm.submit.json.errors', json.data.errors);
                isProgress = false;
                errors = json.data.errors;
            } else {
                isProgress = false;
                console.log('NewPostForm.submit.json.data', json.data);
                dispatch("success", json.data);
            }
        } catch (e) {
        isProgress = false;
        console.log('NewPostForm.submit.error', e);
        errors = Array.isArray(e) ? errors.concat(e) : [e];
        dispatch("error", errors);
        }
        console.log('NewPostForm.submit.end')
    }
</script>


<style>
    .new-post__body {
        width: 100%;
        max-width: 600px;
        min-height: 3em;
        padding: .3rem;
        font-family: inherit;
        font-size: 16px;

        display: block;
    }

    .new-post {
        --margin: 1rem;
        padding-top: 1em;
        padding-bottom: 1em;
        padding-left: var(--margin);
        padding-right: var(--margin);
        margin-bottom: var(--margin);

        margin-left: calc(-1 * var(--margin));
        margin-right: calc(-1 * var(--margin));
        background: #eee;
    }

    label {
        margin-top: 1rem;
        display: block;
    }

    .new-post__submit {
        margin-top: 1rem;
        padding: .3rem;
        font-size: inherit;
    }
</style>

<form action="/feed" method="POST" class="new-post" on:submit|preventDefault={submit}>
    <div>
        
        <label for="body">Текст поста</label>

        <textarea required={!hasOtherContent} on:keydown={submitOnCtrlEnter} bind:value={body} class="new-post__body" name="body" />

        <label>
            Шляпа
            <HatSelect bind:value={username} />
        </label>
        
        <ImageUploader bind:this={uploader} on:update={setAttachments} />

        <button class="new-post__submit" bind:this={submitBtn} type="submit">Запостить</button>
        
    </div>
      {#if isProgress}
        <div>Постим...</div>
    {:else if errors.length}
      <ListErrors {errors} />
    {/if}
</form>

