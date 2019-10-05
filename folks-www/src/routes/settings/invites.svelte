<script context="module">
    import {apiClient} from '../../_clientApi.js'
    export async function preload(page, session) {
        if (!session || !session.token) {
            return this.redirect('/login')
        }

        let resp = await apiClient.get('/me/invites')
        return {
            invites: resp.data.invites
        }
    }
</script>
<script>
export let invites
let inProgress = false
let error = ''

async function gen_invites() {
    inProgress = true
    error = ''
    let json = await apiClient.post('/settings/gen_invites')
    console.log(json)
    if (json.data.invite) {
        console.log(json.data.invite)
        invites = [json.data.invite, ...invites]
    } else if (json.data.error) {
        error = json.data.error
    }
    inProgress = false
}
</script>

<h3>Инвайты</h3>


<table>
<thead>
<th>Пригласили</th>
<th>Код</th>
<th>Ссылка</th>
</thead>
<tbody>
{#each invites.filter(i => !i.redeemed_at) as invite (invite.invite_code) }
    <tr>
        <td>
            <em>пока не использован</em>
        </td>
        <td>
        {invite.invite_code}
        </td>
        <td>
        <a href="/register/?invite={invite.invite_code}">https://the-folks.com/register/?invite={invite.invite_code}</a>
        </td>
    </tr>
{/each}
</tbody>
</table>

<button disabled={inProgress} on:click={gen_invites}>Получить ещё инвайт</button>
{#if error}{error}{/if}

<h3>Окэшенные инвайты</h3>

<table>
<thead>
<th>Пригласили</th>
<th>Код</th>
<th>Ссылка</th>
</thead>
<tbody>
{#each invites.filter(i => i.redeemed_at) as invite (invite.invite_code) }
    <tr>
        <td>{invite.redeemer && invite.redeemer.username || 'ой'} {new Date(invite.redeemed_at).toISOString().split('T')[0]}

        </td>
        <td>
        {invite.invite_code}
        </td>
        <td>
        <a href="/register/?invite={invite.invite_code}">https://the-folks.com/register/?invite={invite.invite_code}</a>
        </td>
    </tr>
{/each}
</tbody>
</table>