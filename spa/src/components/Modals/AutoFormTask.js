import { FormTask } from "./FormTask"
import { get, send } from "../../api/forms.api"
import { 
    sumbitConfirmNumber, submitCardCode,
    selectUserName, selectUserPhoneNumber, Stage,
    selectStage, selectShowModal, selectLoading, selectError, selectPreviousCardCode, logout, setLoading }
    from "../../features/sessionSlice"
import { useSelector, useDispatch } from "react-redux"

export const AutoFormTask = ({uuid}) => {
    const loading = useSelector(selectLoading)
    const dispatch = useDispatch();

    
}