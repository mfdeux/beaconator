import Vue from 'vue';
import Vuex from 'vuex';
import router from '../router';
import Cookies from 'js-cookie';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    auth: null,
    options: {
      codes: [],
    },
  },
  mutations: {
    UPDATE_AUTH(state, value) {
      state.auth = value;
    },
    UPDATE_CODE_OPTIONS(state, values) {
      state.options.codes = [...values];
    },
  },
  actions: {
    async CLIENT_INIT({ commit, dispatch }) {
      let auth = null;
      if (Cookies.get('beaconator.auth')) {
        auth = Cookies.get('beaconator.auth');
        commit('UPDATE_AUTH', auth);
      }
    },
    LOGIN_USER({ state, commit }, token) {
      commit('UPDATE_AUTH', token);
      Cookies.set('beaconator.auth', token, {
        expires: 60 * 60 * 24 * 365,
        path: '/',
      });
      router.push('/properties');
    },
    LOGOUT_USER({ commit }) {
      commit('UPDATE_AUTH', null);
      Cookies.remove('beaconator.auth');
      router.push('/login');
    },
  },
  modules: {},
});
