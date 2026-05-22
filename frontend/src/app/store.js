import { configureStore } from "@reduxjs/toolkit";

import ideasReducer from "../features/ideasSlice";

export const store = configureStore({
  reducer: {
    ideas: ideasReducer,
  },
});
