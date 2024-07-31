<template>
    <div id="modal-container" v-if="this.modal_visible">
        <div id="modal">
            <h1>{{ modal_header }}</h1>
            <p>{{ modal_message }}</p>
            
            <div id="modal-btn" v-if="this.delete_post">
                <button @click="confirmDelete(job.id)">Confirm</button>
                <button @click="() => { this.modal_visible = false }">Close</button>
            </div>

            <div id="modal-btn-else" v-else>
                <button @click="() => { this.modal_visible = false }">Close</button>
            </div>
        </div>
    </div>

    <div id="container">
        <div id="post-top-section">
            <h1>{{ job.job_title }}</h1>
            <p>Date Posted: {{ job.date_posted }}</p>
        </div>

        <div id="post-middle-section">
            <button @click="deleteJob(this.job.id)">Delete Job</button>
            <button @click="setJobInactive(this.job.id)">Close Job</button>
        </div>

        <div id="post-bottom-section">
            <p>{{ job.description }}</p>
        </div>

        <h2>Top Applicants</h2>
        <div id="top-applicants">
            <h3 v-if="!top_applicants|| top_applicants.length === 0">No top applicants.</h3>
            
            <div id="all-top-applicants">
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

                        <h5>Certifications</h5>
                        <div class="info">
                            <li v-for="certification in top_applicant.certifications" :key="certification">{{ certification.title }}</li>
                        </div>

                        <h5>Experience</h5>
                        <div class="info">
                            <li v-for="experience in top_applicant.experiences" :key="experience">
                                {{ experience.job_title }} ({{ experience.tenure_start }} to {{ experience.tenure_end }})
                            </li>
                        </div>
                    </div>

                    <button class="contact-applicant-btn" @click="notifyApplicant(top_applicant.applicant.id)">Contact Applicant</button>
                </div>
            </div>
        </div>

        <h2>Applicants</h2>
        <div id="applicants">
            <h3 v-if="!top_applicants|| top_applicants.length === 0">No top applicants.</h3>
            
            <div v-for="applicant in applicants" :key="applicant.applicant.id" class="applicant">
                <h3>{{ applicant.applicant.firstname }} {{ applicant.applicant.middlename }} {{ applicant.applicant.lastname }}</h3>
                <p class="contact-info">{{ applicant.applicant.email }} - {{ applicant.applicant.contact_no }}</p>

                <div class="resume-details">
                    <h5>Education</h5>
                    <div class="info">
                        <li>Primary - {{ applicant.applicant_resume.ed_1 }}</li>
                        <li>Secondary - {{ applicant.applicant_resume.ed_2 }}</li>
                        <li>College / University - {{ applicant.applicant_resume.ed_3 }}</li>
                    </div>

                    <h5>Certifications</h5>
                    <div class="info">
                        <li v-for="certification in applicant.certifications" :key="certification.id">{{ certification.title }}</li>
                    </div>

                    <h5>Experience</h5>
                    <div class="info">
                        <li v-for="experience in applicant.experiences" :key="experience.id">
                            {{ experience.job_title }} ({{ experience.tenure_start }} to {{ experience.tenure_end }})
                        </li>
                    </div>
                </div>

                <button class="contact-applicant-btn" @click="notifyApplicant(applicant.applicant.id)">Contact Applicant</button>
            </div>
        </div>

    </div>
</template>

<script>
import current_address from '@/address';

export default {
    name: 'PostDetails',
    props: {
        job: {}
    },
    methods: {
        async get_analysis(){
            const response = await fetch(`${current_address}/analyze_resumes?job_id=${this.job.id}`);
            const data = await response.json();

            if (!response.ok){
                console.log('Failed.');
            }
            else{
                this.top_applicants = data.analysis;
                this.applicants = data.applicants;
            }            
        },

        async notifyApplicant(id){
            const response = await fetch(`${current_address}/create_notification?applicant_id=${id}&job_title=${this.job.job_title}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok){
                this.modal_header = 'Applicant Notified';
                this.modal_message = 'A notification has been sent to this applicant.';
                this.modal_visible = true;
            }
            else
            {
                this.modal_header = 'Failed to Notify Applicant';
                this.modal_message = 'The notification could not be sent. Contact your administrator for details.';
                this.modal_visible = false;
            } 
        },

        deleteJob() {
            this.modal_header = 'Confirm Deletion';
            this.modal_message = 'Are you sure you want to delete this item? This action cannot be undone.';
            this.modal_visible = true;
            this.delete_post = true;
        },

         async confirmDelete(id) {
            const response = await fetch(`${current_address}/delete_job_posting`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'id': id
                }),
            })

            const data = await response.json();
            
            if (data.response == 'job deleted'){
                this.modal_header = 'Job Deleted';
                this.modal_message = 'This job has been successfully deleted.';
                this.delete_post = true;
                
                setTimeout(() => {
                    this.$router.push('/admin');
                }, 2000)
            }
        },

        setJobInactive(id){
            const response = await fetch(`${current_address}/set_job_inactive`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'id': id
                }),
            })

            const data = await response.json();
            
            if (data.response == 'job deleted'){
                this.modal_header = 'Job Closed';
                this.modal_message = 'This job has been successfully rendered inactive.';
            }
        }
    },
    data (){
        return {
            top_applicants: [],
            applicants: [],

            modal_header: '',
            modal_message: '',
            modal_visible: false,
            delete_post: false,
            buttons_visible: true
        }
    },
    mounted(){
        this.get_analysis();
    }
}
</script>

<style scoped lang="scss">
#modal-container {
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, .4);
    z-index: 3;
}

#modal {
    height: 40vh;
    width: 35vw;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: white;
    border-radius: 15px;
}

#container {
    height: 100%;
    width: 95%;
    display: flex;
    flex-direction: column;
    padding-right: 5%;
    text-align: left;
    overflow-y: scroll;
}

#post-top-section {
    height: 20%;
    width: 100%;
}

#post-middle-section {
    height: 10%;
    width: 50%;
    padding-left: 50%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;

    button {
        width: 30%;
    }
}

#post-bottom-section {
    height: 20%;
    width: 100%;
    justify-content: center;
    align-items: center;
}

#modal-btn {
    height: 30%;
    width: 70%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;

    button {
        width: 40%;
    }
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
    margin-top: 3%;
}

#top-applicants, #applicants {
    height: 100%;
    width: 100%;
}

#all-top-applicants {
    height: 100%;
    overflow-y: scroll;
}

#container::-webkit-scrollbar, #all-top-applicants::-webkit-scrollbar, #all-jobs::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#container::-webkit-scrollbar-thumb, #all-top-applicants::-webkit-scrollbar-thumb, #all-jobs::-webkit-scrollbar-thumb {
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

.contact-info {
    color: #989898;
}
</style>