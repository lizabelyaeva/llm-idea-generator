import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import { api } from "../services/api";

export const loadMe = createAsyncThunk("auth/loadMe", async () => api.me());

export const login = createAsyncThunk("auth/login", async (payload) => {
  const data = await api.login(payload);
  sessionStorage.setItem("access_token", data.access_token);
  return data.user;
});

export const register = createAsyncThunk("auth/register", async (payload) => {
  const data = await api.register(payload);
  sessionStorage.setItem("access_token", data.access_token);
  return data.user;
});

const authSlice = createSlice({
  name: "auth",
  initialState: {
    user: null,
    loading: false,
    initialized: false,
    error: null,
  },
  reducers: {
    logout(state) {
      sessionStorage.removeItem("access_token");
      state.user = null;
      state.initialized = true;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadMe.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loadMe.fulfilled, (state, action) => {
        state.loading = false;
        state.initialized = true;
        state.user = action.payload;
      })
      .addCase(loadMe.rejected, (state) => {
        state.loading = false;
        state.initialized = true;
        state.user = null;
      })
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.initialized = true;
        state.user = action.payload;
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Не удалось войти";
      })
      .addCase(register.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(register.fulfilled, (state, action) => {
        state.loading = false;
        state.initialized = true;
        state.user = action.payload;
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Не удалось зарегистрироваться";
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
