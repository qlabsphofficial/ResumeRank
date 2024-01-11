<template>
    <div id="container">
        <h1>Profile</h1>
        <p>Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>

        <div id="profile-container">
            <div id="profile-main-details">
                <div id="profile-edit">
                    <div id="profile-pic"></div>
                    <button>Edit Profile</button>
                </div>

                <div id="profile-main-text">
                    <h2>{{ this.user_data.firstname }} {{ this.user_data.middlename }} {{ this.user_data.lastname }}</h2>
                    <p>{{ this.user_data.email }}</p>
                </div>
            </div>

            <h4>My Information</h4>
            <div id="all-info">
                <h5>Education</h5>
                <div class="info">
                    <p>Primary: Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
                    <p>Secondary: Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
                    <p>College / University: Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
                </div>

                <h5>Trainings</h5>
                <div class="info">
                    <p>Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
                    <p>Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
                    <p>Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
                </div>

                <h5>Achievements</h5>
                <div class="info">
                    <p>Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
                    <p>Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
                    <p>Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
                </div>

                <h5>Experience</h5>
                <div class="info">
                    <p>Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
                    <p>Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
                    <p>Lorem ipsum dolor sit amet, consectetur adipscing elit.</p>
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

    },
    data (){

    }
}
</script>

<style scoped lang="scss">
#container {
    height: 100%;
    width: 100%;
    text-align: left;
}

#profile-container {
    height: 70%;
    width: 100%;
    margin-top: 3%;
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

#profile-pic {
    height: 100px;
    width: 100px;
    border: 1px solid black;
    border-radius: 150px;
}

#all-info {
    height: 60%;
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