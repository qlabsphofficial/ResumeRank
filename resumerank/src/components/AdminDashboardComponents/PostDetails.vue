<template>
    <div id="container">
        <h1>{{ job.job_title }}</h1>
        <p>{{ job.date_posted }}</p>
        <p id="description">{{ job.description }}</p>

        <h2>Top Applicants</h2>
        <div id="top-applicants">
            <h3 v-if="this.top_applicants.length == 0">No top applicants.</h3>
            
            <div v-else id="all-top-applicants">
                <div v-for="top_applicant in top_applicants" :key="top_applicant" class="applicant">
                    <h3>{{ top_applicant.applicant.firstname }} {{ top_applicant.applicant.middlename }} {{ top_applicant.applicant.lastname }}</h3>
                    <p class="contact-info">{{ top_applicant.applicant.email }} - {{ top_applicant.applicant.contact_no }}</p>

                    <div class="resume-details">
                        <h5>Education</h5>
                        <div class="info">
                            <li>Primary - {{ top_applicant.applicant_resume.ed_1 }}</li>
                            <li>Secondary - {{ top_applicant.applicant_resume.ed_2 }}</li>
                            <li>College / University - {{ top_applicant.applicant_resume.ed_3 }}</li>
                        </div>

                        <h5>Achievements</h5>
                        <div class="info">
                            <li>{{ top_applicant.applicant_resume.achievement_1 }}</li>
                            <li>{{ top_applicant.applicant_resume.achievement_2 }}</li>
                            <li>{{ top_applicant.applicant_resume.achievement_3 }}</li>
                        </div>

                        <h5>Experience</h5>
                        <div class="info">
                            <li>{{ top_applicant.applicant_resume.experience_1 }}</li>
                            <li>{{ top_applicant.applicant_resume.experience_2 }}</li>
                            <li>{{ top_applicant.applicant_resume.experience_3 }}</li>
                        </div>
                    </div>
                </div>
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
                console.log('Printing top applicants...');
                this.top_applicants = data.analysis;
                console.log(this.top_applicants);
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

#all-top-applicants {
    height: 100%;
    overflow-y: scroll;
}

#all-top-applicants::-webkit-scrollbar, #all-jobs::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#all-top-applicants::-webkit-scrollbar-thumb, #all-jobs::-webkit-scrollbar-thumb {
    background-color: #2984CE;
    border-radius: 15px;
}

.applicant {
    margin-top: 2%;
    margin-bottom: 2%;
    padding: 1%;
    padding-left: 3%;
    padding-bottom: 5%;
    width: 90%;
    border-radius: 15px;
    box-shadow: 2px 2px 2px #AEAEAE;
    background-color: white;
    transition: .4s;
    color: black;

    h3 {
        line-height: 0;
    }
}

.applicant:hover {
    color: white;
    background-color: black;
}

.contact-info {
    color: #989898;
}
</style>