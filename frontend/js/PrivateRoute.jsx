import React from "react";
import { Route, Redirect } from "react-router-dom";

import { authenticationService } from './services/authentication';

export const PrivateRoute = ({ component: Component, ...rest }) => (
  <Route {...rest} render={props => (
      authenticationService.isAuthenticated()
          ? <Component {...props} />
          : <Redirect to={{ pathname: '/login', state: { from: props.location } }} />
  )} />
)
