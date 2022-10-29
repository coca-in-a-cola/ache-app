import React from 'react';
import Lightbox from "react-awesome-lightbox";
import { Spinner } from '../UI/Spinner';
import { SuccessOrFailReport } from "../UI/SuccessOrFailReport"
import { Modal } from "../Modals/Modal"
import { get } from '../../api/Pages/news.api';
import { API_URI } from '../../api/shared';
import PropTypes from 'prop-types'
import "react-awesome-lightbox/build/style.css";
import "../../assets/css/lightbox-custom.css"

export class News extends React.Component {
    static propTypes = {

        /**
         *  Бекенд сушности, которую показываем
         */
        entity: PropTypes.string,
    }

    static defaultProps = {
        entity: "/api/news"
    }

    constructor(props) {
        super(props);
        this.state = {imageList: [], loading: true}
    }

    componentDidMount() {
        get(this.props.entity).then(result => {
            let imageList = result.map(item => {
                return {
                    url: API_URI + (item.url?.[0] == '/' ? "" : '/') + item.url,
                    title: item.title,
                }
            })

            this.setState({ imageList: imageList, loading: false });    
        })
        .catch(errMess => {
            this.setState({ error: errMess, loading: false})
        })
    }

    render() {
        return this.state.loading
            ? <Modal center>
                <Spinner></Spinner>
            </Modal>
            : this.state.error
            ? <Modal center>
                <SuccessOrFailReport fail label={this.state.error} />
            </Modal>
            : (
                this.state.imageList.length == 1
                ? <Lightbox image={this.state.imageList[0].url} title={this.state.imageList[0].title}
                allowRotate={false} doubleClickZoom={2}
                onClose={() => {this.props.navigate(-1)}}/>
                : <Lightbox images={this.state.imageList} allowRotate={false} doubleClickZoom={2}
                onClose={() => {this.props.navigate(-1)}}/>
            );
    }
}