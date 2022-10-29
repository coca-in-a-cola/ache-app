import React from 'react';
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack';

import { Button } from '../UI/Button';

import { Spinner } from '../UI/Spinner';
import { SuccessOrFailReport } from "../UI/SuccessOrFailReport"
import { Modal } from "../Modals/Modal"
import { get } from '../../api/Pages/papers.api';
import { API_URI } from '../../api/shared';

//import '../../assets/css/scrollbar.css'

const gutter = 48;
export class Papers extends React.Component {

    constructor(props) {
        super(props)
        this.state = {numPages: 1, pageNumber: 1, 
        window: {width: window.innerWidth, height: window.innerHeight},
        loading: true}

        this.previousEntry = this.previousEntry.bind(this)
        this.nextEntry = this.nextEntry.bind(this)
        this.changeEntry = this.changeEntry.bind(this)
        this.previousPage = this.previousPage.bind(this)
        this.nextPage = this.nextPage.bind(this)
        this.changePage = this.changePage.bind(this)
    }

    componentDidMount() {
        get().then(result => {
            let papersList = result.map(item => {
                return {
                    url: API_URI + (item.url?.[0] == '/' ? "" : '/') + item.url,
                    title: item.title,
                }
            })
            this.setState({list: papersList, current: 0, loading: false})
        })
        .catch(error => {
            this.setState({loading: false, error: error})
        })
    }

    previousEntry() {
        this.changeEntry.call(this, 1);
    }

    nextEntry() {
        this.changeEntry.call(this, -1);
    }

    changeEntry(offset) {
        this.setState({pageNumber: 1, current: this.state.current + offset})
    }


    onDocumentLoadSuccess({ numPages }) {
        this.setState({numPages: numPages, pageNumber: 1});
    }

    changePage(offset) {
        this.setState({pageNumber: this.state.pageNumber + offset})
    }

    previousPage() {
        this.changePage.call(this, -1);
    }

    nextPage() {
        this.changePage.call(this, 1);
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
        :

        <div className="bg-gray-900 pb-24 pt-24 relative">
            <Document
                file={this.state.list[this.state.current].url}
                renderMode={'svg'}
                onLoadSuccess={this.onDocumentLoadSuccess.bind(this)}
            >
                <Page 
                width={this.state.window.width - gutter*2}
                className={'flex justify-center select-none'}
                pageNumber={this.state.pageNumber} />
            </Document>
            <div className="fixed top-0 left-0 right-0 flex items-center h-24 bg-gray-900">
                <div className="text-white px-8 gap-8 flex justify-center items-center w-full relative">
                    <div className={`justify-start items-center absolute left-10`}>
                        <Button
                            onClick={(e) => {
                                e.preventDefault();
                                this.props.navigate(-1)
                            }}
                            direction="none"
                            className="justify-start bg-red hover:bg-blue-lighter"
                        >
                            Выход
                        </Button>
                    </div>
                    
                    <Button
                        disabled={this.state.current === this.state.list.length - 1}
                        onClick={(e) => {
                            e.preventDefault();
                            this.previousEntry.call(this)
                        }}
                        direction="left"
                    >
                    Предыдущий выпуск
                    </Button>

                    <p className="text-3xl font-black">
                        {this.state.list[this.state.current].title}
                    </p>

                    <Button
                        disabled={this.state.current === 0}
                        onClick={(e) => {
                            e.preventDefault();
                            this.nextEntry.call(this)
                        }}
                        direction="right"
                    >
                    Следующий выпуск
                    </Button>

                </div>
            </div>

            <div className="fixed bottom-0 left-0 right-0 flex items-center h-24 bg-gray-900">
                <div className="text-white px-8 gap-8 w-full flex justify-center items-center">

                    <Button
                        disabled={this.state.pageNumber <= 1}
                        onClick={(e) => {
                            e.preventDefault();
                            this.previousPage.call(this)
                        }}
                        direction="left"
                    >
                        Назад
                    </Button>

                    <p className="text-3xl">
                    Страница {this.state.pageNumber || (this.state.numPages ? 1 : '--')} из {this.state.numPages || '--'}
                    </p>

                    <Button
                        disabled={this.state.pageNumber >= this.state.numPages}
                        onClick={(e) => {
                            e.preventDefault();
                            this.nextPage.call(this)
                        }}
                        direction="right"
                    >
                    Вперёд
                    </Button>
                </div>
            </div>
        </div>
        )
    }
}