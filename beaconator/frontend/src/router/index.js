import Vue from 'vue';
import store from '../store';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    redirect: '/properties',
  },
  {
    path: '/login',
    name: 'Login',
    beforeEnter: (to, from, next) => {
      if (!store.state.auth) {
        next();
      } else {
        next('/properties');
      }
    },
    component: () => import(/* webpackChunkName: "login" */ '../views/accounts/Login.vue'),
  },
  {
    path: '/codes',
    name: 'Codes',
    meta: {
      auth: true,
    },
    component: () => import(/* webpackChunkName: "codes" */ '../views/codes/Codes.vue'),
  },
  {
    path: '/properties',
    name: 'Properties',
    meta: {
      auth: true,
    },
    // eslint-disable-next-line
    component: () =>
      // eslint-disable-next-line
      import(/* webpackChunkName: "properties" */ '../views/properties/Properties.vue'),
  },
];

const router = new VueRouter({
  routes,
});

router.beforeEach(async (to, from, next) => {
  await store.dispatch('CLIENT_INIT');
  if (to.matched.some((record) => record.meta.auth)) {
    if (store.state.auth) {
      next();
    } else {
      next('/login');
    }
  } else {
    next();
  }
});

export default router;
