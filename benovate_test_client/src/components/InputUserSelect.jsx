import React from 'react'
import Select from 'react-select'
import PropTypes from 'prop-types';

const MAX_CONTRIBUTORS = 6;
const ASYNC_DELAY = 500;


export default class InputUserSelect extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: null};
    }
    getData() {
        return this.state.value;
    }
    onChange (value) {
        this.setState({
            value: value,
        });
    }
    getUsers (input, callback) {
        fetch(`//127.0.0.1:8000/balance/users/list/`)
            .then((response) => response.json())
            .then((json) => {
                    input = input.toLowerCase();
                    var options = json.filter(i => {
                        return i.inn.substr(0, input.length) === input;
                    });
                    var data = {
                        options: options.slice(0, MAX_CONTRIBUTORS),
                        complete: options.length <= MAX_CONTRIBUTORS,
                    };
                    setTimeout(function() {
                        callback(null, data);
                    }, ASYNC_DELAY);
            })
    }
    render () {
        return (
            <Select.Async multi={this.props.multi} value={this.state.value} onChange={this.onChange.bind(this)} valueKey="inn" labelKey="username" loadOptions={this.getUsers} />
        );
    }
}

InputUserSelect.propTypes = {
    multi: PropTypes.bool.isRequired,
};