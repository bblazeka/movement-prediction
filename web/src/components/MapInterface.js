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
            maroon: false,
            blue: true,
            black: true,
            red: false,
            orange: false
        }
    }

    static defaultProps = {
        center: { lat: 41.15, lng: -8.61 },
        zoom: 13
    }

    request(that,path) {
        if (that.map) {
            that.map.getSource('green').setData({
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
        that.props.getPrediction('compare',0,JSON.stringify(path).replace(/['"]+/g, ''))
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
        // layer with prediction from instance based learning
        map.getSource('blue').setData(nextProps.general.blue);
        // layer with training data
        map.getSource('orange').setData(nextProps.general.orange);
        // layer with prediction from polynomial regression
        map.getSource('black').setData(nextProps.general.black);
        // layer with linear regression of last few points of input data
        map.getSource('red').setData(nextProps.general.red);
        // polynomial regression prediction with road matching applied
        map.getSource('maroon').setData(nextProps.general.maroon);
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
    getPrediction: (path,user,query) => dispatch(appActions.predictedPath(path,user,query))
})

export default connect(mapStateToProps, mapDispatchToProps)(MapInterface);