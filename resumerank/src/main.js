import { createRouter, createWebHistory } from 'vue-router';
import { createApp } from 'vue';
import App from './App.vue';
import LoginPage from './components/LoginPage.vue';
import RegisterPage from './components/RegisterPage.vue';

// Create the Vue app instance
const app = createApp(App);

// Create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: LoginPage },
    { path: '/register', component: RegisterPage },
  ],
});

// Use the router with the app
app.use(router);

// Mount the app
app.mount('#app');