import React from 'react';

export const Modal = ({children, center}) => {
    return (
    <div className="fixed top-0 left-0 right-0 bottom-0 select-none bg-black bg-opacity-75">
        {
            center ?
            <div class="grid min-h-screen win-w-screen place-content-center">
                {children}
            </div>
            : children
        }
    </div>
    );
}
