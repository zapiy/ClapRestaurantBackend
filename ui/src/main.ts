import { createApp } from "vue";
import App from "./App.vue";
import { router, store } from "@/defines";
import "@/globals/global.scss";

import mdiVue from "mdi-vue/v3";
import * as mdijs from "@mdi/js";

const app = createApp(App);

String.prototype.toTitleCase = function () {
  return this.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
};
app.config.globalProperties.$window = window;
app.config.globalProperties.$store = store;

app
  .use(mdiVue, {
    icons: mdijs,
  })
  .use(router)
  .mount("#app");
