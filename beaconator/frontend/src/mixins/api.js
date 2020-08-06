const makeURL = () => {
  if (window.location.port) {
    return `${window.location.protocol}//${window.location.hostname}:${window.location.port}/images/${this.property.code}`;
  }
  return `${window.location.protocol}//${window.location.hostname}/images/${this.property.code}`;
};
const APIURL = process.NODE_ENV === 'production' ? makeURL() : 'http://127.0.0.1:8000/api';
const axios = require('axios');
import store from '../store';

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
