<template>
    <div id="container">
        <h1>Profile</h1>
        <p>General User Information / Resume Data</p>

        <div id="profile-container">
            <div id="left-panel">
                <div id="profile-main-details">
                    <div id="profile-edit">
                        <div id="profile-pic" @click="triggerFileInput()">
                            <img v-if="profilePicture" :src="profilePicture" alt="Profile Picture" id="profile-image"/>
                            <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*" style="display: none;" />
                        </div>
                    </div>

                    <div id="profile-main-text">
                        <h2>{{ this.fn }} {{ this.mn }} {{ this.ln }}</h2>
                        <p>{{ this.user_email }}</p>


                        <button @click="modifyUserInfo()" v-if="this.profile_edit_permission">Edit Profile</button>
                    </div>
                </div>

                <div id="profile-info">
                    <label for="">First Name</label>
                    <input type="text" v-model="this.firstname" placeholder="First name..." :disabled="this.profile_edit_permission">

                    <label for="">Middle Name</label>
                    <input type="text" v-model="this.middlename" placeholder="Middle name..." :disabled="this.profile_edit_permission">

                    <label for="">Last Name</label>
                    <input type="text" v-model="this.lastname" placeholder="Last name..." :disabled="this.profile_edit_permission">

                    <label for="">Email</label>
                    <input type="email" v-model="this.email" placeholder="Email..." :disabled="this.profile_edit_permission">

                    <label for="">Password</label>
                    <input type="password" v-model="this.password" placeholder="Password..." :disabled="this.profile_edit_permission">
                </div>

                <div id="edit-profile-buttons" v-if="!this.profile_edit_permission">
                    <button @click="saveNewInfo()">Save</button>
                    <button @click="stopModification()">Cancel</button>
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

                    <h5>Certifications</h5>
                    <div class="info">
                        <li v-for="certification of certifications" :key="certification">{{ certification.title }}</li>
                    </div>

                    <h5>Experiences</h5>
                    <div class="info">
                        <li v-for="experience of experiences" :key="experience">{{ experience.job_title }}</li>
                    </div>
                </div>

                <div id="export-to-word">
                    <button @click="export_resume_to_word()">Export to Word</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import current_address from '@/address';

export default {
    name: 'ProfilePage',
    props: {
        user_data: {},
    },
    methods: {
        async retrieve_profile_info(){
            const response = await fetch(`${current_address}/retrieve_profile_info?id=${ this.$route.params.user_id }`);
            const data = await response.json();

            if (response.ok){
                this.fn = data.user.firstname;
                this.mn = data.user.middlename;
                this.ln = data.user.lastname;
                this.user_email = data.user.email;
            }
        },

        async retrieve_resume_data(){
            const response = await fetch(`${current_address}/retrieve_resume_data?user_id=${this.user_data.id}`);
            const data = await response.json();

            if (response.ok){
                this.ed1 = data.resume.ed_1;
                this.ed2 = data.resume.ed_2;
                this.ed3 = data.resume.ed_3;
                this.tr1 = data.resume.training_1;
                this.tr2 = data.resume.training_2;
                this.tr3 = data.resume.training_3;
                this.certifications = data.certifications;
                this.experiences = data.experiences;
            }
            else{
                console.log('Failed');
            }            
        },

        async export_resume_to_word(){
            const response = await fetch(`${current_address}/export_resume_to_word?user_id=${this.user_data.id}`);

            if (!response.ok){
                console.error('Failed to fetch the file:', response.statusText);
            }
            else{
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'Resume.docx';
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            }
        },

        modifyUserInfo(){
            this.profile_edit_permission = false;
        },

        async saveNewInfo(){
            const response = await fetch(`${current_address}/change_profile_info`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'id': this.$route.params.user_id,
                    'email': this.email,
                    'password': this.password,
                    'firstname': this.firstname,
                    'middlename': this.middlename,
                    'lastname': this.lastname
                }),
            });

            const data = await response.json();

            if (data.response == 'Successfully updated profile info'){
                this.email = '';
                this.password = '';
                this.firstname = '';
                this.middlename = '';
                this.lastname = '';

                this.retrieve_profile_info();
            }
            else{
                console.log('failed');
            }

            this.stopModification();
        },

        stopModification(){
            this.profile_edit_permission = true;
        },

        // PROFILE PICTURE UPLOADING
        async retrieve_profile_picture(){
            const pictureResponse = await fetch(`${current_address}/get_profile_picture/${this.user_data.id}`);

            if (pictureResponse.ok) {
                const pictureBlob = await pictureResponse.blob();
                const imageUrl = URL.createObjectURL(pictureBlob);

                // Update the profile picture
                this.profilePicture = imageUrl;
            } else {
                console.error('Failed to retrieve profile picture:', pictureResponse.statusText);
            }
        },

        triggerFileInput() {
            this.$refs.fileInput.click();
        },

        handleFileChange(event) {
            const file = event.target.files[0];
            if (file) {
                this.readImageFile(file);
            }
        },

        async readImageFile(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                this.profilePicture = e.target.result;
                this.uploadProfilePicture(file);
            };
            reader.readAsDataURL(file);
        },

        async uploadProfilePicture(file) {
            try {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('user_id', this.$route.params.user_id);

                const response = await fetch(`${current_address}/upload_profile_picture?user_id=${this.$route.params.user_id}`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'accept': 'application/json'
                    },
                });

                if (response.ok) {
                    console.log('Profile picture uploaded successfully');
                } else {
                    console.error('Failed to upload profile picture:', response.statusText);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
    },
    data (){
        return {
            fn: '',
            mn: '',
            ln: '',
            user_email: '',
            profilePicture: '',

            email: '',
            password: '',
            firstname: '',
            middlename: '',
            lastname: '',
            ed1: '',
            ed2: '',
            ed3: '',
            tr1: '',
            tr2: '',
            tr3: '',
            profile_edit_permission: true,
            certifications: [],
            experiences: []
        }
    },
    mounted() {
        this.retrieve_profile_info();
        this.retrieve_profile_picture();
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
    height: 60%;
    width: 100%;
    margin-bottom: 5%;
}

#profile-edit {
    height: 100%;
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
    height: 100%;
    width: 80%;
}

#profile-info {
    display: flex;
    flex-direction: column;
    height: 80%;
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

#edit-profile-buttons {
    display: flex;
    justify-content: space-evenly;
    margin-top: 5%;
}

#left-panel {
    height: 100%;
    width: 40%;
    display: flex;
    flex-direction: column;
}

#right-panel {
    height: 100%;
    width: 60%;
}

#profile-pic {
    height: 100px;
    width: 100px;
    border: 1px solid black;
    border-radius: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    cursor: pointer; /* Indicates clickability */
}

#profile-pic img {
    max-width: 100%;
    max-height: 100%;
    object-fit: cover;
}

#all-info {
    height: 80%;
    overflow-y: scroll;
}

#export-to-word {
    height: 10%;
    margin-top: 5%;
    display: flex;
    flex-direction: row-reverse;
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