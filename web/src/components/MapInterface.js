import React, { Component } from 'react';
import mapboxgl from 'mapbox-gl';
import { connect } from 'react-redux';
import * as appActions from '../actions/appActions';

import './Map.css';

mapboxgl.accessToken = 'pk.eyJ1IjoiYnJhbmNhIiwiYSI6ImNqcWprdnNodzA0aDMzeHMxZndrYnhucDgifQ.jUE6YbihyEe0kvTfbvD6iw';

class MapInterface extends Component {

    static defaultProps = {
        center: { lat: 41.15, lng: -8.61 },
        zoom: 10
    }

    componentDidMount() {
        this.props.getPrediction(0,"[[-8.585,41.148],[-8.585,41.148],[-8.585,41.148],[-8.585,41.148]]")
        this.props.getPrediction(4,"[[-8.585,41.148],[-8.585,41.148],[-8.585,41.148],[-8.585,41.148]]")
    }

    componentWillReceiveProps(nextProps) {
        console.log("nextprops",nextProps)
        const map = new mapboxgl.Map({
            container: this.mapContainer,
            style: 'mapbox://styles/mapbox/streets-v9',
            center: [nextProps.center.lng, nextProps.center.lat],
            zoom: nextProps.zoom
        });
        map.addControl(new mapboxgl.NavigationControl());

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
            map.on('load', function () {
                map.addSource('trajectory', {
                    type: 'geojson',
                    data: trajectory
                });
                map.addSource('extended', {
                    type: 'geojson',
                    data: extended
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
            });
            map.resize();
        }
        
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