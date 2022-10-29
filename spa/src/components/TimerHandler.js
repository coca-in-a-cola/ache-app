import React, {useEffect} from 'react';
import { useDispatch } from "react-redux"
import { refreshTimer } from '../features/timerSlice';

export const TimerHandler = ({children}) => {
    const dispatch = useDispatch()
    const RTF = () => {
        dispatch(refreshTimer())
    }

    useEffect(() => {
        document.body.addEventListener('click', RTF );

        return function cleanup() {
            window.removeEventListener('click', RTF );
        }
    },[]);


    return <div className='min-w-screen min-h-screen'>
        {children}
    </div>
}