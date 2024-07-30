<template>
    <div id="modal-container" v-if="modal_visible">
        <div id="modal">
            <h1>{{ this.modal_header }}</h1>
            <p>{{ this.modal_message }}</p>

            <button @click="closeModal()">Close</button>
        </div>
    </div>

    <div id="container" class="fade-in-top">
        <div id="main-job">
            <div id="job-image">
                <img :src="job_picture" alt="Job Picture">
            </div>

            <h2>{{ page_title }}</h2>
            <p>{{ job.date_posted.replace('T', ' ') }}</p>


            <div id="job-info">
                <div id="job-description-container">
                    <h3>Overview</h3>
                    <p id="description">{{ job.description }}</p>
                </div>

                <div id="job-description-container">
                    <h3>Job Requirements:</h3>
                    <li v-for="qualification of qualifications" :key="qualification">{{ qualification.description }}</li>
                </div>
                
                <div id="about-the-company">
                    <h3>About the Company</h3>
                    <p>
                        Anvaya Cove, located in Morong, Bataan, is a premier seaside residential community developed by Ayala Land Premier. 
                        Spanning approximately 470 hectares, this exclusive enclave seamlessly integrates the natural beauty of the surrounding landscape 
                        with a range of luxurious amenities and sustainable design practices.
                    </p>
                </div>
            </div>

            <div id="actions">
                <button @click="apply()">Apply Now</button>
            </div>
        </div>

        <div id="all-jobs">
            <h3>Active Jobs</h3>

            <div class="job" v-for="job in all_jobs" :key="job" @click="sendDataToParent(job)">
                <h4>{{ job.job_title }}</h4>
                <h5>{{ job.date_posted.slice(0, 10) }}</h5>
                <p class="description">{{ job.description.slice(0, 40) }}...</p>
                <hr>
            </div>
        </div>
    </div>
</template>

<script>
import current_address from '@/address';

export default {
    name: 'JobDetails',
    props: {
        user_data: {},
        job: {}
    },
    methods: {
        async retrieve_data(){
            const response = await fetch(`${current_address}/show_jobs`);
            const data = await response.json();

            if (!response.ok){
                console.log('Failed.');
            }
            else{
                this.all_jobs = data.jobs;
            }
            
            console.log(this.job);
            const applications_retrieval_response = await fetch(`${current_address}/retrieve_job_qualifications?id=${this.job.id}`);
            const applications_retrieval_data = await applications_retrieval_response.json();

            if (!response.ok){
                console.log('Failed.');
            }
            else{
                console.log(applications_retrieval_data.qualifications);
                this.qualifications = applications_retrieval_data.qualifications;
            }     
        },

        async get_job_picture(){
            const pictureResponse = await fetch(`${current_address}/get_job_picture/${this.job.id}`);

            if (pictureResponse.ok) {
                const pictureBlob = await pictureResponse.blob();
                const imageUrl = URL.createObjectURL(pictureBlob);

                this.job_picture = imageUrl;
            } else {
                console.error('Failed to retrieve profile picture:', pictureResponse.statusText);
            }
        },

        sendDataToParent(job){
            this.$emit('send-job-data', { job_data: job });
        },

        async apply() {
            try {
                const response = await fetch(`${current_address}/apply_to_job?user_id=${this.user_data.id}&job_id=${this.job.id}`, {
                method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                if (response.ok) {
                    const responseData = await response.json();

                    if (responseData && responseData.response === 'applied to job') {
                        this.modal_visible = true;
                        this.modal_header = 'Application Submitted';
                        this.modal_message = 'Your application is now pending for review.';
                    } else {
                        this.modal_visible = true;
                        this.modal_header = 'Application Submission Denied';
                        this.modal_message = 'You have already applied to this job.';
                    }
                }
            } catch (error) {
                console.error('An error occurred during application to job:', error.message);
            }
        },

        closeModal(){
            this.modal_visible = false;
        }
    },
    data (){
        return {
            page_title: '',

            modal_visible: false,
            modal_header: '',
            modal_message: '',

            all_jobs: [],
            qualifications: [],
            job_picture: ''
        }
    },
    mounted() {
        this.page_title = this.job.job_title;
        this.retrieve_data();
    }
}
</script>

<style scoped lang="scss">
@import '@/assets/global/styles.scss';

#modal-container {
    position: absolute;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, .4);
}

#modal {
    height: 40vh;
    width: 35vw;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border-radius: 15px;
    background-color: white;
}

#container {
    height: 100%;
    text-align: left;
    display: flex;
    flex-direction: row;
    justify-content: center;
}

#main-job {
    height: 100%;
    width: 70%;
    margin-right: 5%;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

#job-image {
    height: 15vh;
    width: 100%;
    background-color: #3B6EA5;
    border-radius: 15px;
}

#job-info {
    height: 40vh;
    overflow-y: scroll;
}

#job-description-container {
    width: 80%;
}

#about-the-company {
    margin-top: 5%;
}

#all-jobs {
    height: 96%;
    width: 20%;
    padding: 2%;
    background-color: white;
    border-radius: 15px;

    h3 {
        margin-bottom: 15%;
    }

    .job {
        margin-bottom: 15%;

        h4 {
            line-height: 0;
        }

        p {
            color: #8C8C8C;
            line-height: 1;
        }

        hr {
            display: block;
            height: 1px;
            border: 0;
            border-top: 1px solid #e6e6e6;
            margin: 1em 0;
            padding: 0;
        }
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
</style>