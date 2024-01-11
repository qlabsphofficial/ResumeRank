<template>
    <div id="container">
        <h1>Dashboard</h1>
        <p>Your Command Center for Data Insights.</p>

        <div id="dashboard-info-container">
            <div class="dashboard-info">
                <div class="dashboard-icon"></div>
                <div class="dashboard-info-detail">
                    <h4>0</h4>
                    <p>Profile Views</p>
                </div>
            </div>

            <div class="dashboard-info">
                <div class="dashboard-icon"></div>
                <div class="dashboard-info-detail">
                    <h4>0</h4>
                    <p>Notifications</p>
                </div>
            </div>

            <div class="dashboard-info">
                <div class="dashboard-icon"></div>
                <div class="dashboard-info-detail">
                    <h4>0</h4>
                    <p>Active Proposals</p>
                </div>
            </div>
        </div>

        <div id="dashboard-news">
            <div id="jobs">
                <h2>Available Job Postings</h2>

                <div id="all-jobs">
                    <div class="job" v-for="job in all_jobs" :key="job" @click="sendDataToParent(job)">
                        <h4>{{ job.job_title }}</h4>
                        <p>{{ job.description.slice(0, 80) }}...</p>
                    </div>
                </div>
            </div>

            <div id="notifications">
                <h2>Recent Notifications</h2>

                <div id="all-notifs">
                    <h5>No notifications.</h5>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DashboardContent',
    methods: {
        async retrieve_data(){
            const response = await fetch(`http://127.0.0.1:8000/show_jobs`);
            const data = await response.json();

            if (!response.ok){
                console.log('Failed.');
            }
            else{
                console.log(data.jobs);
                this.all_jobs = data.jobs;
            }            
        },
        sendDataToParent(job){
            this.$emit('send-job-data', { job_data: job });
        }
    },
    data (){
        return {
            all_jobs: []
        }
    },
    mounted() {
        this.retrieve_data();
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
    height: 50%;
    width: 100%;
    margin-top: 7.5%;
    display: flex;
    flex-direction: row;
}

#jobs {
    height: 100%;
    width: 65%;
}

#all-jobs {
    height: 70%;
    width: 100%;
    margin-top: 3%;
    padding: 2%;
    border-radius: 15px;
    box-shadow: 2px 2px 2px 2px #AEAEAE;
    overflow-y: scroll;
    background-color: white;
}

.job {
    margin-top: 5%;
    margin-bottom: 5%;

    h4, p {
        line-height: 0;
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
    background-color: white;
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