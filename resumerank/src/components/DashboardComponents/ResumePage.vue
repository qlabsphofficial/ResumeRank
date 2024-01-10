<template>
    <div id="container">
        <h1>{{ title }}</h1>

        <div id="resume-fillup">
            <h3>Education</h3>
            <input type="text" placeholder="Enter your primary school..." v-model="this.ed1">
            <input type="text" placeholder="Enter your secondary school..." v-model="this.ed2">
            <input type="text" placeholder="Enter your college / university..." v-model="this.ed3">

            <h3>Trainings</h3>
            <input type="text" placeholder="Enter training received..." v-model="this.tr1">
            <input type="text" placeholder="Enter training received..." v-model="this.tr2">
            <input type="text" placeholder="Enter training received..." v-model="this.tr3">

            <h3>Achievements</h3>
            <input type="text" placeholder="Enter an achievement..." v-model="this.ac1">
            <input type="text" placeholder="Enter an achievement..." v-model="this.ac2">
            <input type="text" placeholder="Enter an achievement..." v-model="this.ac3">

            <h3>Experience</h3>
            <input type="text" placeholder="Enter your past experience..." v-model="this.exp1">
            <input type="text" placeholder="Enter your past experience..." v-model="this.exp2">
            <input type="text" placeholder="Enter your past experience..." v-model="this.exp3">

            <h3>About</h3>
            <input type="text" placeholder="Tell us about yourself..." v-model="this.summary">

            <h3>Reference</h3>
            <input type="text" placeholder="Enter a character reference..." v-model="this.cr1">
            <input type="text" placeholder="Enter a character reference..." v-model="this.cr2">
            <input type="text" placeholder="Enter a character reference..." v-model="this.cr3">

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
}

#notifications {
    height: 70%;
    width: 100%;
    margin-top: 3%;
}

#resume-fillup {
    height: 80%;
    margin-top: 1%;
    padding: 2%;
    border-radius: 15px;
    overflow-y: scroll;
}

input {
    display: block;
    height: 5vh;
    width: 40%;
    margin-top: 3%;
    margin-bottom: 3%;
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
</style>