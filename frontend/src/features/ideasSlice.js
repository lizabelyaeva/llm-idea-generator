import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import { api } from "../services/api";

export const generatePipeline = createAsyncThunk("ideas/generatePipeline", async (payload) => {
  const data = await api.generateIdeas(payload);
  return data;
});

export const refreshIdeas = createAsyncThunk("ideas/refreshIdeas", async (sessionId) => {
  return api.getIdeas(sessionId);
});

export const analyzeIdea = createAsyncThunk("ideas/analyzeIdea", async (ideaId) => {
  return api.analyzeIdea(ideaId);
});

export const scoreIdea = createAsyncThunk("ideas/scoreIdea", async (ideaId) => {
  return api.scoreIdea(ideaId);
});

export const deleteIdea = createAsyncThunk("ideas/deleteIdea", async (ideaId) => {
  await api.deleteIdea(ideaId);
  return ideaId;
});

const ideasSlice = createSlice({
  name: "ideas",
  initialState: {
    sessionId: null,
    items: [],
    loading: false,
    error: null,
  },
  reducers: {
    saveIdea(state, action) {
      const idx = state.items.findIndex((item) => item.id === action.payload.id);
      if (idx >= 0) {
        state.items[idx] = action.payload;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(generatePipeline.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(generatePipeline.fulfilled, (state, action) => {
        state.loading = false;
        state.sessionId = action.payload.session_id;
        state.items = action.payload.ideas;
      })
      .addCase(generatePipeline.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Не удалось сгенерировать идеи";
      })
      .addCase(refreshIdeas.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(refreshIdeas.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(refreshIdeas.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Не удалось загрузить идеи";
      })
      .addCase(analyzeIdea.fulfilled, (state, action) => {
        const idx = state.items.findIndex((item) => item.id === action.payload.id);
        if (idx >= 0) {
          state.items[idx] = action.payload;
        }
      })
      .addCase(scoreIdea.fulfilled, (state, action) => {
        const idx = state.items.findIndex((item) => item.id === action.payload.id);
        if (idx >= 0) {
          state.items[idx] = action.payload;
        }
      })
      .addCase(deleteIdea.fulfilled, (state, action) => {
        state.items = state.items.filter((item) => item.id !== action.payload);
      });
  },
});

export const { saveIdea } = ideasSlice.actions;
export default ideasSlice.reducer;
