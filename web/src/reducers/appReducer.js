const defaultAppState = {
    loaded: false
}

export default (state = defaultAppState, action) => {
    switch (action.type) {
        case 'PREDICTION_LOADED':
            return {
                ...state,
                general: action.payload
            }
        default:
            return state
    }
}