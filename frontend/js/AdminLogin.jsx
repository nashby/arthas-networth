import React from "react";

import { authenticationService } from './services/authentication';

export default class AdminLogin extends React.Component {
  constructor(props) {
    super(props);

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    const data = new FormData(event.target);

    authenticationService.login(data.get('username'), data.get('password'))
      .then(
        user => {
          const { from } = this.props.location.state || { from: { pathname: "/" } };
          this.props.history.push(from);
        }
      )
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label name="username">Username:</label>
        <input name="username"></input>

        <label name="username">Password:</label>
        <input name="password"></input>

        <button type="submit">Login</button>
      </form>
    );
  }
}
