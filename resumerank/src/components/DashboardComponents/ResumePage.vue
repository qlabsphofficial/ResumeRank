<template>
    <div id="container">
        <h1>{{ title }}</h1>
        <p>Please enter your resume details below.</p>

        <div id="resume-fillup">
            <h3>Education</h3>
            <div class="user-info-form">
                <div class="info-form">
                    <h5>Primary School Attended</h5>
                    <input type="text" placeholder="Enter your primary school..." v-model="this.ed1">
                </div>

                <div class="info-form">
                    <h5>Secondary School / High School Attended</h5>
                    <input type="text" placeholder="Enter your secondary school..." v-model="this.ed2">
                </div>

                <div class="info-form">
                    <h5>College / University Attended</h5>
                    <input type="text" placeholder="Enter your college / university..." v-model="this.ed3">
                </div>
            </div>

            <h3>Certifications</h3>
            <div class="credentials">
                <div id="certifications">
                    <h4 v-if="this.certifications.length == 0">No Certifications Included.</h4>
                </div>
                <button @click="openCertModal()">Add Certification</button>
            </div>
            
            <h3>Experience</h3>
            <div class="credentials">
                <div id="experiences">
                    <h4 v-if="this.experiences.length == 0">No Work Experience Included.</h4>
                </div>
                <button @click="openWorkModal()">Add Experience</button>
            </div>

            <h3>About</h3>
            <textarea rows="20" cols="130" placeholder="Tell us about yourself..." v-model="this.summary"></textarea>

            <h3>Reference</h3>
            <div class="user-info-form">
                <div class="info-form">
                    <h5>Character Reference</h5>
                    <input type="text" placeholder="Enter a character reference..." v-model="this.cr1">
                </div>

                <div class="info-form">
                    <h5>Character Reference</h5>
                    <input type="text" placeholder="Enter a character reference..." v-model="this.cr2">
                </div>

                <div class="info-form">
                    <h5>Character Reference</h5>
                    <input type="text" placeholder="Enter a character reference..." v-model="this.cr3">
                </div>
            </div>

            <button @click="submit_resume()">Save</button>
        </div>


        <div id="modal-container" v-if="modalOpen">
            <div id="certification-modal" v-if="certModalOpen">
                <h1>Add Certification</h1>

                <h5>Certification</h5>
                <input type="text" placeholder="Enter certification name..." id="cert-title" v-model="certTitle">

                <h5>Training Center</h5>
                <input type="text" placeholder="Enter training center name..." id="cert-title" v-model="certLocation">

                <h5>Date Issued</h5>
                <input type="date" placeholder="Enter issued date..." id="cert-title" v-model="certIssuedDate">

                <h5>Upload File</h5>
                <input type="file" placeholder="Upload certification proof..." id="cert-title" multiple="false" @change="handleFileUpload">

                <div class="buttons">
                    <button @click="addCertification()">Add Certification</button>
                    <button @click="closeCertModal()">Cancel</button>
                </div>
            </div>

            <div id="work-modal" v-if="workModalOpen">
                <h1>Add Work Experience</h1>

                <h5>Job Title</h5>
                <input type="text" placeholder="Enter certification name..." id="cert-title" v-model="jobTitle">

                <h5>Company Name</h5>
                <input type="text" placeholder="Enter training center name..." id="cert-title" v-model="jobCompany">

                <h5>Start of Service</h5>
                <input type="date" placeholder="Enter start date..." id="cert-title" v-model="jobYears">

                <h5>End of Service</h5>
                <input type="date" placeholder="Enter end date..." id="cert-title" v-model="jobYearEnd">

                <div class="buttons">
                    <button @click="addWorkExperience()">Add Work Experience</button>
                    <button @click="closeWorkModal()">Cancel</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ResumePage',
    props: {
        user_data: {}
    },
    methods: {
        async submit_resume(){
            console.log(this.certifications);

            const response = await fetch('http://127.0.0.1:8000/submit_resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'resume_owner': this.user_data.id,
                    'ed_1': this.ed1,
                    'ed_2': this.ed2,
                    'ed_3': this.ed3,
                    'summary': this.summary,
                    'experiences': this.experiences,
                    'certifications': this.certifications,
                    'ref_1': '',
                    'ref_2': '',
                    'ref_3': ''
                }),
            })

          if(response.ok){
              const responseData = await response.json();
              console.log(responseData.response);

              if (responseData.response == 'resume submitted'){
                this.title = 'Resume Updated';
                setTimeout(() => { this.title = 'Resume' }, 2000);
              }
              else {
                  console.log('Failed');
              }
          }
          else {
              console.log(`Request failed with status ${response.status}`);
          }
        },

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
                this.summary = data.resume.summary
                this.cr1 = data.resume.ref_1
                this.cr2 = data.resume.ref_2
                this.cr3 = data.resume.ref_3
            }            
        },

        openCertModal() {
            this.certModalOpen = true;
            this.modalOpen = true;
        },

        closeCertModal(){
            this.certModalOpen = false;
            this.modalOpen = false;
        },

        handleFileUpload(event){
            const files = event.target.files;

            for (let uploadedFile of files){
                this.certFileUpload = uploadedFile;
            }
        },
 
        addCertification() {
            let new_cert = {
                'title': this.certTitle,
                'training_center': this.certLocation,
                'date': this.certIssuedDate,
                'attachment': this.certFileUpload
            }
            
            let certificationDiv = document.createElement('div');
            certificationDiv.classList.add('credential');

            let certificationData = `
                <h3>Title: ${new_cert.title}</h3>
                <p>Training Center: ${new_cert.training_center}</p>
                <p>Date Issued: ${new_cert.date}</p>
                <button class="remove-credential-button">Remove Certification</button>
            `;

            certificationDiv.innerHTML = certificationData;

            let certificationsSection = document.getElementById('certifications');
            certificationsSection.appendChild(certificationDiv);

            this.certifications.push(new_cert);
            this.closeCertModal()
        },

        openWorkModal() {
            this.workModalOpen = true;
            this.modalOpen = true;
        },

        closeWorkModal(){
            this.workModalOpen = false;
            this.modalOpen = false;
        },

        addWorkExperience() {
            let newWorkXp = {
                'job_title': this.jobTitle,
                'company': this.jobCompany,
                'tenure_start': this.jobYears,
                'tenure_end': this.jobYearEnd
            }

            let newExperienceDiv = document.createElement('div');
            newExperienceDiv.classList.add('credential');

            let experienceData = `
                <h3>Title: ${newWorkXp.job_title}</h3>
                <p>Company: ${newWorkXp.company}</p>
                <p>Tenure Start: ${newWorkXp.tenure_start}</p>
                <p>Tenure End: ${newWorkXp.tenure_end}</p>
                <button class="remove-credential-button">Remove Experience</button>
            `;

            newExperienceDiv.innerHTML = experienceData;

            let experiencesSection = document.getElementById('experiences');
            experiencesSection.appendChild(newExperienceDiv);

            this.experiences.push(newWorkXp);
            this.closeWorkModal();
        },
    },
    data (){
        return {
            title: 'Resume',
            ed1: '',
            ed2: '',
            ed3: '',
            summary: '',

            certTitle: '',
            certLocation: '',
            certIssuedDate: '',
            certFileUpload: null,

            jobTitle: '',
            jobCompany: '',
            jobYears: '',
            jobYearEnd: '',

            certModalOpen: false,
            workModalOpen: false,
            modalOpen: false,

            certifications: [],
            experiences: [],
        }
    },
    created() {
        this.retrieve_resume_data();
    },
}
</script>

<style lang="scss">
#container {
    height: 100%;
    width: 100%;
    text-align: left;

    h1 {
        line-height: 0;
    }
}

#notifications {
    height: 70%;
    width: 100%;
    margin-top: 3%;
}

.credentials {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
}

.credential {
    height: 80%;
    width: 50%;
    padding: 3%;
    border-radius: 15px;
    box-shadow: 2px 2px 2px 2px #DFDFDF;
    
    .remove-credential-button {
        width: 40%;
        background-color: black;
        color: white;
        border: 1px solid transparent;
        border-radius: 15px;
        transition: .4s;
    }

    .remove-credential-button:hover {
        border: 1px solid black;
        background-color: transparent;
        color: #444444;
    }
}

#certifications {
    height: 90%;
    width: 100%;
    margin-bottom: 3%;
}

.certification {
    height: 30vh;
    width: 15vw;
    padding: 3%;
    box-shadow: 2px 2px 2px #444444;
    border: 1px solid black;
    border-radius: 15px;
}

#experiences {
    height: 90%;
    width: 100%;
    margin-bottom: 3%;
}

#resume-fillup {
    height: 80%;
    padding: 2%;
    margin-top: 3%;
    border-radius: 15px;
    overflow-y: scroll;

    h3 {
        font-weight: bold;
        color: #2984CE;
    }
}

#work-modal::-webkit-scrollbar, #certification-modal::-webkit-scrollbar, #resume-fillup::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#work-modal::-webkit-scrollbar-thumb, #certification-modal::-webkit-scrollbar-thumb, #resume-fillup::-webkit-scrollbar-thumb {
    background-color: #2984CE;
    border-radius: 15px;
}

.user-info-form {
    display: flex;
    flex-direction: row;
    margin-bottom: 5%;

    input {
        display: block;
        height: 5vh;
        width: 100%;
        margin: 1%;
        background-color: transparent;
        border: none;
        border-bottom: 1px solid black;
    }

    input:focus {
        outline: none;
    }
}


.info-form {
    width: 27%;
    margin-left: 2%;
    margin-right: 2%;

    h5 {
        line-height: 0;
        color: #2984CE;
    }
}

textarea {
    padding: 2%;
    resize: none;
    margin-bottom: 5%;
}


button {
    background-color: black;
    color: white;
    border: 1px solid transparent;
    border-radius: 15px;
    height: 5vh;
    width: 40%;
    margin-bottom: 3%;
    transition: 0.4s;
    font-weight: bold;
}

button:hover {
    color: black;
    background-color: transparent;
    border: 1px solid black;
}

#modal-container {
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    position: absolute;
    top: 0;
    left: 0;
    background-color: rgba($color: #444444, $alpha: 0.4);
    z-index: 10;
}

.buttons {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    margin-top: 5%;

    button {
        width: 30%;
        margin-right: 2%;
    }
}

#certification-modal {
    height: 50vh;
    width: 40vw;
    padding: 3%;
    background-color: white;
    border-radius: 15px;
    overflow-y: scroll;

    h1 {
        margin-bottom: 5%;
    }

    input {
        height: 3vh;
        width: 50%;
    }
}

#work-modal {
    height: 50vh;
    width: 40vw;
    padding: 3%;
    background-color: white;
    border-radius: 15px;
    overflow-y: scroll;

    h1 {
        margin-bottom: 5%;
    }

    input {
        height: 3vh;
        width: 50%;
    }
}
</style>