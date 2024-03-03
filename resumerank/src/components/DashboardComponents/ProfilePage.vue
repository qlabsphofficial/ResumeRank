<template>
    <div id="container">
        <h1>Profile</h1>
        <p>Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>

        <div id="profile-container">
            <div id="left-panel">
                <div id="profile-main-details">
                    <div id="profile-edit">
                        <div id="profile-pic"></div>
                    </div>

                    <div id="profile-main-text">
                        <h2>{{ this.user_data.firstname }} {{ this.user_data.middlename }} {{ this.user_data.lastname }}</h2>
                        <p>{{ this.user_data.email }}</p>
                        <button>Edit Profile</button>
                    </div>
                </div>

                <div id="profile-info">
                    <label for="">First Name</label>
                    <input type="text" placeholder="First name...">

                    <label for="">Middle Name</label>
                    <input type="text" placeholder="Middle name...">

                    <label for="">Last Name</label>
                    <input type="text" placeholder="Last name...">

                    <label for="">Username</label>
                    <input type="text" placeholder="Username...">

                    <label for="">Password</label>
                    <input type="text" placeholder="Password...">
                </div>
            </div>

            <div id="right-panel">
                <h4>My Information</h4>
                <div id="all-info">
                    <h5>Education</h5>
                    <div class="info">
                        <p>Primary - {{ this.ed1 }}</p>
                        <p>Secondary - {{ this.ed2 }}</p>
                        <p>College / University - {{ this.ed3 }}</p>
                    </div>

                    <h5>Trainings</h5>
                    <div class="info">
                        <p>Training / Certification - {{ this.tr1 }}</p>
                        <p>Training / Certification - {{ this.tr2 }}</p>
                        <p>Training / Certification - {{ this.tr3 }}</p>
                    </div>

                    <h5>Achievements</h5>
                    <div class="info">
                        <p>Achievement - {{ this.ac1 }}</p>
                        <p>Achievement - {{ this.ac2 }}</p>
                        <p>Achievement - {{ this.ac3 }}</p>
                    </div>

                    <h5>Experience</h5>
                    <div class="info">
                        <p>Experience - {{ this.exp1 }}</p>
                        <p>Experience - {{ this.exp2 }}</p>
                        <p>Experience - {{ this.exp3 }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ProfilePage',
    props: {
        user_data: {}
    },
    methods: {
        async retrieve_resume_data(){
            const response = await fetch(`http://127.0.0.1:8000/retrieve_resume_data?user_id=${this.user_data.id}`);
            const data = await response.json();

            if (!response.ok){
                console.log('Failed.');
            }
            else{
                console.log(data.resume);
                this.ed1 = data.resume.ed_1
                this.ed2 = data.resume.ed_2
                this.ed3 = data.resume.ed_3
                this.tr1 = data.resume.training_1
                this.tr2 = data.resume.training_2
                this.tr3 = data.resume.training_3
                this.ac1 = data.resume.achievement_1
                this.ac2 = data.resume.achievement_2
                this.ac3 = data.resume.achievement_3
                this.exp1 = data.resume.experience_1
                this.exp2 = data.resume.experience_2
                this.exp3 = data.resume.experience_3
            }            
        }
    },
    data (){
        return {
            ed1: '',
            ed2: '',
            ed3: '',
            tr1: '',
            tr2: '',
            tr3: '',
            ac1: '',
            ac2: '',
            ac3: '',
            exp1: '',
            exp2: '',
            exp3: '',
        }
    },
    mounted() {
        this.retrieve_resume_data();
    },
}
</script>

<style scoped lang="scss">
#container {
    height: 100%;
    width: 100%;
    text-align: left;
}

#profile-container {
    height: 85%;
    width: 100%;
    margin-top: 3%;
    display: flex;
    flex-direction: row;
}

#profile-main-details {
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    margin-bottom: 5%;
}

#profile-edit {
    width: 10%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-right: 5%;

    button {
        margin-top: 15%;
        padding: 10%;
        border-radius: 15px;
        background-color: #2984CE;
        color: white;
        border: 1px solid transparent;
    }
}

#profile-main-text {
    margin-left: 15%;
    width: 80%;
}

#profile-info {
    display: flex;
    flex-direction: column;
    height: 40%;
    width: 100%;

    input {
        margin-top: 1%;
        margin-bottom: 3%;
        height: 4vh;
        width: 90%;
        border: none;
        border-radius: 15px;
        background-color: #DCE5EA;
        padding: 2%;
        box-sizing: border-box; /* Ensure consistent box sizing */
    }
}

#left-panel {
    height: 90%;
    width: 40%;
}

#right-panel {
    height: 90%;
    width: 60%;
}

#profile-pic {
    height: 100px;
    width: 100px;
    border: 1px solid black;
    border-radius: 150px;
}

#all-info {
    height: 90%;
    overflow-y: scroll;
}

#all-info::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#all-info::-webkit-scrollbar-thumb {
    background-color: #2984CE;
    border-radius: 15px;
}
</style>