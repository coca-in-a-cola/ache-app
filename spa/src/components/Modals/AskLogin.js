import { UserInfo } from "../UserInfo"
import {Button} from '../UI/Button'
import PropTypes from 'prop-types'
import { CloseButton } from "../UI/CloseButton"

export const AskLogin = ({text, onCancel, timeout = 60}) => {
    return (
        <div className="absolute left-0 right-0 top-0 bottom-0 flex items-center justify-center">
            <div class="max-w-lg pt-4 pb-8 mb-8 px-8 bg-gray-800 z-index-10 shadow-xl rounded-lg text-center relative mx-auto z-10">
                <div class="mt-4 w-20 h-20 mx-auto relative items-center justify-center flex">
                    <span class="absolute left-4 top-4 flex h-12 w-12">
                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
                    </span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M0 0h24v24H0z" fill="none"/><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
                </div>    

                <div>
                    <h2 class="text-white text-2xl font-black">
                    {text}
                    </h2>
                </div>
                <div className="flex justify-center w-full max-w-5xl mx-auto mt-8">
                <UserInfo/>
                </div>
                <div className='absolute top-2 right-2'>
                    <CloseButton onClick={onCancel}></CloseButton>
                </div>
            </div>
            
        </div>
    )
}