import React from "react";

import { donationsService } from './services/donations';
import Donation from "./Donation";

export default class AdminApp extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    donationsService.getAll(this.props.location.search).then(data => {
      this.setState({data: data.json})
    });
  }

  render() {
    return (
      <div>{
        this.state && this.state.data.map((donation) =>
          <Donation key={donation.id} donation={donation}/>
        )
      }</div>
    );
  }
}
