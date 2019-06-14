export const PREDICT_PATH = 'PREDICT_PATH'
export const PREDICTION_LOADED = 'PREDICTION_LOADED'

export const predictedPath = (path,mode,query) => ({
  type: PREDICT_PATH,
  payload: {
    path,
    mode,
    query,
  }
})