import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home";
import Counter from "@/components/Counter";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home
    },
    {
      // Because default routing mode is "hash",
      // this route is reached via "/#/counter"
      // Routing mode can also be changed to "history" to fix this,
      // but app is reloaded more often
      path: "/counter",
      name: "Counter",
      component: Counter
    },
  ] // Add a new route here in Part 2
});
