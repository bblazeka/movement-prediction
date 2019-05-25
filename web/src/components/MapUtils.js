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

export function demoQuery() {
  let option = -1;
  return (option === 0) ? "[[-8.618643,41.141412],[-8.618499,41.141376],[-8.620326,41.14251],[-8.622153,41.143815],[-8.623953,41.144373],[-8.62668,41.144778],[-8.627373,41.144697],[-8.630226,41.14521],[-8.632746,41.14692],[-8.631738,41.148225],[-8.629938,41.150385],[-8.62911,41.151213],[-8.629128,41.15124],[-8.628786,41.152203],[-8.628687,41.152374],[-8.628759,41.152518],[-8.630838,41.15268],[-8.632323,41.153022],[-8.631144,41.154489],[-8.630829,41.154507],[-8.630829,41.154516],[-8.630829,41.154498],[-8.630838,41.154489]]"
    : (option > 1) ? "[[-8.585676,41.148522],[-8.585712000000001,41.148638999999996],[-8.585685000000002,41.148855000000005],[-8.585730000000002,41.14892699999999],[-8.585982,41.148962999999995],[-8.586396,41.148954],[-8.586072,41.14872],[-8.586324000000001,41.147847],[-8.586999,41.147459999999995],[-8.586575999999999,41.14715400000001],[-8.584883999999999,41.146623000000005]]"
      : "[[15.9533,45.7944],[15.9554,45.7944],[15.9582,45.7943],[15.9590,45.7952],[15.9599,45.7960],[15.9602,45.7972],[15.9609,45.7979],[15.9618,45.7984],[15.9621,45.7991],[15.9636,45.7995],[15.9654,45.7995],[15.9667,45.7996],[15.9679,45.7996],[15.9693,45.7995],[15.9689,45.8007]]"
}