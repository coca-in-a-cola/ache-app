import React from 'react';
import PropTypes from 'prop-types'
import { CloseButton } from '../UI/CloseButton';


export class ReadCard extends React.Component {
    static propTypes = {
        /**
         *  Действие при прочтении ввода
         *  @default (e) => {e.preventDefault()}
         */
        onSubmit: PropTypes.func,

        /**
         *  Действие при отмене ввода пользователем
         *  @default (e) => {e.preventDefault()}
         */
        onCancel: PropTypes.func,
    }

    constructor(props) {
        super(props);
        this.state = {card: '', loading: false}
        this.onInput = this.onInput.bind(this)
    }

    onInput = (event) => {
        //event.preventDefault();
        let number = event.target.value;

        if (this.countdown)
            clearTimeout(this.countdown)
        this.countdown = setTimeout(() => {this.props.onSubmit(number); this.setState({loading: false})}, 1500);
        
        if (!this.state.loading)
        {
            this.setState({loading: true})
        }
    }

    componentDidMount() {

    }
    
    render() {
        return (
            <div className="absolute top-0 left-0 right-0 bottom-0 flex items-center justify-center">
            <form className="max-w-lg pt-4 pb-8 px-8 bg-gray-800 shadow-xl rounded-lg text-center relative">
                <div className="mt-4 w-20 h-20 mx-auto relative items-center justify-center flex">
                {
                    this.state.loading
                    ?
                    <svg className="animate-spin h-14 w-14 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    :
                    <>
                    <span className="absolute left-4 top-4 flex h-12 w-12">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
                    </span>
                    <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 20 20" viewBox="0 0 20 20" fill="#FFFFFF"><rect fill="none" height="20" width="20"/><path d="M5.41,14.59l-1.06,1.06C2.9,14.21,2,12.21,2,10c0-2.21,0.9-4.21,2.34-5.66l1.06,1.06C4.23,6.58,3.5,8.21,3.5,10 S4.23,13.42,5.41,14.59z M16.5,10c0,1.79-0.73,3.42-1.91,4.59l1.06,1.06C17.1,14.21,18,12.21,18,10c0-2.21-0.9-4.21-2.34-5.66 l-1.06,1.06C15.77,6.58,16.5,8.21,16.5,10z M13.5,10c0,0.96-0.39,1.84-1.03,2.47l1.06,1.06C14.44,12.63,15,11.38,15,10 c0-1.38-0.56-2.63-1.46-3.54l-1.06,1.06C13.11,8.16,13.5,9.04,13.5,10z M6.5,10c0-0.96,0.39-1.84,1.03-2.47L6.46,6.46 C5.56,7.37,5,8.62,5,10c0,1.38,0.56,2.63,1.46,3.54l1.06-1.06C6.89,11.84,6.5,10.96,6.5,10z M10,8.25c-0.97,0-1.75,0.78-1.75,1.75 s0.78,1.75,1.75,1.75s1.75-0.78,1.75-1.75S10.97,8.25,10,8.25z"/></svg>
                    </>
                }
                </div>    

                <div>
                    <h2 class="text-white text-4xl font-semibold">
                        Приложите пропуск сотрудника
                    </h2>
                </div>
                
                <input 
                className="absolute opacity-0 top-0 left-0 block w-screen h-full max-w-lg"
                name="card"
                onChange={this.onInput}
                autoFocus>
                </input>
                
                <div className='absolute top-2 right-2'>
                    <CloseButton onClick={this.props.onCancel} timeout={90}></CloseButton>
                </div>
            </form>
            </div>
        );
    }
}