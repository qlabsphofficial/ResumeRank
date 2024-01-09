<template>
    <div id="container">
        <h1>Job Postings</h1>

        <div id="jobs">
            <div id="all-jobs">
                <div class="job" v-for="job in all_jobs" :key="job">
                    <h2>{{ job.job_title }}</h2>
                    <p>{{ job.date_posted }}</p>
                    <p>{{ job.description }}</p>
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

#all-jobs {
    display: flex;
    flex-direction: row;
}

.job {
    height: 15vh;
    width: 27%;
    margin: 1%;
    box-shadow: 2px 2px 2px 2px #AEAEAE;
    background-color: white;
    border-radius: 15px;
    padding: 3%;
    transition: .4s;
}
.job:hover {
    margin-top: 0;
}
</style>