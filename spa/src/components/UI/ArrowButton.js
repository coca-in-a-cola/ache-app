import React from 'react';
import PropTypes from 'prop-types'
import { Link } from 'react-router-dom';

/**
 * Крупные кнопки интерфейса инфокиоска <br>
 * Их размер определяется в основном извне, с использованием родительских контейнеров и className
 */
 export const ArrowButton = ({left, color, link, onClick, className}) => {

    const ParentTagName = link ? Link : 'button'
    return (
    <ParentTagName
    className={
        " "
        + className
    }

    style={
        left ? {
            '-webkit-transform': 'rotateY(180deg)',
            transform: 'rotateY(180deg)'
        } : {}
    }

    to={link}
    onClick={link ? undefined : onClick}>
        <div className="text-center">
            <div className=" flex justify-center items-center p-4">
                <svg className="h-28 w-auto"xmlns="http://www.w3.org/2000/svg" fill={color ? color : "#fff"} enable-background="new 0 0 24 24" viewBox="0 0 24 24"><g><rect/></g><g><g><polygon points="15.5,5 11,5 16,12 11,19 15.5,19 20.5,12"/><polygon points="8.5,5 4,5 9,12 4,19 8.5,19 13.5,12"/></g></g></svg>
            </div>
        </div>
    </ParentTagName>
    );
}

ArrowButton.propTypes = {
    /** 
     * Смотрит ли срелка налево?
     */
    left: PropTypes.bool,

    /** 
     * Ссылка, по которой ведёт кнопка. <br/>
     * Если задана, кнопка оборачивается в ссылку и функция OnClick не срабатывает
     */
    link: PropTypes.string,

    /** 
     * Действие при нажатии кнопки
     */
    onClick: PropTypes.func,

    /** 
     * Добавочные css классы к кнопке <br/>
     * Желательно использовать классы Tailwind Css
     * @example className = "col-span-2 row-span-1" 
     * растянет кнопку внутри сетки (CSS) на 1 ряд и 2 колонки 
     * @example className = "bg-blue-lighter hover:bg-red"
     * сделает кнопку синей, а при наведении на неё мышкой - красной 
     */
    className: PropTypes.string,
    
    /**
     * Цвет кнопки
     */
    color: PropTypes.string,
}

ArrowButton.defaultProps = {
    color: "#0058a3"
}