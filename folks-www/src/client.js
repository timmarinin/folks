import * as sapper from '@sapper/app'
import * as stores from './stores.js'
import { configureClientApi } from './_clientApi.js'

if (typeof __SAPPER__ !== 'undefined' && __SAPPER__ && __SAPPER__.session && __SAPPER__.session.token) {
	configureClientApi(__SAPPER__.session.token)
}

window.stores = stores;

sapper.start({
	target: document.querySelector('#sapper')
})