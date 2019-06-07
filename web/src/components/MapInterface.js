import React, { Component } from 'react';
import mapboxgl from 'mapbox-gl';
import { connect } from 'react-redux';
import Button from '@material-ui/core/Button';
import Switch from '@material-ui/core/Switch';
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
    // currently disabled personalized prediction: change 0 and 4
    that.props.getPrediction(this.state.method, 0, JSON.stringify(path).replace(/['"]+/g, ''))
  }

  componentDidMount() {
    this.loadMap();
    let i = 0;
    let that = this;
    let path = utils.demoQuery();
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
    // layer with prediction from instance based learning
    map.getSource('blue').setData(blue);
    // layer with training data
    map.getSource('orange').setData(orange);
    // layer with prediction from polynomial regression
    map.getSource('black').setData(black);
    // layer with linear regression of last few points of input data
    map.getSource('red').setData(red);
    // polynomial regression prediction with road matching applied
    map.getSource('maroon').setData(maroon);
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

  renderButtons() {
    let options = []
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
          <Button
            color={this.state.method === 'compare' ? 'primary' : 'secondary'}
            onClick={() => this.setState({method: 'compare'})}
          >
            Compare
          </Button>
          <Button
            color={this.state.method === 'regression' ? 'primary' : 'secondary'}
            onClick={() => this.setState({method: 'regression'})}
          >
            Regression
          </Button>
          <Button
            disabled
            color={this.state.method === 'instance' ? 'primary' : 'secondary'}
            onClick={() => this.setState({method: 'instance'})}
          >
            Instance
          </Button>
          <Button
            disabled
            color={this.state.method === 'markov' ? 'primary' : 'secondary'}
            onClick={() => this.setState({method: 'markov'})}
          >
            Markov
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
  individual: state.app.individual
})

const mapDispatchToProps = dispatch => ({
  getPrediction: (path, user, query) => dispatch(appActions.predictedPath(path, user, query))
})

export default connect(mapStateToProps, mapDispatchToProps)(MapInterface);