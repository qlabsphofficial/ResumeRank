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

            <h3>Trainings</h3>
            <div class="user-info-form">
                <div class="info-form">
                    <h5>Training / Seminar Attended</h5>
                    <input type="text" placeholder="Enter training received..." v-model="this.tr1">
                </div>

                <div class="info-form">
                    <h5>Training / Seminar Attended</h5>
                    <input type="text" placeholder="Enter training received..." v-model="this.tr2">
                </div>

                <div class="info-form">
                    <h5>Training / Seminar Attended</h5>
                    <input type="text" placeholder="Enter training received..." v-model="this.tr3">
                </div>
            </div>

            <h3>Achievements</h3>
            <div class="user-info-form">
                <div class="info-form">
                    <h5>Achievement</h5>
                    <input type="text" placeholder="Enter an achievement..." v-model="this.ac1">
                </div>

                <div class="info-form">
                    <h5>Achievement</h5>
                    <input type="text" placeholder="Enter an achievement..." v-model="this.ac2">
                </div>

                <div class="info-form">
                    <h5>Achievement</h5>
                    <input type="text" placeholder="Enter an achievement..." v-model="this.ac3">
                </div>
            </div>
            
            <h3>Experience</h3>
            <div class="user-info-form">
                <div class="info-form">
                    <h5>Work Experience</h5>
                    <input type="text" placeholder="Enter your past work experience..." v-model="this.exp1">
                </div>

                <div class="info-form">
                    <h5>Work Experience</h5>
                    <input type="text" placeholder="Enter your past work experience..." v-model="this.exp2">
                </div>

                <div class="info-form">
                    <h5>Work Experience</h5>
                    <input type="text" placeholder="Enter your past work experience..." v-model="this.exp3">
                </div>
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
          const response = await fetch('https://resumerank.onrender.com/submit_resume', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                'resume_owner': this.user_data.id,
                'ed_1': this.ed1,
                'ed_2': this.ed2,
                'ed_3': this.ed3,
                'training_1': this.tr1,
                'training_2': this.tr2,
                'training_3': this.tr3,
                'achievement_1': this.ac1,
                'achievement_2': this.ac2,
                'achievement_3': this.ac3,
                'experience_1': this.exp1,
                'experience_2': this.exp2,
                'experience_3': this.exp3,
                'summary': this.summary,
                'ref_1': this.cr1,
                'ref_2': this.cr2,
                'ref_3': this.cr3
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
            const response = await fetch(`https://resumerank.onrender.com/retrieve_resume_data?user_id=${this.user_data.id}`);
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
                this.summary = data.resume.summary
                this.cr1 = data.resume.ref_1
                this.cr2 = data.resume.ref_2
                this.cr3 = data.resume.ref_3
            }            
        }
    },
    data (){
        return {
            title: 'Resume',
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
            summary: '',
            cr1: '',
            cr2: '',
            cr3: ''
        }
    },
    created() {
        this.retrieve_resume_data();
    },
}
</script>

<style scoped lang="scss">
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

#resume-fillup::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#resume-fillup::-webkit-scrollbar-thumb {
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
</style>