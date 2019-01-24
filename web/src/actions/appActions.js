const endpoint = "http://localhost:5000/api/path"

export const predictedPath = (user,path) => (dispatch, getState) => {
    fetch(endpoint+"?user="+user+"&input="+path)
      .then(response => {
        console.log(response)
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then(data => {
          if (user === 0) {
            dispatch({
              type: 'GENERAL_PREDICTION_LOADED',
              payload: data
            })
          } else {
            dispatch({
              type: 'SPECIFIC_PREDICTION_LOADED',
              payload: data
            })
          }
        });
}