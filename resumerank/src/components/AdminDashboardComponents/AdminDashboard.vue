<template>
    <div id="container">
        <h1>Admin Dashboard</h1>
        <hr>

        <div id="dashboard-news">
            <div id="jobs">
                <h3>Active Job Postings</h3>
                <div class="all-jobs">
                    <div class="job" v-for="active_job in active_jobs" :key="active_job" @click="sendDataToParent(active_job)">
                        <div class="credential-header"></div>

                        <div class="credential-details">
                            <h4>Active Job</h4>
                            <h3>{{ active_job.job_title }}</h3>

                            <p>Description {{ active_job.description.slice(0, 100) }}</p>
                            <p>Expire Date: {{ active_job.date_expired.slice(0, 10) }}</p>

                            <div class="remove-credential-container">
                                <button class="remove-credential-button" >View Job</button>
                            </div>
                        </div>
                    </div>
                </div>

                <h3>Inactive Job Postings</h3>
                <div class="all-jobs">
                    <div class="job" v-for="inactive_job in inactive_jobs" :key="inactive_job" @click="sendDataToParent(inactive_job)">
                        <div class="credential-header"></div>

                        <div class="credential-details">
                            <h4>Inactive Job</h4>
                            <h3>{{ inactive_job.job_title }}</h3>

                            <p>Description {{ inactive_job.description.slice(0, 100) }}</p>
                            <p>Expire Date: {{ inactive_job.date_expired.slice(0, 10) }}</p>

                            <div class="remove-credential-container">
                                <button class="remove-credential-button" >View Job</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import current_address from '@/address';

export default {
    name: 'DashboardContent',
    methods: {
        async retrieve_dashboard_data(){
            const active_response = await fetch(`${current_address}/show_active_jobs`);
            const active_data = await active_response.json();

            if (!active_response.ok){
                console.log('Failed.');
            }
            else{
                console.log(active_data.active_jobs);
                this.active_jobs = active_data.active_jobs;
            }     
            
            const inactive_response = await fetch(`${current_address}/show_inactive_jobs`);
            const inactive_data = await inactive_response.json();

            if (!inactive_response.ok){
                console.log('Failed.');
            }
            else{
                console.log(inactive_data.inactive_jobs);
                this.inactive_jobs = inactive_data.inactive_jobs;
            }   
        },

        sendDataToParent(job){
            this.$emit('send-job-data', { job_data: job });
        },
    },
    data (){
        return {
            active_jobs: [],
            inactive_jobs: []
        }
    },
    mounted() {
        this.retrieve_dashboard_data();
    },
}
</script>

<style scoped lang="scss">
#container {
    height: 100%;
    width: 100%;
    text-align: left;
}

#dashboard-info-container {
    display: flex;
    flex-direction: row;
    height: 10vh;
    width: 100%;
    margin-top: 5%;
}

.dashboard-info {
    height: 100%;
    width: 30%;
    margin-left: 2%;
    margin-right: 2%;
    padding: 2%;
    background-color: black;
    border-radius: 15px;
    box-shadow: 2px 2px 2px #AEAEAE;
    display: flex;
    flex-direction: row;
    align-items: center;

    h4, p {
        color: white;
    }
}

.dashboard-icon {
    height: 80px;
    width: 80px;
    border-radius: 150px;
    background-color: white;
}

.dashboard-info-detail {
    margin-left: 5%;
}

#dashboard-news {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: row;
    overflow-y: scroll;
}

#jobs {
    height: 100%;
    width: 100%;
}

.all-jobs {
    display: flex;
    justify-content: center;
    flex-direction: row;
    flex-wrap: wrap;
    margin-top: 1%;
    padding: 2%;
    overflow-y: scroll;
}

.job {
    height: 400px;
    width: 30%;
    background-color: white;
    margin: 1%;
    border-radius: 15px;
    box-shadow: 2px 2px 2px 2px #DFDFDF;

    .credential-header {
        height: 3%;
        width: 100%;
        border-top-left-radius: 30px;
        border-top-right-radius: 30px;
        background-color: #2c3e50;
    }

    .credential-details {
        padding: 5%;
    }

    .remove-credential-container {
        width: 100%;
        margin-top: 20%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .remove-credential-button {
        width: 60%;
        background-color: #DE3636;
        color: white;
        border: 1px solid transparent;
        border-radius: 15px;
        transition: .4s;
    }

    .remove-credential-button:hover {
        border: 1px solid #DE3636;
        background-color: transparent;
        color: #DE3636;
    }
}

#notifications {
    height: 100%;
    width: 30%;
    margin-left: 5%;
}

#all-notifs {
    height: 75%;
    width: 90%;
    overflow-y: scroll;
    margin-top: 3%;
    padding: 2%;
    padding-left: 8%;
    padding-right: 8%;
    border-radius: 15px;
    box-shadow: 2px 2px 2px 2px #AEAEAE;
    overflow-y: scroll;
}

#all-notifs::-webkit-scrollbar, #all-jobs::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#all-notifs::-webkit-scrollbar-thumb, #all-jobs::-webkit-scrollbar-thumb {
    background-color: #2984CE;
    border-radius: 15px;
}
</style>