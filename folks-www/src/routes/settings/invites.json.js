import { getInvites, genInvite } from '../../_serverApi.js'

export async function get(req, res) {
    let json = await getInvites()
    if (json.data.invites) {
        res.json({
            data: {
                invites: json.data.invites
            }
        })
    }
}

export async function post(req, res) {
    let json = await genInvite()
        .then(data => ({ invite: data.data.invite }))
        .catch(error => {
            if (error.response.data.message === 'UNREDEEMED') {
                return { error: 'UNREDEEMED'}
            } else {
                return Promise.reject(error)
            }
        })
    if (json.error) {
        return res.json({
            error: 'UNREDEEMED'
        })
    }
    if (json.invite) {
        res.json({
            invite: json.invite
        })
    }
}