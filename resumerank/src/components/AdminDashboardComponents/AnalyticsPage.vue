<template>
    <div id="user-modal-container" v-if="user_modal_visible">
        <div id="user-modal">
           <div id="user-modal-content">
                <h1>User Profile</h1>
                <hr>

                <div id="user-info">
                    <div id="profile-pic-container">
                        <div id="profile-picture">
                            <img src="" alt="No Image Provided">
                        </div>
                    </div>

                    <div v-if="!editing_state">
                        <h2></h2>
                        <h3>Contact Number: </h3>
                        <h3>Email: </h3>
                        <h3>Address: </h3>
                    </div>

                    <div v-if="editing_state">
                        <div class="modify-info">
                            <h3>First Name:</h3>
                            <input type="text" placeholder="Enter your first name..." v-model="first_name">
                        </div>

                        <div class="modify-info">
                            <h3>Middle Name:</h3>
                            <input type="text" placeholder="Enter your middle name..." v-model="middle_name">
                        </div>

                        <div class="modify-info">
                            <h3>Last Name:</h3>
                            <input type="text" placeholder="Enter your last name..." v-model="last_name">
                        </div>

                        <div class="modify-info">
                            <h3>Email Address:</h3>
                            <input type="text" placeholder="Enter your email address..." v-model="email">
                        </div>

                        <div class="modify-info">
                            <h3>Contact:</h3>
                            <input type="text" placeholder="Enter your contact number..." v-model="contact">
                        </div>

                        <div class="modify-info">
                            <h3>Address:</h3>
                            <input type="text" placeholder="Enter your address..." v-model="address">
                        </div>
                    </div>
                </div>

                <div id="user-modal-buttons">
                    <button @click="modifyValues">{{ this.editing_text }}</button>
                    <button @click="closeUserProfileModal">Cancel</button>
                </div>
           </div>
        </div>
    </div>

    <div id="container">
        <h1>Analytics</h1>
        <hr>

        <div id="users-container">
            
        </div>
    </div>
</template>

<script>
import current_address from '@/address';

export default {
    name: 'AnalyticsPage',
    props: {
        user_data: {}
    },
    methods: {
        async retrieve_users(){
            const response = await fetch(`${current_address}/show_users`);
            const data = await response.json();

            if (data.response == 'User Retrieval Success'){
                
                this.users = data.users;
                console.log(this.users);
            }
            else{
                console.log(`Request failed with status ${response.status}`);
            }
        },

        async viewUserProfile(user){
            this.user_modal_visible = true;
            this.first_name = user.firstname;
            this.middle_name = user.middlename;
            this.last_name = user.lastname;
            this.email = user.email;
            this.contact = user.contact_no;
            this.address = user.address;
        },

        closeUserProfileModal(){
            this.user_modal_visible = false;
            this.clearData();
        },

        modifyValues(){
            if (!this.editing_state){
                this.editing_text = 'Save';
                this.editing_state = true;
            }

            else {
                this.editing_text = 'Edit';
                this.editing_state = false;
                this.clearData();
            }
        },

        clearData(){
            this.first_name = '';
            this.middle_name = '';
            this.last_name = '';
            this.email = '';
            this.contact = '';
            this.address = '';
        }
    },
    data (){
        return {

        }
    },
    mounted() {
        this.retrieve_users();
    }
}
</script>

<style scoped lang="scss">
#user-modal-container {
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

#user-modal {
    height: 80vh;
    width: 50vw;
    border-radius: 15px;
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
}

#user-modal-content {
    height: 95%;
    width: 95%;
    text-align: left;
    overflow-y: scroll;

    .modify-info {
        width: 70%;
        margin-bottom: 1%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;

        input {
            width: 60%;
        }
    }

    #user-modal-buttons {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: flex-end;

        button {
            width: 30%;
            margin-left: 1%;
            margin-right: 1%;
        }
    }
}

#container {
    height: 100%;
    width: 100%;
    text-align: left;
}

#users-container {
    height: 95%;
    width: 100%;
    margin-top: 2.5%;
    display: flex;
    flex-direction: column; /* Adjusted to column for better scrolling control */
    overflow-y: auto; /* Allows vertical scrolling */
    overflow-x: hidden; /* Prevent horizontal scrolling if table overflows */

    table {
        width: 100%;
        border-collapse: collapse;
        background-color: white;
        border-radius: 10px;

        th, td {
            vertical-align: middle;
            padding: 4px 8px; /* Adjust padding for a tighter appearance */
        }

        th {
            background-color: #2c3e50;
            color: white;
            text-align: center;
        }

        tr {
            height: 30px; /* Set a fixed height for rows */
        }

        tr:nth-child(even) {
            background-color: #dde9fa;
        }

        button {
            height: 100%;
            width: 80%;
            margin: 0 auto; /* Center the button in the cell */
        }
    }
}
</style>