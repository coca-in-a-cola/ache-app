import React from 'react';
import { FlatButton } from './UI/FlatButton'
import { ArrowButton } from './UI/ArrowButton'
import PropTypes from 'prop-types';
import { get } from '../api/flatMenu.api';
import { Modal } from './Modals/Modal'
import { Spinner } from './UI/Spinner'
import { API_URI } from '../api/shared';
import { SuccessOrFailReport } from './UI/SuccessOrFailReport';

export class FlatMenu extends React.Component {

    constructor(props) {
        super(props);
        this.state = {loading: true}
    }

    componentDidUpdate(prevProps) {
        if (prevProps.path != this.props.path) {
            this.componentDidMount()
        }
    }

    componentDidMount() {
        get(this.props.path).then((result => {
            console.log(result)
            if (Object.keys(result).length > 0)
                this.setState(({loading: false, error: false, ...result}))
            else
                this.setState({loading: false, error: "Меню не найдено"})
        }))
        .catch((error => {
            this.setState({loading: false, error: error})
        }))
    }

    render() {
        return (
            this.state.loading
            ? <Modal center>
                <Spinner></Spinner>
            </Modal>
            : this.state.error
            ? <Modal center>
                <SuccessOrFailReport fail label={this.state.error} />
            </Modal>
            : <div className="flex flex-wrap-reverse shrink py-4 mx-auto w-full items-center justify-start max-w-screen-2xl">
            {
            this.state.buttons.map((button, index) => 
                <div className="basis-1/3 border-transparent border-8">
                    <FlatButton
                    color={this.state.color}
                    className={"w-full border-transparent border-8 h-48"}
                    icon={button.icon ? API_URI + (button.icon?.[0] == '/' ? "" : '/') + button.icon : undefined}
                    link={button.link}
                    onClick={button.link? undefined : button.onClick}
                    >
                        {button.text}
                    </FlatButton>
                </div>
            )
            }
            {

                this.state.goBack ?
                    <div className="absolute top-80 left-0">
                    <ArrowButton left color={this.state.color} onClick={() => this.props.navigate(-1)}/>
                    </div>
                : null
            }
            </div>
        )
    }
}