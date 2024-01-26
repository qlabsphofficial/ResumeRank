<template>
    <div id="container">
        <h1>Dashboard</h1>

        <div id="dashboard-info-container">
            <div class="dashboard-info">
                <div class="dashboard-icon">
                    <img src="@/assets/icons/icons8-eye-60.png" height="50px" width="50px">
                </div>
                <div class="dashboard-info-detail">
                    <h2>0</h2>
                    <p>Profile Views</p>
                </div>
            </div>

            <div class="dashboard-info">
                <div class="dashboard-icon">
                    <img src="@/assets/icons/icons8-check-document-96.png" height="50px" width="50px">
                </div>
                <div class="dashboard-info-detail">
                    <h2>0</h2>
                    <p>Notifications</p>
                </div>
            </div>
        </div>

        <div id="dashboard-news">
            <div id="jobs">
                <h2>Available Job Postings</h2>

                <div id="all-jobs">
                    <div class="job" v-for="job in all_jobs" :key="job" @click="sendDataToParent(job)">
                        <div class="job-general-info">
                            <h4>{{ job.job_title }}</h4>
                            <p>{{ job.date_posted.slice(0, 10).replace(/-/g, '/') }}</p>
                        </div>
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
    height: 5vh;
    width: 100%;
    margin-top: 3%;
}

.dashboard-info {
    height: 100%;
    width: 30%;
    margin-left: 2%;
    margin-right: 2%;
    padding: 3%;
    background-color: #3B6EA5;
    border-radius: 50px;
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
    display: flex;
    justify-content: center;
    align-items: center;
}

.dashboard-info-detail {
    width: 50%;
    margin-left: 10%;
    text-align: center;

    h2 {
        font-size: 28pt;
        color: white;
        line-height: 0;
    }
}

#dashboard-news {
    height: 70%;
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
    overflow-y: scroll;
    background-color: white;
}

.job {
    height: 30%;
    padding-left: 3%;
    width: 92%;
    display: flex;
    flex-direction: column;
    justify-content: center;

    margin-top: 3%;
    margin-bottom: 3%;
    border-radius: 15px;
    background-color: #DCE5EA;

    h4, p {
        line-height: 0;
    }
}

.job-general-info {
    width: 97%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

#notifications {
    height: 100%;
    width: 30%;
    margin-left: 5%;
}

#all-notifs {
    height: 70%;
    width: 90%;
    overflow-y: scroll;
    margin-top: 3%;
    padding: 2%;
    padding-left: 8%;
    padding-right: 8%;
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
    background-color: #BAC1C7;
    border-radius: 15px;
}
</style>