<template>
    <div id="job-posting-modal-container" v-if="this.modal_visible">
        <div id="job-posting">
            <h2>Add Job Posting</h2>
            <hr>

            <div id="new-job-posting-form">
                <div class="form-input">
                    <h4>Title</h4>
                    <input type="text" placeholder="Enter title..." v-model="title">
                </div>
    
                <div class="form-input">
                    <h4>Job Title</h4>
                    <input type="text" placeholder="Enter job role..." v-model="jobTitle">
                </div>
    
                <div class="form-input">
                    <h4>Date Expired</h4>
                    <input type="date" placeholder="Enter date expired..." v-model="dateExpiration">
                </div>
    
                <div id="qualifications">
                    <h4>Qualifications</h4>
                    <div v-for="(qualification, index) in qualifications" :key="index" class="qualification">
                        <input type="text" v-model="qualifications[index]" placeholder="Enter qualification...">
                        <button @click="removeQualification(index)">Remove</button>
                    </div>

                    <button @click="addQualification('')">Add Qualification</button>
                </div>

                <div class="form-input">
                    <h4>Image (Optional)</h4>
                    <input type="file" accept="image/*" @change="onImageChange">
                </div>
            </div>

            <h4>Description</h4>
            <textarea rows="30" cols="100" placeholder="Tell us about yourself..." v-model="this.jobDescription"></textarea>

            <div class="modal-buttons">
                <button @click="submit_job_postings()">Add Job Posting</button>
                <button @click="closeJobPostingModal()">Cancel</button>
            </div>
        </div>
    </div>

    <div id="job-post-modal-info-container" v-if="post_modal_visible">
        <div id="job-post-modal-info">
            <h1>{{ modal_header }}</h1>
            <p>{{ modal_message }}</p>

            <button @click="closePostInfoModal()">Close</button>
        </div>
    </div>

    <div id="container" class="fade-in-top">
        <div id="top-container">
            <div id="top-left-container">
                <h1>Job Postings</h1>
                <p>Listed below are the active job postings.</p>
            </div>

            <div id="top-right-container" v-if="this.$route.path === '/admin'">
                <button @click="openJobPostingModal()">Create Job Posting</button>
            </div>
        </div>
        
        <div id="jobs" class="fade-in-left">
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

        async submit_job_postings() {
            let job_id = null;

            const response = await fetch(`${current_address}/create_job_posting`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'title': this.title,
                    'job_title': this.jobTitle,
                    'description': this.jobDescription,
                    'post_status': 1,
                    'qualifications': this.qualifications,
                    'date_expired': this.dateExpiration
                }),
            })

            if(response.ok){
                const responseData = await response.json();
                if (responseData.response == 'job created'){
                    this.retrieve_data();
                    this.closeJobPostingModal();
                    this.post_modal_visible = true;
                    this.modal_header = 'Job Posting Saved';
                    this.modal_message = 'Job Posting has been successfully Added.';
                    job_id = responseData.job_id;
                }
                else {
                    console.log('Failed');
                }
            }
            else {
                console.log(`Request failed with Status ${response.status}`);
            }
            
            // UPLOADING IMAGE FOR JOB POSTING
            console.log(this.image);
            console.log(job_id);
            
            if (this.image != null && job_id != null){
                this.uploadJobPicture(this.image, job_id);
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

        closePostInfoModal(){
            this.post_modal_visible = false;
        },

        addQualification(qualification_text) {
            this.qualifications.push(qualification_text);
        },
        removeQualification(index) {
            this.qualifications.splice(index, 1);
        },

        onImageChange(event) {
            const file = event.target.files[0];
            this.image = file;
        },

        async uploadJobPicture(file, job_id){
            try {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('job_id', job_id);

                const job_response = await fetch(`${current_address}/upload_job_picture`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'accept': 'application/json'
                    },
                });

                if (job_response.ok) {
                    console.log('Job picture uploaded successfully');
                } else {
                    console.error('Failed to upload job picture:', job_response.statusText);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
    },

    data (){
        return {
            all_jobs: [],

            modal_visible: false,
            title: '',
            jobTitle: '',
            jobDescription: '',
            qualifications: [''],
            dateExpiration: '',
            image: null,

            post_modal_visible: false,
            modal_header: '',
            modal_message: '',
        }
    },
    mounted(){
        this.retrieve_data();
    }
}
</script>

<style scoped lang="scss">
@import '@/assets/global/styles.scss';

#container {
    height: 100%;
    width: 100%;
    text-align: left;

    button {
        background-color: #2984CE;
        border: 1px solid transparent;
        transition: .4s;
    }

    button:hover {
        border: 1px solid #2984CE;
        background-color: transparent;
        color: #2984CE;
    }
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

    button {
        background-color: #2984CE;
        border: 1px solid transparent;
        transition: .4s;
    }

    button:hover {
        border: 1px solid #2984CE;
        background-color: transparent;
        color: #2984CE;
    }
}

#job-posting {
    height: 65vh;
    width: 40vw;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 2%;
    background-color: white;
    border-radius: 15px;

    hr {
        width: 100%;
        border: 1px solid #f1f1f1;
    }

    #new-job-posting-form {
        height: 100vh;
        width: 100%;
        padding: 1%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        overflow-y: scroll;

        .form-input {
            width: 100%;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
        }
    
        input {
            height: 3vh;
            width: 80%;
            border: none;
            border-bottom: 1px solid #AEAEAE;
            transition: .4s;
        }
    
        input:focus {
            border: none;
            outline: 2px solid #2984CE;
        }

        #qualifications {
            height: 80vh;
            width: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            .qualification {
                width: 100%;

                input {
                    width: 70%;
                    margin-right: 1%;
                }
    
                button {
                    width: 10%;
                }
            }
        }
    }

    .modal-buttons {
        margin-top: 5%;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
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

#job-post-modal-info-container {
    height: 100vh;
    width: 100vw;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, .4);
    z-index: 3;
}

#job-post-modal-info {
    height: 40vh;
    width: 35vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    background-color: white;
}

textarea {
    height: 1000px;
    border: 1px solid #CBCBCB;
    outline: none;
    padding: 2%;
    resize: none;
    margin-bottom: 5%;
    font-family: 'Montserrat', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
}

#new-job-posting-form::-webkit-scrollbar, #certification-modal::-webkit-scrollbar, #resume-fillup::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#new-job-posting-form::-webkit-scrollbar-thumb, #certification-modal::-webkit-scrollbar-thumb, #resume-fillup::-webkit-scrollbar-thumb {
    background-color: #2984CE;
    border-radius: 15px;
}
</style>