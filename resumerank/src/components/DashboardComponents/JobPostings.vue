<template>
    <div id="container">
        <h1>Job Postings</h1>

        <div id="jobs">
            <div id="all-jobs">
                <div class="job" v-for="job in all_jobs" :key="job" @click="sendDataToParent(job)">
                    <div class="job-top-section">
                        
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
export default {
    name: 'JobPostings',
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

    h3 {
        line-height: 0;
    }
}

.job-top-section {
    height: 60%;
    width: 100%;
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
</style>