<template>
    <div id="main-container">
        <div id="navbar">
            <div id="navbar-top">
                <img src="@/assets/icons/ResumeRankLogo2.png" height="50%" width="25%">
                <h2>ResumeRank</h2>
            </div>

            <div id="navbar-links">
                <div class="link">
                    <img src="@/assets/icons/icons8-home-24.png" height="30px" width="30px">
                    <a @click="changeComponent('DashboardContent')" class="nav-link">Dashboard</a>
                </div>

                <div class="link">
                    <img src="@/assets/icons/icons8-notification-48.png" height="30px" width="30px">
                    <a @click="changeComponent('NotificationPage')" class="nav-link">Notifications</a>
                </div>

                <div class="link">
                    <img src="@/assets/icons/icons8-person-24.png" height="30px" width="30px">
                    <a @click="changeComponent('ProfilePage')" class="nav-link">Profile</a>
                </div>

                <div class="link">
                    <img src="@/assets/icons/icons8-edit-file-24.png" height="30px" width="30px">
                    <a @click="changeComponent('ResumePage')" class="nav-link">My Resume</a>
                </div>

                <div class="link">
                    <img src="@/assets/icons/icons8-briefcase-48.png" height="30px" width="30px">
                    <a @click="changeComponent('JobPostings')" class="nav-link">Job Postings</a>
                </div>
            </div>

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
    justify-content: space-evenly;
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

#navbar-top {
    text-align: center;
    width: 100%;
    margin-bottom: 5%;
}

#navbar-links {
    display: flex;
    flex-direction: column;
    width: 70%;
    padding-left: 30%;
    text-align: left;
}

.link {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-bottom: 5%;

    a {
        margin-left: 5%;
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
    height: 78%;
    width: 85%;
    padding: 5%;
    padding-top: 2%;
    background-color: white;
    border-radius: 15px;
    box-shadow: 2px 2px 2px #AEAEAE;
}
</style>