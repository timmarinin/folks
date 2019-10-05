<script>
import {createEventDispatcher} from 'svelte'

import ImagePreview from './ImagePreview.svelte'

const dispatch = createEventDispatcher()

export function upload() {
    console.log('should upload', files)
    return [
        'attach1',
        'attach2'
    ]
}

let files = []
let previews = []

function uploadFiles() {
    console.log('files', files)
}

function selectedFile(e) {
    console.log('selectedFile')
    files = files.concat(e.target.files)
    console.log(files);
    for (let f of e.target.files) {
        console.log('working on', f)
        let i = previews.length
        previews[i] = ''
        console.log('image #', i)
        let reader = new FileReader()
        reader.onload = e => {
            console.log('loaded as datauri', i)
            previews[i] = e.target.result
        }
        reader.readAsDataURL(f)
    }
    dispatch('update', files)
}

function dropFile(index) {
    files.splice(index, 1);
    previews.splice(index, 1);
    files = files;
    previews = previews;
}

</script>
<style>
input {
    display: none;
}
label {
    display: inline-block;
    background: var(--main-color);
    border-radius: 6px;
    color: var(--button-text-color);
    padding: .3rem .7rem;
}

label:hover {
    background: var(--main-hover-color);
    color: var(--button-text-hover-color);
}
label:active {
    background: var(--main-active-color);
    color: var(--button-text-active-color);
}

.preview {
    display: grid;
    grid-template-columns: repeat(3, auto);
}
</style>

<form enctype="multipart/form-data" on:submit|preventDefault={uploadFiles}>
    <input on:change={selectedFile} type="file" name="file" multiple id="upload-file">
    <label for="upload-file">Добавить картинки</label>
    <div class="preview">
        {#each previews as p, i}
            <ImagePreview src={p} on:delete={() => dropFile(i)} />
        {/each}
    </div>
</form>