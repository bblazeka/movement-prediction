export const trajectoryLayer = {
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
}

export const extendedLayer = {
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