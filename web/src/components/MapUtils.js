export const requestTypes = ['compare', 'regression', 'instance', 'markov', 'tests'];
export const cities = [
  {
    name: 'Zagreb',
    value: 'zg',
    center: { lat: 45.8, lng: 15.97 },
    input: ["[[15.9533,45.7944],[15.9554,45.7944],[15.9582,45.7943],[15.9590,45.7952],[15.9599,45.7960],[15.9602,45.7972],[15.9609,45.7979],[15.9618,45.7984],[15.9621,45.7991],[15.9636,45.7995],[15.9654,45.7995],[15.9667,45.7996],[15.9679,45.7996],[15.9693,45.7995],[15.9689,45.8007]]"],
  },
  {
    name: 'Porto',
    value: 'porto',
    center: { lat: 41.16, lng: -8.66 },
    input: [
      "[[-8.61080,41.14594],[-8.61029,41.14615],[-8.60947,41.14613],[-8.60829,41.14615],[-8.60729,41.14616],[-8.60685,41.14696],[-8.60664,41.14762],[-8.60631,41.14834],[-8.60610,41.14888],[-8.60601,41.14931],[-8.60567,41.15006],[-8.60535,41.15098],[-8.60432,41.15097],[-8.60424,41.15019],[-8.60416,41.14939],[-8.60404,41.14867],[-8.60404,41.14790],[-8.60391,41.14726],[-8.60388,41.14650]]",
      "[[-8.618643,41.141412],[-8.618499,41.141376],[-8.620326,41.14251],[-8.622153,41.143815],[-8.623953,41.144373],[-8.62668,41.144778],[-8.627373,41.144697],[-8.630226,41.14521],[-8.632746,41.14692],[-8.631738,41.148225],[-8.629938,41.150385],[-8.62911,41.151213],[-8.629128,41.15124],[-8.628786,41.152203],[-8.628687,41.152374],[-8.628759,41.152518],[-8.630838,41.15268],[-8.632323,41.153022],[-8.631144,41.154489],[-8.630829,41.154507],[-8.630829,41.154516],[-8.630829,41.154498],[-8.630838,41.154489]]",
      "[[-8.61083,41.14485],[-8.61083,41.14560],[-8.61102,41.14608],[-8.61121,41.14668],[-8.61105,41.14747],[-8.61088,41.14820],[-8.61052,41.14901],[-8.61027,41.14987],[-8.61033,41.15055],[-8.60986,41.15114],[-8.60983,41.15186],[-8.61011,41.15268],[-8.61008,41.15390],[-8.60944,41.15451]]"
    ],
  }
]
export const toggleableLayers = ['red', 'blue', 'black', 'orange', 'maroon'];
export const token = 'pk.eyJ1IjoiYnJhbmNhIiwiYSI6ImNqcWprdnNodzA0aDMzeHMxZndrYnhucDgifQ.jUE6YbihyEe0kvTfbvD6iw';

export const emptyFeatureCollection = {
  type: 'geojson',
  data: {
    "type": "FeatureCollection",
    "features": []
  }
}

export const blueLayer = {
  'id': 'blue-layer',
  'type': 'circle',
  'source': 'blue',
  'layout': {
    'visibility': 'visible'
  },
  'paint': {
    'circle-radius': 2,
    'circle-color': 'rgba(55,148,179,1)'
  }
}

export const blackLayer = {
  'id': 'black-layer',
  'type': 'circle',
  'source': 'black',
  'layout': {
    'visibility': 'visible'
  },
  'paint': {
    'circle-radius': 2,
    'circle-color': 'rgba(0,0,0,1)'
  }
}

export const greenLayer = {
  'id': 'green-layer',
  'type': 'circle',
  'source': 'green',
  'layout': {
    'visibility': 'visible'
  },
  'paint': {
    'circle-radius': 3,
    'circle-color': 'rgba(0,100,0,1)'
  }
}

export const redLayer = {
  'id': 'red-layer',
  'type': 'circle',
  'source': 'red',
  'layout': {
    'visibility': 'visible'
  },
  'paint': {
    'circle-radius': 2,
    'circle-color': 'rgba(255,0,0,1)'
  }
}

export const orangeLayer = {
  'id': 'orange-layer',
  'type': 'circle',
  'source': 'orange',
  'layout': {
    'visibility': 'visible'
  },
  'paint': {
    'circle-radius': 2,
    'circle-color': 'rgba(255,165,0,1)'
  }
}

export const maroonLayer = {
  'id': 'maroon-layer',
  'type': 'circle',
  'source': 'maroon',
  'layout': {
    'visibility': 'visible'
  },
  'paint': {
    'circle-radius': 2,
    'circle-color': 'rgba(128,0,0,1)'
  }
}