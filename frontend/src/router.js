import Vue from "vue";
import Router from "vue-router";
import SignUp from "./views/SignUp.vue";
import Login from "./views/SignIn.vue";
import Home from "./views/Home.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/register",
      name: "register",
      component: SignUp
    },
    {
      path: "/login",
      name: "login",
      component: Login
    },
    {
      path: "/home",
      name: "home",
      component: Home
    },
    { path: '/', redirect: '/home' },
    { path: '*', redirect: '/home' }
  ]
});
