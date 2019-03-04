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
            advanced: true,
            prediction: true,
            direction: true,
            optional: true,
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
        let option = 0;
        let path = (option===0) ? "[[-8.618643,41.141412],[-8.618499,41.141376],[-8.620326,41.14251],[-8.622153,41.143815],[-8.623953,41.144373],[-8.62668,41.144778],[-8.627373,41.144697],[-8.630226,41.14521],[-8.632746,41.14692],[-8.631738,41.148225],[-8.629938,41.150385],[-8.62911,41.151213],[-8.629128,41.15124],[-8.628786,41.152203],[-8.628687,41.152374],[-8.628759,41.152518],[-8.630838,41.15268],[-8.632323,41.153022],[-8.631144,41.154489],[-8.630829,41.154507],[-8.630829,41.154516],[-8.630829,41.154498],[-8.630838,41.154489]]"
        : (option>1) ? "[[-8.585676,41.148522],[-8.585712000000001,41.148638999999996],[-8.585685000000002,41.148855000000005],[-8.585730000000002,41.14892699999999],[-8.585982,41.148962999999995],[-8.586396,41.148954],[-8.586072,41.14872],[-8.586324000000001,41.147847],[-8.586999,41.147459999999995],[-8.586575999999999,41.14715400000001],[-8.584883999999999,41.146623000000005]]"
        :"[[-8.610876000000001, 41.14557], [-8.610858, 41.145579000000005], [-8.610903, 41.145768], [-8.610444, 41.146190999999995], [-8.609445000000001, 41.146758], [-8.608896, 41.147118], [-8.608968, 41.147127], [-8.608707, 41.147532000000005], [-8.608347, 41.148117000000006], [-8.608149,41.148351000000005],[-8.608041,41.148576000000006],[-8.607654,41.14926],[-8.607348000000002,41.149899000000005],[-8.607393,41.149899000000005],[-8.607357,41.149962],[-8.606817,41.150979],[-8.606358,41.151914999999995],[-8.605719,41.152788],[-8.604981,41.153318999999996],[-8.604783,41.154345],[-8.604828,41.154372],[-8.604801,41.155353],[-8.604648000000001,41.156774999999996],[-8.604522,41.158197],[-8.604513,41.159943000000005],[-8.604377999999999,41.16055500000001],[-8.604377999999999,41.1606],[-8.604369,41.160644999999995],[-8.60436,41.160807],[-8.604162,41.161176],[-8.604126,41.161248],[-8.60409,41.16129300000001],[-8.60409,41.161266000000005],[-8.604108,41.161239],[-8.604126,41.161194],[-8.604135,41.161275],[-8.60391,41.162048999999996],[-8.602929000000001,41.162832],[-8.602551000000002,41.163111],[-8.601894,41.163597]]"
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