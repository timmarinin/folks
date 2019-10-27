import sirv from 'sirv'
import express from 'express'
import compression from 'compression'
import * as sapper from '@sapper/server'
import session from 'express-session'
import ConnectRedis from 'connect-redis'
import bodyParser from 'body-parser'
import {configureClient, checkToken, me } from './_serverApi.js'
import multer from 'multer'
const m = multer({ storage: multer.memoryStorage() })
const RedisStore = ConnectRedis(session)
import faye from 'faye'
import fayeRedis from 'faye-redis'

const { PORT, NODE_ENV, REDIS_URL } = process.env
const dev = NODE_ENV === 'development'


let bayeux = new faye.NodeAdapter({
	mount: '/faye',
	timeout: 45,
	engine: {
		type: fayeRedis,
		host: 'localhost',
		port: 6379
	}
});

const app = express()

app.use(session({
	store: new RedisStore({
		url: REDIS_URL
	}),
	cookie: {
		secure: true,
		maxAge: 1000 * 86400 * 14,
		path: '/',
		httpOnly: true,
	},
	secret: process.env.COOKIE_SECRET,
	resave: true,
	saveUninitialized: false
}))
app.use(function (req, res, next) {
	req.flash = function (msg) {
		if (req.session && req.session.flashes) {
			req.session.flashes.push(msg)
		} else {
			req.session.flashes = [msg]
		}
	}
	req.getFlash = function () {
		const f = req.session && req.session.flashes || []
		req.session.flashes = []
		return f
	}
	next()
})

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
app.use(compression({ threshold: 0 }))
app.use(sirv('static', { dev }))
app.use('/server-side-api', function(req, res, next) {
	if (req.body.token='HELLO') {
		bayeux.getClient().publish('/reader_feed/' + req.body.reader_feed, {
			post: req.body.post
		})
		res.json({ok: true})
	} else {
		next()
	}
})
app.use(async function (req, res, next) {
	let token = null;
	if (req.path.startsWith('/client/') || req.path === '/service-worker.js') {
		return next()
	}
	try {
		token = req.session.token
		if (token) {
			req.apiClient = configureClient(token)
			await checkToken().catch(e => {
				delete req.session.token
				delete req.session.user
				req.session.save()
			})

			if (! req.session.user.reader_feed) {
				console.log('Перезапрашиваем пользователя, потому что нет reader_feed ', req.session.user)
				const resp = await me()
				req.session.user = resp.data.user
			}
		} else {
			req.apiClient = configureClient(null)
			delete req.session.token
			delete req.session.user
		}
	} catch (e) {
		req.session.token = null;
		req.session.user = null;
	}
	next()
})
app.use('/feed', m.any())
app.use(sapper.middleware({
	session: (req, res) => {
		const sess = {
			user: req.session && req.session.user || undefined,
			token: req.session && req.session.token || undefined,
			flash: req.getFlash()
		}
		return sess
	}
}))



const server = app.listen(PORT, err => {
	if (err) console.log('Не смогли подключиться к серверу', err);
});


bayeux.attach(server);
