<template>
    <div id="job-posting-modal-container" v-if="this.modal_visible">
        <div id="job-posting">
            <h1>Add Job Posting</h1>
            <h5>Title</h5>
            <input type="text" placeholder="Enter title..." v-model="jobTitle">

            <h5>Job Title</h5>
            <input type="text" placeholder="Enter job role..." v-model="jobCompany">

            <h5>Description</h5>
            <textarea rows="10" cols="60" placeholder="Job description..." v-model="this.summary"></textarea>

            <h5>Date Expired</h5>
            <input type="date" placeholder="Enter date expired..." v-model="jobYears">

            <div class="buttons">
                <button @click="submit_experience()">Add Work Experience</button>
                <button @click="closeWorkModal()">Cancel</button>
            </div>
        </div>
    </div>

    <div id="container">
        <div id="top-container">
            <div id="top-left-container">
                <h1>Job Postings</h1>
                <p>Listed below are the active job postings.</p>
            </div>

            <div id="top-right-container">
                <button @click="openJobPostingModal()">Create Job Posting</button>
            </div>
        </div>
        
        <div id="jobs">
            <div id="all-jobs">
                <div class="job" v-for="job in all_jobs" :key="job" @click="sendDataToParent(job)">
                    <div class="job-top-section">
                        <img src="@/assets/icons/ResumeRankLogo3.png" height="100px" width="100px">
                    </div>

                    <div class="job-bottom-section">
                        <h3>{{ job.job_title }}</h3>
                        <p>{{ job.date_posted.slice(0, 10) }}</p>

                        <p class="description">{{ job.description.slice(0, 40) }}...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import current_address from '@/address';

export default {
    name: 'JobPostings',
    methods: {
        async retrieve_data(){
            const response = await fetch(`${current_address}/show_jobs`);
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
        },

        openJobPostingModal() {
            this.modal_visible = true;
        },

        closeJobPostingModal(){
            this.modal_visible = false;
        },
    },

    data (){
        return {
            all_jobs: [],

            modal_visible: false
        }
    },
    mounted(){
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

#notifications {
    height: 70%;
    width: 100%;
    margin-top: 3%;
}

#jobs {
    height: 80%;
    width: 96%;
    margin-top: 1%;
    padding: 2%;
    overflow-y: scroll;
}

#jobs::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#jobs::-webkit-scrollbar-thumb {
    background-color: #2984CE;
    border-radius: 15px;
}

#all-jobs {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
}

.job {
    height: 30vh;
    width: 30%;
    margin: 1%;
    padding-bottom: 5%;
    box-shadow: 2px 2px 2px 2px #AEAEAE;
    background-color: white;
    border-radius: 15px;
    transition: .4s;
    cursor: pointer;

    h3 {
        line-height: 0;
    }
}

.job-top-section {
    height: 60%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #2984CE;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
}

.job-bottom-section {
    height: 40%;
    width: 88%;
    padding: 5%;
}

.description {
    margin-top: 3%;
}

.job:hover {
    margin-top: 0;
}

#job-posting-modal-container {
    height: 100vh;
    width: 100vw;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, .4);
    z-index: 1;
}

#job-posting {
    height: 50vh;
    width: 40vw;
    padding: 3%;
    background-color: white;
    border-radius: 15px;
    overflow-y: scroll;

    input {
        height: 3vh;
        width: 50%;
    }
}

#top-container {
    height: 20%;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

#top-left-container {
    height: 100%;
    width: 70%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

#top-right-container {
    height: 100%;
    width: 40%;
    display: flex;
    flex-direction: column;
    align-items: end;
    justify-content: center;
}
</style>