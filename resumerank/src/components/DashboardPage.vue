<template>
    <div id="main-container">
        <div id="navbar">
            <a @click="changeComponent('DashboardContent')" class="nav-link">Dashboard</a>
            <a @click="changeComponent('NotificationPage')" class="nav-link">Notifications</a>
            <a @click="changeComponent('ProfilePage')" class="nav-link">Profile</a>
            <a @click="changeComponent('ResumePage')" class="nav-link">My Resume</a>
            <a @click="changeComponent('JobPostings')" class="nav-link">Job Postings</a>

            <a @click="this.$router.push('/login')" class="nav-link" id="sign-out">Sign Out</a>
        </div>

        <div id="main-content">
            <div id="main-content-container">
                <component :is="currentComponent" :job="this.childData" :user_data="this.user_data" @send-job-data="handleJobData" />
            </div>
        </div>
    </div>
</template>

<script>
import DashboardContent from './DashboardComponents/DashboardContent.vue';
import NotificationPage from './DashboardComponents/NotificationPage.vue';
import ProfilePage from './DashboardComponents/ProfilePage.vue';
import JobPostings from './DashboardComponents/JobPostings.vue';
import ResumePage from './DashboardComponents/ResumePage.vue';
import JobDetails from './DashboardComponents/JobDetails.vue';

export default {
    name: 'DashboardPage',
    props: ['user_id'],
    components: {
        DashboardContent,
        NotificationPage,
        ProfilePage,
        JobPostings,
        ResumePage,
        JobDetails
    },
    methods: {
        changeComponent(componentName){
            this.currentComponent = componentName;
        },

        async retrieve_dashboard_data(){
            const response = await fetch(`http://127.0.0.1:8000/retrieve_user_data?user_id=${this.user_id}`);
            const data = await response.json();

            if (!response.ok){
                console.log('Failed.');
            }
            else{
                this.user_data = data.payload.user_data;
                console.log(this.user_data);
            }            
        },

        handleJobData(data){
            this.childData = data.job_data;
            console.log(this.childData);
            this.currentComponent = JobDetails;
        }
    },
    data (){
        return {
            currentComponent: ProfilePage,
            user_data: [],
            childData: {}
        }
    },
    mounted(){
        this.changeComponent('DashboardContent');
        this.retrieve_dashboard_data();
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