//import { Session } from '../user/Session';
//import { status } from '../constants/dummyConstants';
import { API_URI, wrapFetch } from './shared';

export const refreshSession = (session) => {
    return new Promise(function(resolve, reject) {
        
    });
}


export const sendCardCode = (cardCode) => {
    return wrapFetch(
        fetch(API_URI + "/api/session", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ssid: cardCode})
      }))
}

export const sendConfirmNumber = (authToken, confirmNumber) => {
    return wrapFetch(
        fetch(API_URI + "/api/session/confirmNumber", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({authToken: authToken, confirmNumber: confirmNumber})
      }))
}

export const requestService = (authToken, uuid, data = {}) => {
    // uuid - id запрашиваемой услуги
    return new Promise(function(resolve, reject) {
        fetch(`/api/forms/send/${uuid}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({authToken: authToken, ...data})
          })
        .then((response) => {
            if (response.ok) {
                //resolve(status.SUCCESS)
            }
            else {
                //reject(status.FAIL)
            }
        })
    });
}