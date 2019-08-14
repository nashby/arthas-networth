import React from "react";

import { donationsService } from './services/donations';

export default class Donation extends React.Component {
  constructor(props) {
    super(props);

    this.state = {approved: false};

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    const data = new FormData(event.target);

    donationsService.update(data)
      .then(
        donation => {
          this.setState({approved: true})
        }
      )
  }

  handleDelete(event) {
    event.preventDefault();

    const data = new FormData(event.target);

    donationsService.destroy(data)
      .then(
        donation => {
          this.setState({approved: true})
        }
      )
  }

  render() {
    if (!this.state.approved) {
      return(
        <div>
          <div>{this.props.donation.raw_donation} <a href={`https://www.youtube.com/watch?v=${this.props.donation.vod_youtube_id}&t=${this.props.donation.donated_at}`} target="_blank">link</a></div>

          <img src={`data:image/webp;base64,${this.props.donation.donation_image}`}></img>

          <form onSubmit={this.handleSubmit}>
            <input type="hidden" name="id" defaultValue={this.props.donation.id}></input>
            <label name="author">Author</label>
            <input name="author" defaultValue={this.props.donation.author}></input>
            <label name="amount">Amount</label>
            <input name="amount" defaultValue={this.props.donation.amount}></input>
            <label name="currency">Currency</label>
            <input name="currency" defaultValue={this.props.donation.currency}></input>
            <button type="submit">Save</button>
          </form>

          <form onSubmit={this.handleDelete}>
            <input type="hidden" name="id" value={this.props.donation.id}></input>
            <button type="submit">Delete</button>
          </form>
        </div>
      )
    } else {
      return null;
    }
  }
}
