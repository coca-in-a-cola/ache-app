import { API_URI, wrapFetch } from './shared';

export const get = (path) => {
    return wrapFetch(fetch(API_URI + "/api/menus" + path))
}
