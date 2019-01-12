import React from 'react';
import mapboxgl from 'mapbox-gl';

import './Map.css';

mapboxgl.accessToken = 'pk.eyJ1IjoiYnJhbmNhIiwiYSI6ImNqcWprdnNodzA0aDMzeHMxZndrYnhucDgifQ.jUE6YbihyEe0kvTfbvD6iw';

export default class MapInterface extends React.Component {

    static defaultProps = {
        center: { lat: 41.15, lng: -8.61 },
        zoom: 10
    }

    componentDidMount() {
        const map = new mapboxgl.Map({
            container: this.mapContainer,
            style: 'mapbox://styles/mapbox/streets-v9',
            center: [this.props.center.lng, this.props.center.lat],
            zoom: this.props.zoom
        });
        map.addControl(new mapboxgl.NavigationControl());
        let trajectory = {
                 "type": "FeatureCollection",
                "features": this.props.data.data.map(function(v) {
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
            "features": this.props.data.allRoutes.map(function(v) {
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

    render() {
        return (
            <div ref={el => this.mapContainer = el} className="map"/>
        )
    }
}