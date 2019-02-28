export const PREDICT_PATH = 'PREDICT_PATH'
export const GENERAL_PREDICTION_LOADED = 'GENERAL_PREDICTION_LOADED'
export const INDIVIDUAL_PREDICTION_LOADED = 'INDIVIDUAL_PREDICTION_LOADED'

export const predictedPath = (user,path) => ({
  type: PREDICT_PATH,
  payload: {
    user,
    path
  }
})