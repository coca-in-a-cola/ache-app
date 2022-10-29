import React from 'react';
import { useEffect, useState, useRef } from "react";
import PropTypes from 'prop-types'
import { selectTimer, setTimer, _unsetTimer } from '../../features/timerSlice';
import { useSelector, useDispatch } from "react-redux"

export const CloseButton = ({onClick, timeout}) => {
    const timer = useSelector(selectTimer)
    const dispatch = useDispatch()
    const button = useRef()

    useEffect(() => {
        // Запускаем наш таймер, если таковой не имеется
        if (timeout) {
            dispatch(setTimer(() => {button.current.click?.()}, timeout))
        }
    }, [timeout]);

    return (
        <button type="button"
        class="relative p-2 inline-flex items-center justify-center text-gray-400 hover:text-gray-500"
        ref={button}
        onClick={onClick}>
        <span class="sr-only">Close menu</span>
        <svg class="h-12 w-12" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>

        {
            timeout ?
            <div className="absolute -bottom-4">
                <span className="text-xl text-gray-400">
                {timer}
                </span>
            </div>
            : null
        }
        </button>
    );
}

CloseButton.propTypes = {
    /**
     *  Действие при закрытии окна
     *  @default (e) => {e.preventDefault()}
     */
     onClick: PropTypes.func,

    /**
     *  Время в секундах до осуществления действия
     */
    timeout: PropTypes.number,
}