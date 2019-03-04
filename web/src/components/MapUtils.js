export const toggleableLayers = [ 'optional', 'prediction', 'direction', 'training', 'advanced' ];
export const token = 'pk.eyJ1IjoiYnJhbmNhIiwiYSI6ImNqcWprdnNodzA0aDMzeHMxZndrYnhucDgifQ.jUE6YbihyEe0kvTfbvD6iw';

export const emptyFeatureCollection = {
    type: 'geojson',
    data: {
        "type": "FeatureCollection",
        "features": []
    }
}

export const predictionLayer = {
    'id': 'prediction-layer',
   'type': 'circle',
    'source': 'prediction',
   'layout': {
        'visibility': 'visible'
    },
    'paint': {
    'circle-radius': 2,
     'circle-color': 'rgba(55,148,179,1)'
    }
}

export const directionLayer = {
    'id': 'direction-layer',
   'type': 'circle',
    'source': 'direction',
   'layout': {
        'visibility': 'visible'
    },
    'paint': {
    'circle-radius': 2,
     'circle-color': 'rgba(0,0,0,1)'
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

export const optionalLayer = {
    'id': 'optional-layer',
   'type': 'circle',
    'source': 'optional',
   'layout': {
        'visibility': 'visible'
    },
    'paint': {
    'circle-radius': 2,
     'circle-color': 'rgba(255,0,0,1)'
    }    
}

export const trainingLayer = {
    'id': 'training-layer',
   'type': 'circle',
    'source': 'training',
   'layout': {
        'visibility': 'none'
    },
    'paint': {
    'circle-radius': 1,
     'circle-color': 'rgba(255,165,0,1)'
    }    
}

export const advancedLayer = {
    'id': 'advanced-layer',
   'type': 'circle',
    'source': 'advanced',
   'layout': {
        'visibility': 'visible'
    },
    'paint': {
    'circle-radius': 2,
     'circle-color': 'rgba(128,0,0,1)'
    }    
}