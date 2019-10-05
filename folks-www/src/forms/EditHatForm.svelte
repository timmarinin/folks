<script>
import AjaxForm from './AjaxForm.svelte'
export let hat, new_hat
let about_me = new_hat ? '' : hat.about_me
let display_name = new_hat ? '' :hat.display_name
let add_user = ''
let username = ''

let formValue = () => ({
    about_me,
    display_name,
    username: new_hat ? username : hat.username,
    new_hat,
    add_user
})
</script>

<style>
label {
    display: block;
    margin: 1rem 1rem 1rem 0;
    width: 100%;
    box-sizing: border-box;
}


textarea {
    display: block;
    width: 100%;
}

:global(.edit-post-form) {
    margin-bottom: 1.4rem;
    margin-top: 1.4rem;
}

:global(.edit-post-form) + :global(.edit-post-form) {
    border-top: 1px solid #eee;
}

</style>

<AjaxForm {formValue} class="edit-post-form" action={"/settings/hats"}>
    <div slot="fields">
        {#if !new_hat}
            <h3>{hat.username}</h3>
            <input type="hidden" value={hat.username} name="username" />
        {:else}
            <h3>Новая шляпа</h3>
            <input type="hidden" value={1} name="new_hat" />
            <label>Юзернейм
                <input bind:value={username} name="username" />
            </label>
        {/if}
        
        <label>Дисплейнейм
            <input bind:value={display_name} name="display_name" />
        </label>
        <label>Эбаут
        <textarea bind:value={about_me} name="about_me" />
        </label>
        
        {#if !new_hat}
            <label>
                Выдать пользователю
                <input type="text" name="add_user" />
            </label>
            <button type="submit">Отредактировать</button>
        {:else}
            <button type="submit">Создать</button>
        {/if}
    </div>
</AjaxForm>