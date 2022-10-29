import { createSlice } from "@reduxjs/toolkit";
import { sendCardCode, sendConfirmNumber } from "../api/session.api";
import { get as getFormData, send as sendFormData } from "../api/forms.api"


export const Stage = {
    UNAUTHORIZED: 0,
    READ_CARD: 1,
    CONFIRM_NUMBER: 2,
    SUCCESS: 3,
}

const initialState = {
    session: {},
    loading: false,
    error: null,
    stage: Stage.UNAUTHORIZED,
    showModal: false,
    formData: null,
    success: null,
    reportLarge: false,
}

export const sessionSlice = createSlice({
    name: 'session',
    initialState,
    reducers: {
        setLoading: (state, action) => {
            state.loading = action.payload
        },

        setError: (state, action) => {
            state.error = action.payload
            state.loading = false
        },

        showModal: (state) => {
            state.showModal = true
        },

        hideModal: (state) => {
            state.reportLarge = false
            state.success = null
            state.error = null
            state.showModal = false
        },

        startLogin: (state) => {
            state.showModal = true
            state.stage = Stage.READ_CARD
        },

        setCardCode: (state, action) => {
            state.session = action.payload
            state.stage = Stage.CONFIRM_NUMBER
            state.loading = false
            state.error = false
            state.success = false
        },

        setConfirmNumber: (state, action) => {
            state.session = action.payload
            state.stage = Stage.SUCCESS
            state.loading = false
            state.error = false
            state.success = false
        },

        setFormData: (state, action) => {
            state.formData = action.payload
            state.showModal = true
            state.loading = false
            state.error = false
            state.success = false
            state.reportLarge = true
        },

        setSuccess: (state, action) => {
            state.success = action.payload
            state.loading = false
        },

        setReportLarge: (state, action) => {
            state.reportLarge = action.payload
        },

        logout: (state) => {
        // Redux Toolkit allows us to write "mutating" logic in reducers. It
        // doesn't actually mutate the state because it uses the immer library,
        // which detects changes to a "draft state" and produces a brand new
        // immutable state based off those changes
            Object.assign(state, initialState)
        }
    },
    
    /**extraReducers: (builder) => {
        builder.addCase(inputCardCode.pending, (state) => {
            state.loading = true;
        })
        builder.addCase(inputCardCode.rejected, (state, action) => {
            state.error = action.payload;
            state.loading = false;
        })
        builder.addCase(inputCardCode.fulfilled, (state, action) => {
            // Add user to the state array
            Object.assign(state.session, action.payload)
            state.loginStage = Stage.CONFIRM_NUMBER
            state.loading = false;
        })
    },*/
})

export const { logout, setLoading, setError, showModal, hideModal,
    startLogin, setCardCode, setConfirmNumber, setFormData, setReportLarge,
    setSuccess } = sessionSlice.actions


// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched
export const submitCardCode = (ssid) => (dispatch) => {
    dispatch(setLoading(true))
    
    sendCardCode(ssid).then(result => {
        dispatch(setCardCode({ssid: ssid, ...result}))
    })
    .catch(error => {
        dispatch(setError(error))
    })
}

export const sumbitConfirmNumber = (confirmNumber) => (dispatch, getState) => {
    dispatch(setLoading(true))
    const authToken = selectAuthToken(getState())

    sendConfirmNumber(authToken, confirmNumber).then(result => {
        dispatch(setConfirmNumber(result))
    })
    .catch(error => {
        dispatch(setError(error))
        dispatch(showModal())
    })
}

export const submitFormData = (data) => (dispatch, getState) => {
    
    dispatch(setLoading(true))
    const authToken = selectAuthToken(getState())
    const uuid = selectPreviousFormUuid(getState())

    sendFormData(uuid, authToken, data).then(result => {
        dispatch(setReportLarge(true))
        dispatch(setSuccess(result))
    })
    .catch(error => {
        dispatch(setReportLarge(true))
        dispatch(setError(error))
    })
}

export const fetchFormData = (uuid) => (dispatch, getState) => {
    dispatch(setLoading(true))

    getFormData(uuid).then(result => {
        dispatch(setFormData(result))
    })
    .catch(error => {
        dispatch(setError(error))
    })
}


export const selectUserName = (state) => state.session.session?.fullname
export const selectUserPhoneNumber = (state) => state.session.session?.phoneNumber
export const selectAuthToken = (state) => state.session.session?.authToken;
export const selectStage = (state) => state.session.stage
export const selectLoading = (state) => state.session.loading
export const selectError = (state) => state.session.error
export const selectShowModal = (state) => state.session.showModal
export const selectPreviousCardCode = (state) => state.session.session?.ssid

export const selectFormData = (state) => state.session.formData
export const selectPreviousFormUuid = (state) => state.session.formData?.uuid
export const selectSuccess = (state) => state.session.success
export const selectReportLarge = (state) => state.session.reportLarge

export default sessionSlice.reducer