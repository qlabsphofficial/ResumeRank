import { createRouter, createWebHistory } from 'vue-router';
import { createApp } from 'vue';
import App from './App.vue';
import LoginPage from './components/LoginPage.vue';
import RegisterPage from './components/RegisterPage.vue';
import DashboardPage from './components/DashboardPage.vue';
import AdminPage from './components/AdminPage.vue';

// Create the Vue app instance
const app = createApp(App);

// Create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: LoginPage },
    { path: '/register', component: RegisterPage },
    { path: '/dashboard/:user_id', component: DashboardPage, name: 'dashboard', props: true },
    { path: '/admin', component: AdminPage }
  ],
});

// Use the router with the app
app.use(router);

// Mount the app
app.mount('#app');