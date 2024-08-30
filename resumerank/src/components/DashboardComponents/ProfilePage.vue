<template>
    <div id="edit-container" v-if="this.profile_edit_permission">
        <div id="edit-modal">
            <h3>Edit Profile Information</h3>

            <div id="profile-info">
                <label for="">First Name</label>
                <input type="text" v-model="this.firstname" placeholder="First name...">
    
                <label for="">Middle Name</label>
                <input type="text" v-model="this.middlename" placeholder="Middle name...">
    
                <label for="">Last Name</label>
                <input type="text" v-model="this.lastname" placeholder="Last name...">
    
                <label for="">Email</label>
                <input type="email" v-model="this.email" placeholder="Email...">
    
                <label for="">Password</label>
                <input type="password" v-model="this.password" placeholder="Password...">
            </div>
    
            <div id="edit-profile-buttons">
                <button @click="saveNewInfo()">Save</button>
                <button @click="stopModification()">Cancel</button>
            </div>
        </div>
    </div>

    <div id="container" class="fade-in-top">
        <h1>Profile</h1>
        <p>General User Information / Resume Data</p>

        <div id="profile-container">
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

                    <div id="profile-edit-buttons">
                        <button @click="modifyUserInfo()">Edit Profile</button>
                        <button @click="export_resume_to_word()">Export to PDF</button>
                    </div>
                </div>
            </div>

            <div class="section-header" style="margin-top: 1.5%;">           
                <img src="@/assets/icons/icons8-summary-58.png" height="24px" width="24px">  
                <h3>Summary</h3>
            </div>
            <p>{{ this.summary }}</p>

            <div class="section-header" style="margin-top: 3%;">           
                <img src="@/assets/icons/icons8-education-24.png" height="24px" width="24px">  
                <h3>Education</h3>
            </div>

            <div class="education">
                <h4>Primary</h4>
                <p>{{ this.ed1 }}</p>

                <h4>Secondary</h4>
                <p>{{ this.ed2 }}</p>

                <h4>College / University</h4>
                <p>{{ this.ed3 }}</p>
            </div>

            <div class="section-header" style="margin-top: 3%;">
                <img src="@/assets/icons/icons8-certificate-50.png" height="24px" width="24px">  
                <h3>Trainings and Certifications</h3>
            </div>
            
            <div class="info">
                <table>
                    <tr>
                        <th>Certification</th>
                        <th>Certifier / Training Center</th>
                        <th>Date Issued</th>
                    </tr>

                    <tr v-for="certification of certifications" :key="certification">
                        <td>{{ certification.title }}</td>
                        <td>{{ certification.training_center }}</td>
                        <td>{{ certification.date }}</td>
                    </tr>
                </table>
            </div>


            <div class="section-header" style="margin-top: 3%;">
                <img src="@/assets/icons/icons8-work-50.png" height="24px" width="24px">  
                <h3>Work Experience</h3>
            </div>

            <div style="margin-top: 3%;">
                <div v-for="experience of experiences" :key="experience" class="experience">
                    <div class="exp-left">
                        <p>{{ experience.tenure_start }}</p>
                        <div class="divider"></div>
                        <p v-if="experience.tenure_end">{{ experience.tenure_end }}</p>
                        <p v-else>Current</p>
                    </div>

                    <div class="exp-right">
                        <h4>{{ experience.job_title }}</h4>
                        <p>{{ experience.company }}</p>
                    </div>
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
                this.summary = data.resume.summary;
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
                a.download = 'Resume.pdf';
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            }
        },

        modifyUserInfo(){
            this.profile_edit_permission = true;
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
            this.profile_edit_permission = false;
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
            summary: '',
            ed1: '',
            ed2: '',
            ed3: '',
            tr1: '',
            tr2: '',
            tr3: '',
            profile_edit_permission: false,
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
@import '@/assets/global/styles.scss';

#edit-container {
    height: 100vh;
    width: 100vw;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba($color: #000000, $alpha: .6);
    z-index: 10;
}

#edit-modal {
    height: 70%;
    width: 40%;
    padding: 2%;
    background-color: white;
    border-radius: 15px;
    text-align: left;

    #profile-info {
        display: flex;
        flex-direction: column;
        height: 70%;
        width: 100%;
        margin-top: 5%;

        label {
            font-weight: bold;
        }
    
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
}

#container {
    height: 100%;
    width: 100%;
    text-align: left;
}

#profile-container {
    height: 81%;
    width: 96%;
    padding: 2%;
    margin-top: 3%;
    display: flex;
    flex-direction: column;
    overflow-y: scroll;
}

#profile-main-details {
    display: flex;
    flex-direction: row;
    align-items: center;
    height: 60%;
    width: 40%;
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
    margin-left: 12.5%;
    height: 100%;
    width: 80%;

    h2 {
        line-height: 0;
    }

    #profile-edit-buttons {
        width: 70%;
        margin-top: 3%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;

        button {
            width: 45%;
        }
    }
}

#edit-profile-buttons {
    display: flex;
    justify-content: space-evenly;
    margin-top: 10%;
}

.section-header {
    height: 9%;
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: start;

    h3 {
        margin-left: 2.5%;
    }
}

table {
    width: 100%;

    th, td {
        padding: 1%;
    }
}

.education {
    h4 {
        line-height: 0;
    }

    p {
        margin-bottom: 3%;
    }
}

.experience {
    height: 15%;
    display: flex;
    flex-direction: row;
    margin-bottom: 3%;

    h4 {
        line-height: 0;
    }

    .exp-left {
        height: 100%;
        width: 10%;
        display: flex;
        flex-direction: column;
        align-items: center;

        p {
            line-height: 0;
        }

        .divider {
            height: 75px;
            width: 5px;
            background-color: rgba($color: #000000, $alpha: .1);
        }
    }

    .exp-right {
        height: 100%;
        width: 60%;
        margin-left: 3%;
        display: flex;
        flex-direction: column;
        justify-content: center;

        h4 {
            line-height: 0;
        }

        p {
            line-height: 0;
        }
    }
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

#export-to-word {
    height: 10%;
    margin-top: 2%;
    display: flex;
    flex-direction: row-reverse;
}

#profile-container::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#profile-container::-webkit-scrollbar-thumb {
    background-color: #2984CE;
    border-radius: 15px;
}
</style>