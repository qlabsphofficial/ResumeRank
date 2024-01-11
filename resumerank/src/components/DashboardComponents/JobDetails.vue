<template>
    <div id="container">
        <h1>{{ page_title }}</h1>
        <p>{{ job.date_posted.replace('T', ' ') }}</p>
        <p id="description">{{ job.description }}</p>

        <div id="actions">
            <button @click="apply()">Apply Now</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'JobDetails',
    props: {
        user_data: {},
        job: {}
    },
    methods: {
        async apply() {
            try {
                const response = await fetch(`https://resumerank.onrender.com/apply_to_job?user_id=${this.user_data.id}&job_id=${this.job.id}`, {
                method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                console.log('test works');

                if (response.ok) {
                    const responseData = await response.json();
                    console.log(responseData.response);

                    if (responseData && responseData.response === 'applied to job') {
                        this.page_title = 'Application Successful.';
                        setTimeout(() => { this.page_title = this.job.job_title }, 2000);
                    } else {
                        console.log('Error');
                    }
                } else {
                    console.log('Login Failed. Status:', response.status);
                }
            } catch (error) {
                console.error('An error occurred during login:', error.message);
            }
        }
    },
    data (){
        return {
            page_title: ''
        }
    },
    mounted() {
        this.page_title = this.job.job_title;
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
</style>