import { createSlice} from "@reduxjs/toolkit";

export const loaderSlice= createSlice({
  name: "loader",
  initialState: {
    fileUploadLoading:false,
    normalLoading:false,
    skeletonLoading:false,
    profileLoading:false,
    searchLoading:false,
    currentPage:"Home"
  },
  reducers: {
   fileUploadLoader:(state)=>{
       state.fileUploadLoading=!state.fileUploadLoading
   },
   normalLoader:(state)=>{
     state.normalLoading=!state.normalLoading
   },
   skeletonLoader:(state)=>{
     state.skeletonLoading=!state.skeletonLoading
   },
   profileLoader:(state)=>{
     state.profileLoading=!state.profileLoading
   },
   searchLoader:(state)=>{
     state.searchLoading=!state.searchLoading
   },
   setCurrentPage:(state,action)=>{
     state.currentPage=action.payload
   }
  },
});

export const {
  fileUploadLoader,
  normalLoader,
  skeletonLoader,
  profileLoader,
  searchLoader,
  setCurrentPage
} = loaderSlice.actions;

export const fileLoading = (state) => state.loader.fileUploadLoading;
export const normalLoading = (state) => state.loader.normalLoading;
export const skeletonLoading=(state)=>state.loader.skeletonLoading
export const profileLoading=(state)=>state.loader.profileLoading
export const searchLoading=(state)=>state.loader.searchLoading
export const selectPage  = (state)=>state.loader.currentPage

export default loaderSlice.reducer;
