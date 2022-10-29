import { API_URI, wrapFetch } from './shared';

export const get = (uuid) => {
    return wrapFetch(fetch(API_URI + "/api/forms/" + uuid))
}

export const send = (uuid, authToken, data) => {
    return wrapFetch(
        fetch(API_URI + "/api/forms/send/" + uuid, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({authToken: authToken, ...data})
      }))
}