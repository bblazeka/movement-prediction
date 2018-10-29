import React from 'react';
import Marker from './Marker.js';
import GoogleMapReact from 'google-map-react'

const googlemaps = require('../../../../apikeys.json')
export default class MapInterface extends React.Component {
    static defaultProps = {
        center: { lat: 41.15, lng: -8.61 },
        zoom: 12
      }

    rendercomponents(data){
        let marks = []
        for(let ind in data){
            let point = data[ind]
            marks.push(
                <Marker
                    key={ point.id }
                    lat={ point.lat }
                    lng={ point.long }
                />)
        }
        return marks
    }

    render() {
        console.log(this.props.data.length)
        return (
            !this.props.data.length ? (
              <p>Nothing to show</p>
            ) : (
                <div style={{ height: '100vh', width: '100%' }}>
                <GoogleMapReact
                    bootstrapURLKeys={{key: googlemaps.googlemaps}}
                  defaultCenter={ this.props.center }
                  defaultZoom={ this.props.zoom }>
                    {this.rendercomponents(this.props.data)}
                </GoogleMapReact>
              </div>
            )
        )
    }
}