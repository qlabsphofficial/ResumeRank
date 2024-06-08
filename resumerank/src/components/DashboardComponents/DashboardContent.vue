<template>
    <div id="container">
        <h1>Dashboard</h1>

        <div id="dashboard-info-container">
            <div class="notifications" v-for="notification in notifications" :key="notification">
                <h4>{{ notification.message }}</h4>
            </div>
        </div>

        <div id="dashboard-news">
            <div id="jobs">
                <h2>Available Job Postings</h2>

                <div id="all-jobs">
                    <div class="job" v-for="job in all_jobs" :key="job" @click="sendDataToParent(job)">
                        <div class="job-info">
                            <h4>{{ job.job_title }}</h4>
                            <p>{{ job.date_posted.slice(0, 10) }}</p>
                        </div>
                        <p>{{ job.description.slice(0, 80) }}...</p>
                    </div>
                </div>
            </div>

            <div id="notifications">
                <h2>Recent Notifications</h2>

                <div id="all-notifs">
                    <h3 v-if="notifications.length === 0">No notifications.</h3>

                    <div class="notification" v-for="notification in notifications" :key="notification">
                        <h4>{{ notification.message }}</h4>
                        <p class="date-posted">{{ notification.date_posted }}</p>
                        <p v-if="notification.message === 'Application Reviewed'">The recruiter wants to move forward with your application.</p>
                        <p v-else>The recruiter has decided not to push through with your application.</p>
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
        async retrieve_data(){
            const jobs_response = await fetch(`${current_address}/show_jobs`);
            const jobs_data = await jobs_response.json();

            if (jobs_response.ok){
                this.all_jobs = jobs_data.jobs;
            }
            else {
                console.log('Retrieval of Jobs Failed.');
            }
            
            const notifs_response = await fetch(`${ current_address }/show_notifications?id=${ this.$route.params.user_id }`);
            const notifs_data = await notifs_response.json();

            console.log(notifs_data);

            if (notifs_response.ok) {
                this.notifications = notifs_data.notifications;
            }
            else {
                console.log('Retrieval of Notifications Failed.');
            }
        },

        sendDataToParent(job){
            this.$emit('send-job-data', { job_data: job });
        }
    },

    data (){
        return {
            all_jobs: [],
            notifications: []
        }
    },

    mounted() {
        this.retrieve_data();
    }
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
    margin-top: 3%;
    overflow-y: scroll;
}

.dashboard-info {
    height: 100%;
    width: 30%;
    margin-left: 2%;
    margin-right: 2%;
    padding: 2%;
    background-color: #3B6EA5;
    border-radius: 75px;
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
    padding: 2%;
    overflow-y: scroll;
}

.job {
    background-color: #EDF3F3;
    margin-top: 2%;
    margin-bottom: 2%;
    padding: 3%;
    border-radius: 15px;
    box-shadow: 2px 2px 2px #AEAEAE;
    transition: .4s;
}

.job:hover {
    transform: translateY(-10%);
}

.job-info {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
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
    overflow-y: scroll;
}

.notification {
    height: 50%;
    width: 90%;
    padding: 5%;
    background-color: #EDF3F3;
    border-radius: 15px;
    box-shadow: 2px 2px 2px #AEAEAE;
    transition: .4s;
}

.notification:hover {
    transform: translateY(-10%);
}

#all-notifs::-webkit-scrollbar, #all-jobs::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#all-notifs::-webkit-scrollbar-thumb, #all-jobs::-webkit-scrollbar-thumb {
    background-color: #B8C3C6;
    border-radius: 15px;
}
</style>