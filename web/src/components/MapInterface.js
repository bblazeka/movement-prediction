import React, { Component } from 'react';
import mapboxgl from 'mapbox-gl';
import { connect } from 'react-redux';
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
            advanced: false,
            prediction: false,
            direction: true,
            optional: false,
            training: false
        }
    }

    static defaultProps = {
        center: { lat: 41.15, lng: -8.61 },
        zoom: 13
    }

    request(that,path) {
        if (that.map) {
            that.map.getSource('input').setData({
                "type": "FeatureCollection",
                "features": path.map(function(v) {
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
        that.props.getPrediction(0,JSON.stringify(path).replace(/['"]+/g, ''))
    }

    componentDidMount() {
        this.loadMap();
        let i = 0;
        let that = this;
        let path = utils.demoQuery();
        let interval = window.setInterval(function() {
            i++;
            const array = JSON.parse(path)
            const subpath = array.slice(0,i*5);
            that.request(that,subpath)
            if (i > 5) {
                window.clearInterval(interval)
            }
        }, 5000);
    }

    componentWillReceiveProps(nextProps) {
        const map = this.map;
        map.getSource('prediction').setData(nextProps.general.predicted);
        map.getSource('training').setData(nextProps.general.training);
        map.getSource('direction').setData(nextProps.general.direction);
        map.getSource('optional').setData(nextProps.general.optional);
        map.getSource('advanced').setData(nextProps.general.advanced);
    }

    toggleVisibility = name => event => {
        const map = this.map;
        const clickedLayer = name+'-layer'
        var visibility = map.getLayoutProperty(clickedLayer, 'visibility');
             
            if (visibility === 'visible') {
            map.setLayoutProperty(clickedLayer, 'visibility', 'none');
            this.className = '';
            } else {
            this.className = 'active';
            map.setLayoutProperty(clickedLayer, 'visibility', 'visible');
        }
        this.setState({ [name]: event.target.checked });
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
            map.addSource('advanced', utils.emptyFeatureCollection);
            map.addSource('prediction', utils.emptyFeatureCollection);
            map.addSource('direction', utils.emptyFeatureCollection);
            map.addSource('input', utils.emptyFeatureCollection);
            map.addSource('optional', utils.emptyFeatureCollection);
            map.addSource('training', utils.emptyFeatureCollection);
            map.addLayer(utils.advancedLayer);
            map.addLayer(utils.predictionLayer);
            map.addLayer(utils.directionLayer);
            map.addLayer(utils.inputLayer);
            map.addLayer(utils.optionalLayer);
            map.addLayer(utils.trainingLayer);
            map.resize();
        });
        let path = []
        that = this
        map.on("click", function(e) {
            let lng = e.lngLat.lng.toFixed(3);
            let lat = e.lngLat.lat.toFixed(3);
            path.push([lng,lat])
            if (path.length > 3) {
                that.request(that,path)
            }
            console.log(JSON.stringify(path).replace(/['"]+/g, ''))
        })
        map.addControl(new mapboxgl.NavigationControl());
        this.map = map;
    }

    renderButtons() {
        let controls = [];
        utils.toggleableLayers.forEach((value) => {
            controls.push(
            <FormControlLabel
                control={
                  <Switch
                    checked={this.state[value]}
                    onChange={this.toggleVisibility(value)}
                  />
                }
                key={'button-'+value}
                label={'toggle '+value}
              />
            
          )
        });
        return controls;
    }

    render() {
        return (
            <div>
                <div ref={el => this.mapContainer = el} className="map"/>
                <FormGroup row>
                  {this.renderButtons()}
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
    getPrediction: (user,path) => dispatch(appActions.predictedPath(user,path))
})

export default connect(mapStateToProps, mapDispatchToProps)(MapInterface);