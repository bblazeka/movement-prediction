export const emptyFeatureCollection = {
    type: 'geojson',
    data: {
        "type": "FeatureCollection",
        "features": []
    }
}

export const individualLayer = {
    'id': 'individual-layer',
   'type': 'circle',
    'source': 'individual',
   'layout': {
        'visibility': 'visible'
    },
    'paint': {
    'circle-radius': 2,
     'circle-color': 'rgba(55,148,179,1)'
    }
}

export const generalLayer = {
    'id': 'general-layer',
   'type': 'circle',
    'source': 'general',
   'layout': {
        'visibility': 'visible'
    },
    'paint': {
    'circle-radius': 2,
     'circle-color': 'rgba(128,0,0,1)'
    }
}

export const inputLayer = {
    'id': 'input-layer',
   'type': 'circle',
    'source': 'input',
   'layout': {
        'visibility': 'visible'
    },
    'paint': {
    'circle-radius': 3,
     'circle-color': 'rgba(0,100,0,1)'
    }
}