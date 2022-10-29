import { configureStore } from '@reduxjs/toolkit';
import sessionSlice from '../features/sessionSlice';
import timerSlice from '../features/timerSlice';

export const store = configureStore({
  reducer: {
    session: sessionSlice,
    timer: timerSlice
  },
}, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__());
