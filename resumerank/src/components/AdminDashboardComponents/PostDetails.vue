<template>
    <div id="container">
        <h1>{{ job.job_title }}</h1>
        <p>{{ job.date_posted }}</p>
        <p id="description">{{ job.description }}</p>

        <h2>Top Applicants</h2>
        <div id="top-applicants">
            <div v-for="top_applicant in top_applicants" :key="top_applicant">
                <h3>{{ top_applicant.firstname }} {{ top_applicant.middlename }} {{ top_applicant.lastname }}</h3>
                <p>{{ top_applicant.email }} - {{ top_applicant.contact }}</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PostDetails',
    props: {
        job: {}
    },
    methods: {
        async get_analysis(){
            const response = await fetch(`http://127.0.0.1:8000/analyze_resumes?job_id=${this.job.id}`);
            const data = await response.json();

            if (!response.ok){
                console.log('Failed.');
            }
            else{
                console.log(this.top_applicants);
                this.top_applicants = data.analysis;
            }            
        },
    },
    data (){
        return {
            top_applicants: []
        }
    },
    mounted(){
        this.get_analysis();
    }
}
</script>

<style scoped lang="scss">
#container {
    height: 100%;
    width: 100%;
    text-align: left;
}

#description {
    margin-top: 5%;
}

button {
    background-color: black;
    color: white;
    border: 1px solid transparent;
    border-radius: 15px;
    height: 5vh;
    width: 40%;
    margin-top: 5%;
    margin-bottom: 3%;
    transition: 0.4s;
    font-weight: bold;
}

button:hover {
    border: 1px solid black;
    background-color: transparent;
    color: black;
}

h2 {
    margin-top: 5%;
}

#top-applicants {
    height: 50%;
    width: 100%;
}
</style>