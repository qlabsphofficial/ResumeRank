<template>
    <div id="main-container">
        <div id="navbar">
            <div id="navbar-header">
                <img src="@/assets/icons/ResumeRankLogo2_Inverted.png" height="25%" width="40%">
                <h2>ResumeRank</h2>
            </div>

            <div id="nav-links">
                <div class="link">
                    <img src="@/assets/icons/icons8-home-24.png" height="30px" width="30px">
                    <a @click="changeComponent('AdminDashboard')" class="nav-link">Dashboard</a>
                </div>

                <div class="link">
                    <img src="@/assets/icons/icons8-briefcase-48.png" height="30px" width="30px">
                    <a @click="changeComponent('JobPostings')" class="nav-link">Job Postings</a>
                </div>
            </div>

            <a @click="this.$router.push('/')" class="nav-link" id="sign-out">Sign Out</a>
        </div>

        <div id="main-content">
            <div id="main-content-container">
                <component :is="currentComponent" :job="this.job_data" @send-job-data="handleChildData" />
            </div>
        </div>
    </div>
</template>

<script>
import AdminDashboard from './AdminDashboardComponents/AdminDashboard.vue';
import JobPostings from './DashboardComponents/JobPostings.vue';
import PostDetails from './AdminDashboardComponents/PostDetails.vue';


export default {
    name: 'DashboardPage',
    components: {
        AdminDashboard,
        JobPostings,
        PostDetails
    },
    methods: {
        changeComponent(componentName){
            this.currentComponent = componentName;
        },  
        handleChildData(data){
            this.job_data = data.job_data;
            this.changeComponent('PostDetails');
        }
    },
    data (){
        return {
            currentComponent: 'AdminDashboard',
            job_data: {}
        }
    },
    mounted(){
        this.changeComponent('AdminDashboard');
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

#navbar-header {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

#nav-links {
    width: 75%;
    padding-left: 25%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.link {
    margin-top: 2%;
    margin-bottom: 2%;
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;

    img {
        margin-right: 5%;
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