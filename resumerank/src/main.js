import { createRouter, createWebHistory } from 'vue-router';
import { createApp } from 'vue';
import App from './App.vue';
import LoginPage from './components/LoginPage.vue';
import RegisterPage from './components/RegisterPage.vue';
import DashboardPage from './components/DashboardPage.vue';
import AdminPage from './components/AdminPage.vue';
import ForgotPass from './components/ForgotPass.vue';

// Create the Vue app instance
const app = createApp(App);

// Create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: LoginPage },
    { path: '/administrator_page', component: AdminPage },
    { path: '/register', component: RegisterPage },
    { path: '/forgot_password', component: ForgotPass },
    { path: '/dashboard/:user_id', component: DashboardPage, name: 'dashboard', props: true },
  ],
});

// Use the router with the app
app.use(router);

// Mount the app
app.mount('#app');