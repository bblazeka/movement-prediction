import React, { Component } from 'react';
import mapboxgl from 'mapbox-gl';
import { connect } from 'react-redux';
import Button from '@material-ui/core/Button';
import Switch from '@material-ui/core/Switch';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import NavigationIcon from '@material-ui/icons/Navigation';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';

import * as appActions from '../actions/appActions';
import './Map.css';
import * as utils from './MapUtils';

mapboxgl.accessToken = utils.token;

class MapInterface extends Component {
  map;

  constructor(props) {
    super(props);
    this.state = {
      dataset: 'zg',
      method: 'compare',
      maroon: {
        title: '',
        visible: false,
      },
      blue: {
        title: '',
        visible: false,
      },
      black: {
        title: '',
        visible: false,
      },
      red: {
        title: '',
        visible: false,
      },
      orange: {
        title: '',
        visible: false,
      },
    }
  }

  static defaultProps = {
    center: { lat: 45.8, lng: 15.97 },
    zoom: 13
  }

  request(that, path) {
    if (that.map) {
      that.map.getSource('green').setData({
        "type": "FeatureCollection",
        "features": path.map(function (v) {
          return {
            "type": "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": [v[0], v[1]]
            }
          };
        })
      })
    }
    that.props.getPrediction(this.state.method, this.state.dataset, JSON.stringify(path).replace(/['"]+/g, ''))
  }

  componentDidMount() {
    this.loadMap();
  }

  recentre() {
    let center = utils.cities.filter(x => x.value === this.state.dataset)[0].center;
    this.map.jumpTo({'center': center, 'zoom': 12});
  }

  generate() {
    let i = 0;
    let that = this;
    let path = utils.cities.filter(x => x.value === this.state.dataset)[0].input[0];
    let interval = window.setInterval(function () {
      i++;
      const array = JSON.parse(path)
      const subpath = array.slice(0, i * 5);
      that.request(that, subpath)
      if (i > 5) {
        window.clearInterval(interval)
      }
    }, 10000);
  }

  componentWillReceiveProps(nextProps) {
    const map = this.map;
    const {
      blue,
      orange,
      black,
      red,
      maroon,
    } = nextProps.general;
    if (blue) {
      map.getSource('blue').setData(blue);
    }
    if (orange) {
      map.getSource('orange').setData(orange);
    }
    if (black) {
      map.getSource('black').setData(black);
    }
    if (red) {
      map.getSource('red').setData(red);
    }
    if (maroon) {
      map.getSource('maroon').setData(maroon);
    }
    this.setState({
      blue: {
        title: blue ? blue.properties.title : '',
        visible: blue !== undefined,
      },
      orange: {
        title: orange ? orange.properties.title : '',
        visible: orange !== undefined,
      },
      black: {
        title: black ? black.properties.title : '',
        visible: black !== undefined,
      },
      red: {
        title: red ? red.properties.title : '',
        visible: red !== undefined,
      },
      maroon: {
        title: maroon ? maroon.properties.title : '',
        visible: maroon !== undefined,
      },
    })
  }

  toggleVisibility = name => event => {
    const map = this.map;
    const clickedLayer = name + '-layer'
    var visibility = map.getLayoutProperty(clickedLayer, 'visibility');

    if (visibility === 'visible') {
      map.setLayoutProperty(clickedLayer, 'visibility', 'none');
      this.className = '';
    } else {
      this.className = 'active';
      map.setLayoutProperty(clickedLayer, 'visibility', 'visible');
    }
    this.setState({
      [name]: Object.assign({}, this.state[name], {
        visible: event.target.checked
      })
    });
  };

  loadMap() {
    const map = new mapboxgl.Map({
      container: this.mapContainer,
      style: 'mapbox://styles/mapbox/streets-v9',
      center: [this.props.center.lng, this.props.center.lat],
      zoom: this.props.zoom
    });
    let that = this;
    map.on('load', function () {
      map.addSource('maroon', utils.emptyFeatureCollection);
      map.addSource('blue', utils.emptyFeatureCollection);
      map.addSource('black', utils.emptyFeatureCollection);
      map.addSource('green', utils.emptyFeatureCollection);
      map.addSource('red', utils.emptyFeatureCollection);
      map.addSource('orange', utils.emptyFeatureCollection);
      map.addLayer(utils.maroonLayer);
      map.addLayer(utils.blueLayer);
      map.addLayer(utils.blackLayer);
      map.addLayer(utils.greenLayer);
      map.addLayer(utils.redLayer);
      map.addLayer(utils.orangeLayer);
      map.resize();
    });
    let path = []
    that = this
    map.on("click", function (e) {
      let lng = e.lngLat.lng.toFixed(5);
      let lat = e.lngLat.lat.toFixed(5);
      path.push([lng, lat])
      if (path.length > 3) {
        that.request(that, path)
      }
      console.log(JSON.stringify(path).replace(/['"]+/g, ''))
    })
    map.addControl(new mapboxgl.NavigationControl());
    this.map = map;
  }

  renderControls() {
    let controls = [];
    utils.toggleableLayers.forEach((value) => {
      controls.push(
        <FormControlLabel
          control={
            <Switch
              checked={this.state[value].visible}
              onChange={this.toggleVisibility(value)}
            />
          }
          disabled={!this.state[value].title}
          key={'button-' + value}
          label={'toggle ' + this.state[value].title}
        />

      )
    });
    return controls;
  }

  render() {
    return (
      <div>
        <div>
          <Button aria-label="Generate" onClick={() => this.generate()}>
            <NavigationIcon />
            Generate
          </Button>
          <Select
            value={this.state.method}
            onChange={(event) => this.setState({method: event.target.value})}
          >
          {
            utils.requestTypes.map((value) => {
              return (<MenuItem value={value}>{value}</MenuItem>)
            })
          }
          </Select>
          <Select
            value={this.state.dataset}
            onChange={(event) => this.setState({dataset: event.target.value})}
          >
            <MenuItem value={"zg"}>Zagreb</MenuItem>
            <MenuItem value={"porto"}>Porto</MenuItem>
          </Select>
          <Button onClick={() => this.recentre()}>
            Recentre
          </Button>
        </div>
        <div ref={el => this.mapContainer = el} className="map" />
        <FormGroup row>
          {this.renderControls()}
        </FormGroup>
      </div>

    )
  }
}

const mapStateToProps = state => ({
  general: state.app.general,
})

const mapDispatchToProps = dispatch => ({
  getPrediction: (path, user, query) => dispatch(appActions.predictedPath(path, user, query))
})

export default connect(mapStateToProps, mapDispatchToProps)(MapInterface);