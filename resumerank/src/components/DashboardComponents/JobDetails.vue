<template>
    <div id="container">
        <h1>{{ job.job_title }}</h1>
        <p>{{ job.date_posted }}</p>
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

                    if (responseData && responseData.response === 'Login successful.') {
                        console.log('im here')
                        this.$router.push({ name: 'dashboard', params: { user_id: responseData.user_data.id } });
                    } else {
                        this.message = 'LOGIN FAILED.';
                        setTimeout(() => { this.message = 'LOGIN'}, 2000);
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

        }
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
    margin-top: 15%;
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