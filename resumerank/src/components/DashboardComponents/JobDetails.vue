<template>
    <div id="modal-container" v-if="modal_visible">
        <div id="modal">
            <h1>{{ this.modal_header }}</h1>
            <p>{{ this.modal_message }}</p>

            <button @click="closeModal()">Close</button>
        </div>
    </div>

    <div id="container">
        <h1>{{ page_title }}</h1>
        <p>{{ job.date_posted.replace('T', ' ') }}</p>
        <p id="description">Date Posted: {{ job.description }}</p>

        <div id="actions">
            <button @click="apply()">Apply Now</button>
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
                    console.log(responseData.response);

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
            modal_message: ''
        }
    },
    mounted() {
        this.page_title = this.job.job_title;
    }
}
</script>

<style scoped lang="scss">
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
    width: 100%;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: center;
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
</style>