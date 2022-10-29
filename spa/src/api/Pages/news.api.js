import { API_URI, wrapFetch } from '../shared';

export const get = (entity) => {
    return wrapFetch(fetch(API_URI + entity))
}
