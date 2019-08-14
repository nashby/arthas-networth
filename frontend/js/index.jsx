import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import AdminApp from "./AdminApp";
import AdminLogin from "./AdminLogin";
import { PrivateRoute } from "./PrivateRoute";

import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";

ReactDOM.render((
  <Router>
    <Switch>
      <Route exact path="/" component={App} />
      <Route path="/login" component={AdminLogin} />
      <PrivateRoute path="/admin" component={AdminApp} />
    </Switch>
  </Router>
), document.body);
