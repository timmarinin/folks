import { createPost, postImages, flashRedirect } from '../../_serverApi.js'

export async function post(req, res) {
    let attachments = []
    const { username, body } = req.body
    if (req.files) {
        attachments = postImages(req.files)
    }

    const resp = await createPost({ username, body })
    if (req.headers['x-client-api']) {
        return res.json({
            post: resp.data.post
        })
    }

    flashRedirect(req, res, {
        msg: 'Пост опубликован',
        to: '/feed'
    })
}