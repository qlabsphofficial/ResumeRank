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
                    <h2>{{ user_data.firstname }} {{ user_data.middlename }} {{ user_data.lastname }}</h2>
                    <p>{{ user_data.email }}</p>
                </div>
            </div>

            <h4>My Information</h4>
            <div id="all-info">
                <p>Sample Notification</p>
                <p>Sample Notification</p>
                <p>Sample Notification</p>
                <p>Sample Notification</p>
                <p>Sample Notification</p>
                <p>Sample Notification</p>
                <p>Sample Notification</p>
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
</style>