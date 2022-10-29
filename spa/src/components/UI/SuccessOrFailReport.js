import React from 'react';
import PropTypes from 'prop-types'
import { Button } from './Button';

import { selectUserName, logout, hideModal } from "../../features/sessionSlice"
import { useSelector, useDispatch } from "react-redux"

const newlineText = (text) =>
    <>{text.split('\n').map(line => <>{line} <br/></>)}</>

export const SuccessOrFailReport = ({fail, large, label, text, }) => {
    const userName = useSelector(selectUserName)
    const dispatch = useDispatch();

    return ( <div
        className={ large
            ? "absolute top-0 left-0 right-0 bottom-0 flex justify-center items-center"
            : ""}>
    <div className="w-full">
    <div className={`flex items-center gap-4 my-4
    ${fail ? 'bg-red' : 'bg-blue-darker'} p-4 rounded-md w-full max-w-5xl mx-auto`}>
    <div className="w-max">
        <div className="h-24 w-28 flex text-white border-r-4 border-white">
            {
                fail 
                ? <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                : <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ffffff"><path d="M0 0h24v24H0z" fill="none"></path><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"></path></svg>
            }
        </div>
    </div>
    <div className="space-y-1 pl-2 text-left">
        <h6 className="font-black text-2xl text-white">{label}</h6>
        {
            text ?
            <p className="font-black text-xl text-gray-100">{newlineText(text)}</p>
            : null
        }
    </div>
    </div>

    {   
        large ?
        <div className="flex justify-between w-full max-w-5xl mx-auto">
            <Button className="w-96 bg-red" onClick={() => dispatch(logout())} timeout={30}>ВЫХОД</Button>
            <Button className="w-96 bg-blue-darker" onClick={() => dispatch(hideModal())}>
                ПРОДОЛЖИТЬ КАК {userName?.split(' ')?.[1].toUpperCase()}
            </Button>
        </div>
        : undefined
    }
    </div>
    </div>)
}

SuccessOrFailReport.propTypes = {
    /**
     * Выводим ли мы сообщение об ошибке?
     */
    fail: PropTypes.bool,

    /**
     * Выводим ли мы отчёт на весь экран с кнопками?
     */
    large: PropTypes.bool,

    /** 
     * Текст сообщения
     */
    label: PropTypes.string,

    /** 
     * Текст сообщения
     */
    text: PropTypes.string,
}

SuccessOrFailReport.defaultProps = {
    fail: false,
    large: false,
}