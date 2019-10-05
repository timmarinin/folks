<script context="module">
export function preload(page, session) {
    if (!session || !session.user) {
        return this.redirect(302, '/login')
    }
}
</script>
<script>
import Introduction from '../../components/Introduction.svelte'
</script>

<Introduction />