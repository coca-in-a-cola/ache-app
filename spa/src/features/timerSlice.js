import { createSlice, createSelector, createDraftSafeSelector } from "@reduxjs/toolkit";

const initialState = {
    timer: undefined,
    timeout: undefined,
    isActivated: false
    /*
    TODO: хранить данные о последней сущности, которая вызвала таймаут,
    либо о последней функции, которую нужно использовать
    */
}

let timeout = undefined
let callbackFunction = undefined
export const timerSlice = createSlice({
    name: 'timer',
    initialState,
    reducers: {
        _setTimer: (state, {payload}) => {
            state.timer = payload
            state.timeout = payload
            state.isActivated = false
            // Нужно удалять старый таймаут при создании нового
            clearTimeout(timeout)
        },

        refreshTimer: (state, action) => {
            state.timer = state.timeout
        },

        _unsetTimer: (state, action) => {
            Object.assign(state, initialState)
            callbackFunction = undefined
        },

        _tickTimer: (state, action) => {
            state.timer -= 1
        },

        _setActivated: (state, action) => {
            state.isActivated = action.payload
        }
    }
})

export const { _setTimer, _unsetTimer, _tickTimer, _setActivated, refreshTimer } = timerSlice.actions

const selectSelf = (state) => state.timer
export const selectTimer = createDraftSafeSelector(selectSelf, (state) => {return state.timer})
export const selectIsActivated = createDraftSafeSelector(selectSelf, (state) => {return state.isActivated})

export const setTimer = (callbackFn, timer) => (dispatch, getState) => {
    callbackFunction = callbackFn
    dispatch(_setTimer(timer))
    dispatch(timerTick())
}

const timerTick = () => (dispatch, getState) => {
    const timer = selectTimer(getState())

    if (timer > 0) {
        dispatch(_tickTimer())

        // Вот это говнокод
        timeout = setTimeout(() => dispatch(timerTick()), 1000)
    }
    else if (timer === 0) {
        callbackFunction?.()
        dispatch(_unsetTimer())
        setTimeout(() => dispatch(_setActivated(true)), 2000)
    }
}

export default timerSlice.reducer