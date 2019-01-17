import React, { Component } from 'react';
import mapboxgl from 'mapbox-gl';
import { connect } from 'react-redux';
import * as appActions from '../actions/appActions';

import './Map.css';

mapboxgl.accessToken = 'pk.eyJ1IjoiYnJhbmNhIiwiYSI6ImNqcWprdnNodzA0aDMzeHMxZndrYnhucDgifQ.jUE6YbihyEe0kvTfbvD6iw';

class MapInterface extends Component {
    map;

    static defaultProps = {
        center: { lat: 41.15, lng: -8.61 },
        zoom: 12
    }

    componentDidMount() {
        this.loadMap();
        let i = 0;
        let that = this;
        let path = "[[-8.618643,41.141412],[-8.618499,41.141376],[-8.620326,41.14251],[-8.622153,41.143815],[-8.623953,41.144373],[-8.62668,41.144778],[-8.627373,41.144697],[-8.630226,41.14521],[-8.632746,41.14692],[-8.631738,41.148225],[-8.629938,41.150385],[-8.62911,41.151213],[-8.629128,41.15124],[-8.628786,41.152203],[-8.628687,41.152374],[-8.628759,41.152518],[-8.630838,41.15268],[-8.632323,41.153022],[-8.631144,41.154489],[-8.630829,41.154507],[-8.630829,41.154516],[-8.630829,41.154498],[-8.630838,41.154489]]"
        window.setInterval(function() {
            i++;
            const array = JSON.parse(path)
            const subpath = array.slice(0,i*5);
            that.props.getPrediction(4,JSON.stringify(subpath).replace(/['"]+/g, ''))
            that.props.getPrediction(0,JSON.stringify(subpath).replace(/['"]+/g, ''))
        }, 5000);
    }

    componentWillReceiveProps(nextProps) {
        console.log("nextprops",nextProps)
        const map = this.map;

        // if both path predictions have loaded
        if (nextProps.general && nextProps.individual) {
            let trajectory = {
                "type": "FeatureCollection",
               "features": nextProps.general.map(function(v) {
              return {
                     "type": "Feature",
                      "geometry": {
                          "type": "Point",
                           "coordinates": [v.long, v.lat]
                      }
                  };
                })
            };
            let extended = {
                "type": "FeatureCollection",
                "features": nextProps.individual.map(function(v) {
               return {
                      "type": "Feature",
                       "geometry": {
                           "type": "Point",
                            "coordinates": [v.long, v.lat]
                       }
                   };
                 })
            }
            map.getSource('trajectory').setData(trajectory);
            map.getSource('extended').setData(extended);
        }
    }

    loadMap() {
        const map = new mapboxgl.Map({
            container: this.mapContainer,
            style: 'mapbox://styles/mapbox/streets-v9',
            center: [this.props.center.lng, this.props.center.lat],
            zoom: this.props.zoom
        });
        let that = this;
        map.on('load', function () {
            map.addSource('trajectory', {
                type: 'geojson',
                data: {
                    "type": "FeatureCollection",
                    "features": []
                }
            });
            map.addSource('extended', {
                type: 'geojson',
                data: {
                    "type": "FeatureCollection",
                    "features": []
                }
            });
            map.addLayer({
                 'id': 'trajectory-layer',
                'type': 'circle',
                 'source': 'trajectory',
                'layout': {
                     'visibility': 'visible'
                 },
                 'paint': {
                 'circle-radius': 2,
                  'circle-color': 'rgba(55,148,179,1)'
                 }
            });
            map.addLayer({
                'id': 'extended-layer',
               'type': 'circle',
                'source': 'extended',
               'layout': {
                    'visibility': 'visible'
                },
                'paint': {
                'circle-radius': 2,
                 'circle-color': 'rgba(128,0,0,1)'
                }
            });
            map.resize();
        });
        let path = []
        map.on("click", function(e) {
            let lng = e.lngLat.lng.toFixed(3);
            let lat = e.lngLat.lat.toFixed(3);
            path.push([lng,lat])
            if (path.length > 3) {
                that.props.getPrediction(4,JSON.stringify(path).replace(/['"]+/g, ''))
                that.props.getPrediction(0,JSON.stringify(path).replace(/['"]+/g, ''))
            }
            console.log(JSON.stringify(path).replace(/['"]+/g, ''))
        })
        map.addControl(new mapboxgl.NavigationControl());
        this.map = map;
    }

    render() {
        return (
            <div ref={el => this.mapContainer = el} className="map"/>
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