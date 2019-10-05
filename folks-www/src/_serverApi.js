import axios from 'axios'

const client = axios.create({
    baseURL: 'http://localhost:8000/',
})

export function configureClient(token) {
    if (token) {
        client.defaults.headers = {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json'
        }
    } else {
        delete client.defaults.headers.Authorization
    }
    return client
}

export function login({username, password}) {
    return client.post('/v2/token', { username, password })
}

export function register({username, password, invite }) {
    return client.post('/v2/users', { username, password, invite})
}

export function me() {
    return client.get('/v2/me')
}

export function getFeed() {
    return client.get('/v2/feed')
}

export function createPost({ username, body }) {
    return client.post('/v2/feed', { username, body })
}

export function getHat({ username }) {
    return client.get('/v2/hats/' + username)
}

export function getMyHats() {
    return client.get('/v2/me/hats')
}

export function getInvites() {
    return client.get('/v2/me/invites')
}

export function genInvite() {
    return client.post('/v2/settings/gen_invites')
}

export function checkToken() {
    return client.get('/v2/token')
}

export function postImages(files) {
    form = new FormData()

    for (let f of files) {
        form.append('files', f)
        
    }

    return client.post('/v2/image', form, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
}

export function editHat(hat) {
    return client.post('/v2/hats/' + hat.username, hat)
}

export function createHat(hat) {
    return client.post('/v2/hats', hat)
}

export function flashRedirect(req, res, {msg, to}) {
    req.flash(msg)
    res.setHeader('Location', to)
    res.statusCode = 302
    res.end()
}


export function unexpected(req, res, e) {
    console.error(e)
    res.statusCode = 500
    res.json({
        error: 'Something went wrong'
    })
}

export function logout(req) {
    req.session.destroy((e) => {
        if (e) {
            console.error('Не получилось удалить сессию', e)
        } else {
            console.log('Сессия удалена')
        }
    })
}

export function _login({ token, user }, req) {
    req.session.token = token.token;
    req.session.user = user;
    return new Promise((resolve) => {
        req.session.save(function(e) {
            if (e) {
                console.error('Не смогли сохранить сессию', e);
                resolve()
            } else {
                console.log('Сохранили сессию')
                resolve()
            }
        });
    })
}