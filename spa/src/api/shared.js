export const API_URI = process.env.NODE_ENV !== 'production' ? "http://localhost:5000" : ""
export const API_TIMEOUT_MS = 30000;

export const wrapFetch = (fetch) => {
    return new Promise(function(resolve, reject) {
        const timeout = setTimeout(() => {
            reject('Превышено время ожидания ответа сервера')
        }, API_TIMEOUT_MS)
        
        fetch
        .then((response) => {
            clearTimeout(timeout)

            if (response) {
                const contentType = response.headers.get("content-type");
                if (contentType && contentType.indexOf("application/json") !== -1) {
                    response.json()
                    .then((result) => {
                        response.ok ? resolve(result) : reject(result)
                    })
                    .catch((errMes) => {
                        reject(errMes)
                    })    
                }
                else 
                    reject("Произошла ошибка целостности данных")
                
            }
            else {
                response.json().then((errMes) => {
                    reject(errMes)
                })
                .catch((error) => {
                    reject("Произошла ошибка http " + response.status + ": " + error);
                })
                
            }
        })
        .catch((error) => {
            clearTimeout(timeout)
            reject("Произошла ошибка сети " + error);
        })
    });
}
