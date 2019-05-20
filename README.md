# Movement Prediction

Using various algorithms/methods to dynamically predict movement, such as: *Polynomial regression*, *Instance based learning* or *Markov model*. They can be compared, evaluated or viewed separately.

Project consists out of two important components. First one is server component (Flask, Python) that generates the prediction and a client component (React, Javascript) that displays the prediction on a Mapbox map component. Initially, a default example runs. Map component is capable of receiving input, switches to that mode after first three points are clicked on a map.

Suggested input is [ECML-PKDD 2015 Taxi prediction](https://www.kaggle.com/c/pkdd-15-predict-taxi-service-trajectory-i) in a folder data/PortoTaxi in root directory or output of [SUMO](https://sumo.dlr.de/index.html) in a folder data/sumo.

Detailed description to be added...

# Running

- database: MongoDB (run with: `sudo service mongod start`)

- evaluation: jupyter notebook

- run pipenv: pipenv shell

- server: Flask (run with: `FLASK_APP=server.py flask run`)

- web: React.js (run with: `npm start`)
