import { API_URI, wrapFetch } from '../shared';

export const get = () => {
    return wrapFetch(fetch(API_URI + "/api/papers"))
}