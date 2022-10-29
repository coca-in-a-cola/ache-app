import { Header } from '../Header';
import background from '../../assets/img/background.jpg'
import { FlatMenu } from '../FlatMenu';
import { Modals } from '../Modals/Modals';
import { TimerHandler } from '../TimerHandler';
export const Main = ({location, navigate, form_uuid}) => {
    return (
        <TimerHandler>
        <div className="fixed top-0 left-0 right-0 bottom-0 select-none -z-10">
            <img src={background} 
                className="select-none -z-10 absolute top-0 left-0 h-screen w-screen"
                alt="Фоновая картинка"/>
        </div>

        <div className="select-none">
            <Header navigate={navigate} />
        </div>

        <div className="relative">
        {
            <div 
            className={`absolute top-12 left-0 right-0 translate-y-0 transition-all duration-200 transform-gpu
            ${location == "" || location == "/" ? "translate-y-1/2" : " "}`}>
                <FlatMenu path={location} navigate={navigate} />
            </div>
        }
        </div>
        <Modals form_uuid={form_uuid} location={location} navigate={navigate} />
        </TimerHandler>
    )
}
