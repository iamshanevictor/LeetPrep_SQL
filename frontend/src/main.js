import { createApp } from "vue";

import App from "./App.vue";
import router from "./router";
import { applyTheme, getStoredTheme } from "./services/themeStorage";
import "./assets/styles.css";

applyTheme(getStoredTheme());

createApp(App).use(router).mount("#app");
