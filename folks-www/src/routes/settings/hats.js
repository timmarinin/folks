import {editHat, createHat, flashRedirect} from '../../_serverApi.js'

export async function post(req, res) {
    const { username, display_name, about_me, new_hat, add_user } = req.body
    let resp
    if (new_hat) {
        resp = await createHat({ username, display_name, about_me })
    } else {
        resp = await editHat({ display_name, about_me, username, add_user })
    }
    if (req.headers['x-client-api']) {
        return res.json({
            hat: resp.data.hat
        })
    }

    flashRedirect(req, res, {
        msg: 'Шляпа отредактирована',
        to: '/feed'
    })
}
