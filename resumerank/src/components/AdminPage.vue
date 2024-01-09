<template>
    <div id="main-container">
        <div id="navbar">
            <a @click="changeComponent('DashboardContent')" class="nav-link">Dashboard</a>
            <a @click="changeComponent('NotificationPage')" class="nav-link">Job Postings</a>

            <a @click="this.$router.push('/login')" class="nav-link" id="sign-out">Sign Out</a>
        </div>

        <div id="main-content">
            <div id="main-content-container">
                <component :is="currentComponent"></component>
            </div>
        </div>
    </div>
</template>

<script>
import DashboardContent from './DashboardComponents/DashboardContent.vue';
import NotificationPage from './DashboardComponents/NotificationPage.vue';
import ProfilePage from './DashboardComponents/ProfilePage.vue';

export default {
    name: 'DashboardPage',
    components: {
        DashboardContent,
        NotificationPage,
        ProfilePage
    },
    methods: {
        changeComponent(componentName){
            this.currentComponent = componentName;
        }
    },
    data (){
        return {
            currentComponent: ProfilePage
        }
    },
    mounted(){
        this.changeComponent('DashboardContent');
    }
}
</script>

<style scoped lang="scss">
#main-container {
    position: absolute;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    background-color: #2984CE;
    display: flex;
    flex-direction: row;
}

#navbar {
    height: 100%;
    width: 20%;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: left;

    a {
        color: white;
        text-decoration: none;
        margin-top: 5%;
        margin-bottom: 5%;
        text-align: left;
    }
}

#main-content {
    height: 100%;
    width: 80%;
    display: flex;
    justify-content: center;
    align-items: center;
}

#main-content-container {
    height: 75%;
    width: 85%;
    padding: 5%;
    background-color: #F5F5F5;
    border-radius: 15px;
    box-shadow: 2px 2px 2px #AEAEAE;
}
</style>