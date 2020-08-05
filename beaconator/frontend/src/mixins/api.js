const APIURL = 'http://127.0.0.1:8000/api';
const axios = require('axios');
import router from '../router';
import store from '../store';
import Cookie from 'js-cookie';

axios.interceptors.request.use(
  (config) => {
    let token = store.state.auth;

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    return config;
  },

  (error) => {
    return Promise.reject(error);
  }
);

// // axios.onRequest(request => {
// //   request.baseURL = process.env.baseClientRestApiUrl
// //   if (!process.server) {
// //     if (store.state.auth) {
// //       const token = store.state.auth
// //       if (token) request.headers.common.Authorization = `Bearer ${token}`
// //     }
// //   }
// // })

// app.$axios.onRequest(request => {
//   request.baseURL = process.env.baseClientRestApiUrl
//   if (!process.server) {
//     if (store.state.auth) {
//       const token = store.state.auth
//       if (token) request.headers.common.Authorization = `Bearer ${token}`
//     }
//   }

// axios.onError(async (error) => {
//   // if (!error.response) {
//   //   errorPage({ statusCode: 404, message: 'Post not found' })
//   //   return
//   // }

//   const code = parseInt(error.response && error.response.status);

//   if (code === 401) {
//     router.push('/login');
//   }

//   if (code === 403) {
//     router.push('/login');
//   }
// });

export default {
  getCodes() {
    return axios.get(`${APIURL}/codes`);
  },
  getProperties() {
    return axios.get(`${APIURL}/properties`);
  },
  deleteCode(id) {
    return axios.delete(`${APIURL}/codes/${id}`);
  },
  deleteProperty(id) {
    return axios.delete(`${APIURL}/properties/${id}`);
  },
  createCode(data) {
    return axios.post(`${APIURL}/codes`, data);
  },
  createProperty(data) {
    return axios.post(`${APIURL}/properties`, data);
  },
  updateCode(id, data) {
    return axios.patch(`${APIURL}/codes/${id}`, data);
  },
  updateProperty(id, data) {
    return axios.patch(`${APIURL}/properties/${id}`, data);
  },
};
