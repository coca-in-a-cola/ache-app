import { Button } from "./UI/Button"
import { selectUserName, logout, startLogin } from "../features/sessionSlice"
import { useSelector, useDispatch } from "react-redux"

/* 
    Информация о пользователе
*/
export const UserInfo = ({short, navigate}) => {

    const userName = useSelector(selectUserName)
    const dispatch = useDispatch();

    if (!userName)
        return <Button onClick={() => dispatch(startLogin())}>
        ВОЙТИ КАК СОТРУДНИК
        </Button>
    
    return <StaticUserInfo userName={userName} onClick={() => {dispatch(logout()); navigate?.("/")}} short={short}/>
}

export const StaticUserInfo = ({userName, onClick = () => {}, short}) => {

    if (!userName)
        return <></>
    
    return (
    <div className="max-w-lg flex flex-col space-y-4 justify-center items-center">
        <div className="bg-transparent w-auto flex items-center p-2">
        <div className="flex items-center space-x-4 text-red">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
        </div>
        <div className="flex-grow p-3">
        <div className="font-semibold text-2xl text-blue-darker">
            {userName}
        </div>
        {/* <div class="text-sm text-gray-500">
            {(() => {
                if (user.roles.has(userRoles.EMPLOYEE))
                    return "Сотрудник"
                else
                    return "Вход в систему не выполнен"
            })()}
        </div> */}
        </div>
        {
            short ?
            ""
            :<Button timeout={60} onClick={onClick}>
                ВЫХОД
            </Button>

        }
        </div>
    </div>)
}
