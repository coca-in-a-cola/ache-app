import React from 'react';
import { useEffect, useState, useRef } from "react";
import PropTypes from 'prop-types'
import { selectTimer, selectIsActivated, setTimer, _unsetTimer, _setActivated } from '../../features/timerSlice';
import { useSelector, useDispatch } from "react-redux"

const sizes = {
    'small': {
        height: "h-12",
        width: "w-12",
        border: "border-2",
        padding: "px-4",
        text: 'text-md',
    },
    'medium': {
        height: "h-16",
        width: "w-16",
        border: "border-2",
        padding: "px-6",
        text: 'text-xl',
    }
}


export const Button = ({children, onClick, disabled, timeout, size, className}) => {
    
    const timer = useSelector(selectTimer)
    const dispatch = useDispatch()
    const button = useRef()
    const isActivated = useSelector(selectIsActivated)
    
    const setupTimeout = () => {
        dispatch(setTimer(() => {button.current.click?.()}, timeout))
    }
    
    if (isActivated && timeout) {
        setupTimeout()
    }

    useEffect(() => {
        // Запускаем наш таймер, если таковой не имеется
        if (timeout) {
            setupTimeout()
        }
    }, [timeout]);

    const currentSize = sizes[size]

    return (
    <button 
        disabled={disabled}
        className={`flex justify-items-stretch font-semibold shadow-md ${currentSize.height} ${currentSize.text} text-white ${className}  disabled:opacity-75`}
        onClick={onClick}
        ref={button}>
        <div className={`w-full h-full shrink flex items-center justify-self-center justify-center text-center ${currentSize.padding} `}>
            {children}
        </div>
        {
            timeout ?
            <div className={`justify-self-end flex-shrink-0 flex items-center ${currentSize.height} justify-center items-center font-black`}>
                <span className={`border-l-2 ${currentSize.width} border-white`}>
                {timer}
                </span>
            </div>
            : null
        }
    </button>
    )
}

Button.propTypes = {
    /**
     *  Действие при нажатии кнопки либо по истечении времени
     */
    onClick: PropTypes.func,

    /**
     *  Время в секундах до осуществления действия
     */
    timeout: PropTypes.number,

    /**
     * Размер кнопки. 
     */
    size: PropTypes.oneOf(['small', 'medium']),

    /**
     * Цвет кнопки (как в css)
     */
    color: PropTypes.string,

    /**
     * Активна ли кнопка?
     */
    disabled: PropTypes.bool,

    /** 
     * Добавочные css классы к кнопке <br/>
     * Желательно использовать классы Tailwind Css
     * @example className = "col-span-2 row-span-1" 
     * растянет кнопку внутри сетки (CSS) на 1 ряд и 2 колонки 
     * @example className = "bg-blue-lighter hover:bg-red"
     * сделает кнопку синей, а при наведении на неё мышкой - красной 
     */
    className: PropTypes.string,
}

Button.defaultProps = {
    timeout: undefined,
    size: 'medium',
    className: "bg-red"
}
