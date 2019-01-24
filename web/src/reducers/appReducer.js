const defaultAppState = {
    loaded: false
}

export default (state = defaultAppState, action) => {
    switch (action.type) {
        case 'GENERAL_PREDICTION_LOADED':
            return {
                ...state,
                general: action.payload
            }
        case 'SPECIFIC_PREDICTION_LOADED':
            return {
                ...state,
                individual: action.payload
            }
        default:
            return state
    }
}