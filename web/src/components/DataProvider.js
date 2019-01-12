import React, { Component } from "react";
import PropTypes from "prop-types";
class DataProvider extends Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired,
    render: PropTypes.func.isRequired
  };
  state = {
      data: [],
      allRoutes: [],
      loaded: false,
      placeholder: "Loading..."
    };
  componentDidMount() {
    fetch(this.props.endpoint)
      .then(response => {
        console.log(response)
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then(data => this.setState({ data: data, loaded: true }));
    fetch(this.props.endpoint+"all/")
      .then(response => {
        console.log(response)
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then(data => this.setState({ allRoutes: data, loaded: true }));
  }
  render() {
    const { allRoutes, data, loaded, placeholder } = this.state;
    const ready = allRoutes.length>0 && data.length>0;
    return loaded && ready ? this.props.render({allRoutes,data}) : <p>{placeholder}</p>;
  }
}
export default DataProvider;