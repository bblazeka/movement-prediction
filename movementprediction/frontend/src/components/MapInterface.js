import React from 'react';
import mapboxgl from 'mapbox-gl';

mapboxgl.accessToken = 'pk.eyJ1IjoiYnJhbmNhIiwiYSI6ImNqbnliMmVoeTA1MTMzcG54Y3h2bnFtYmwifQ.o6CzepqOg00rpv7wKNeOuQ';

export default class MapInterface extends React.Component {
    static defaultProps = {
        center: { lat: 41.15, lng: -8.61 },
        zoom: 12
      }

    componentDidMount() {

        const map = new mapboxgl.Map({
            container: this.mapContainer,
            style: 'mapbox://styles/mapbox/streets-v9',
            center: [this.props.center.lng, this.props.center.lat],
            zoom: this.props.zoom
        });

        this.props.data.forEach(function(marker) {
            // create a HTML element for each feature
            var el = document.createElement('div');
            el.className = 'marker';             
            el.style.width = '5px';                                                      
            el.style.height = '5px';
            el.style.borderRadius = '50%';
            el.style.border = '1px solid gray';
            el.style.backgroundColor = 'lightblue';

            // make a marker for each feature and add to the map
            new mapboxgl.Marker(el)
            .setLngLat([marker.long,marker.lat])
            .addTo(map);
        });
    }

    render() {
        return (
            !this.props.data.length ? (
              <p>Nothing to show</p>
            ) : (
                <div>
                  <div ref={el => this.mapContainer = el} className="absolute top right left bottom" />
                </div>
            )
        )
    }
}