import Vue from 'vue';
// import VueRouter from 'vue-router';

import App from './App.vue';

Vue.config.productionTip = false;
// Vue.use(VueRouter);

// export const router = new VueRouter({
//   routes: [
//     { path: '/', component: LoginView, props: true },
//     { path: '/login', component: LoginView, props: true },
//     { path: '/user/:username?', component: UserView, props: true },
//     { path: '/settings', component: ProfileEditView, props: true },
//     { path: '/global', component: Main, props: true },
//     { path: '/home', component: TimelineView, props: true},
//     { path: '*', component: NotFoundView, props: true }
//   ],
//   mode: 'history',
// });

new Vue({
  el: "#app",
  // router,
  render: (h) => h(App),
});

