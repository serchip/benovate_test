import React from 'react'
import {ModalContainer, ModalDialog} from 'react-modal-dialog'
import NumericInput from 'react-numeric-input'
import cookie from 'react-cookies'
require('es6-promise').polyfill()
import fetch from 'isomorphic-fetch'

import InputUserSelect from './InputUserSelect.jsx'

class BalanceApp extends React.Component {
    constructor(props) {
        super(props);
        this.state = {users: [],
            _inputDecSum: 0.00,
            isShowingModal: false,
        };
    }
    handleModalOpen() { this.setState({isShowingModal: true})}
    handleModalClose() {this.setState({isShowingModal: false})}

    componentDidUpdate() {
        this._updateLocalStorage();
    }
    handleChangeDecSum(n) {
        this.setState({_inputDecSum: n});
    }
    getResponce(data) {
        return fetch('//127.0.0.1:8000/balance/post/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': cookie.load('csrftoken'),
                },
                body: JSON.stringify(data)
            })
            .then((response) => {
                return response.json();
            })
            .catch((error) => {
                console.warn(error);
            })

    }

    handleSubmit(event) {
        this.clearForm();
        let user_from = this._inputUserFrom.getData() ? this._inputUserFrom.getData().id : null
        let users_to = this._inputUserTo.getData() ? this._inputUserTo.getData().map((item) => item.inn) : null
        var data = Object.assign(
            {},
            {user_from: user_from},
            {users_to: users_to},
            {dec_sum: this.state._inputDecSum}
        );
        this.getResponce(data).then((result) => {
            if (result.success){
                this.setState({
                    step: this.state._inputDecSum / 4,
                    intervalId: setInterval(this.timer.bind(this), 100)
                });
            }
            else {
                let errors = result.errors
                Object.keys(errors).map((key) => {
                    this.toggleHasError(key, errors[key])
                })
            }
        })
        event.preventDefault();
    }
    timer() {
        let newCount = this.state._inputDecSum - this.state.step;
        if(newCount > 0) {
            this.setState({ _inputDecSum: newCount });
        } else {
            this.setState({ _inputDecSum: 0 });
            clearInterval(this.state.intervalId);
            this.handleModalOpen();
        }
    }
    toggleHasError(refName, mess) {
        if (!this.refs[refName].classList.contains('has-error')){
            this.refs[refName].classList.add('has-error')
        }
        if (mess) {this.refs[refName + '_help'].innerHTML = mess }
        else {this.refs[refName + '_help'].innerHTML = ''}
    }
    clearForm(){
        let CLEARDATA = [{'non_field_errors': ''},
            {'user_from': 'Поиск пользователя по ИНН'},
            {'users_to': 'Поиск пользователей по ИНН'},
            {'dec_sum': ''}
        ]
        CLEARDATA.map((todo) => {
            Object.keys(todo).map((key) => {
                this.refs[key].classList.remove('has-error')
                this.refs[key + '_help'].innerHTML =  todo[key]
            })
        })
    }
    render() {
        return (
            <div className="balance-app">
                <h2 className="app-header">BalanceApp</h2>
                <div className="container">
                    <div className="col-md-4">
                        <form onSubmit={this.handleSubmit.bind(this)} ref="non_field_errors">
                            <h3 className="help-block" ref="non_field_errors_help"></h3>
                            <div ref="user_from" className="form-group">
                                <label htmlFor="lableInputFrom">От кого перевод</label>
                                <InputUserSelect multi={false}
                                               className="form-control"
                                               ref={(ref) => this._inputUserFrom = ref}
                                />
                                <span className="help-block" ref="user_from_help">Поиск пользователя по ИНН</span>
                            </div>
                            <div ref="users_to" className="form-group">
                                <label htmlFor="lableInputTo">Кому перевод</label>
                                <InputUserSelect multi={true}
                                                 className="form-control"
                                                 ref={(ref) => this._inputUserTo = ref}
                                />
                                <span className="help-block" ref="users_to_help">Поиск пользователей по ИНН</span>
                            </div>
                            <div ref="dec_sum" className="form-group">
                                <label htmlFor="lableInputSum">Сумма перевода</label>
                                <NumericInput step={1.0} precision={2} className="form-control"
                                              value = {this.state._inputDecSum}
                                              onChange={this.handleChangeDecSum.bind(this)}
                                />
                                <span className="help-block" ref="dec_sum_help"></span>
                            </div>
                            <button type="submit" className="btn btn-primary">Отправить</button>
                        </form>
                    </div>
                </div>
                {
                    this.state.isShowingModal &&
                    <ModalContainer onClose={this.handleModalClose.bind(this)}>
                        <ModalDialog onClose={this.handleModalClose.bind(this)}>
                            <h3 className="text-success">Успешное сохранение.</h3>
                        </ModalDialog>
                    </ModalContainer>
                }
            </div>
        );
    }

    _updateLocalStorage() {
        var notes = JSON.stringify(this.state.users);
        localStorage.setItem('users', notes);
    }
}

export default BalanceApp;
