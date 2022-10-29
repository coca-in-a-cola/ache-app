import React from 'react';
import PropTypes from 'prop-types'
import { Link } from 'react-router-dom';

/**
 * Крупные кнопки интерфейса инфокиоска <br>
 * Их размер определяется в основном извне, с использованием родительских контейнеров и className
 */
 export const FlatButton = ({icon, link, onClick, className, color, children, disabled}) => {

    const ParentTagName = link ? Link : 'button'
    return (
    <ParentTagName
    className={
        "relative transition-colors duration-200 rounded inline-flex box-border "
        + "justify-center items-center  text-white shadow-xl "
        + className
    }

    style={
        color && !disabled ? {
        backgroundColor: color
    } : null}

    disabled={disabled}

    to={link}
    onClick={link ? undefined : onClick}>
        <div className="text-center my-4">
            {
                icon ?
                <div className="w-28 h-28 p-1 mx-auto">
                        <img className="min-w-full" src={icon} alt="icon" />
                </div>
                : null
            }
            <h3 className="text-4xl font-black mx-4">
                {children}
            </h3>
        </div>
    </ParentTagName>
    );
}

FlatButton.propTypes = {
    /** 
     * Иконка кнопки, url
     */
    icon: PropTypes.string,

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

    /** 
     * Внутри компонента пишется текст кнопки
     */
    children: PropTypes.oneOfType([PropTypes.number, PropTypes.string])
}

FlatButton.defaultProps = {
    icon: undefined,
    children: 'Кнопка',
    color: "#0058a3"
}