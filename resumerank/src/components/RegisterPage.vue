<template>
    <div id="container">
      <div id="login-container">
        <div id="login-form-container">
            <div id="left-section">
                <h1>Register</h1>
                <p>Registration Page</p>

                <div id="login-form">
                    <h4>Username</h4>
                    <input type="text" placeholder="Enter your username..." v-model="username">

                    <h4>Password</h4>
                    <input type="password" placeholder="Enter your password..." v-model="password">

                    <h4>Confirm Password</h4>
                    <input type="password" placeholder="Confirm your password..." v-model="confirm">

                    <h4>First Name</h4>
                    <input type="text" placeholder="Enter your first name..." v-model="first_name">

                    <h4>Middle Name</h4>
                    <input type="text" placeholder="Enter your middle name..." v-model="middle_name">

                    <h4>Last Name</h4>
                    <input type="text" placeholder="Enter your last name..." v-model="last_name">

                    <h4>Email</h4>
                    <input type="email" placeholder="Enter your email..." v-model="email">

                    <h4>Contact Number</h4>
                    <input type="text" placeholder="Enter your contact number..." v-model="contact">

                    <h4>Address</h4>
                    <input type="text" placeholder="Enter your address..." v-model="address">
                </div>

                <div id="forgot-section">
                    <a href="">Forgot Password?</a>
                </div>

                <div id="button-container">
                    <button @click="register()">Register</button>
                    <p @click="this.$router.push('/login')">Already a user? Sign in.</p>
                </div>
            </div>

            <div id="right-section">
                <img src="@/assets/logo1.png" height="50%" width="50%">
                <h1>ResumeRank</h1>
                <p>Your Journey, Your Story, Your Success – ResumeRank Guides the Way.</p>
            </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'RegisterPage',
    methods: {
      async register(){
          // const response = await fetch('http://127.0.0.1:8000/register', {
          const response = await fetch('https://resumerank.onrender.com/register', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                  'username': this.username,
                  'password': this.password,
                  'confirm': this.confirm,
                  'firstname': this.first_name,
                  'middlename': this.middle_name,
                  'lastname': this.last_name,
                  'contact_no': this.contact,
                  'email': this.email,
                  'address': this.address
              }),
          })

          if(response.ok){
              const responseData = await response.json();
              console.log(responseData.response);

              if (responseData.response == 'Registration successful.'){
                  this.$router.push('/login');
              }
              else {
                  console.log('Failed');
              }
          }
          else {
              console.log(`Request failed with status ${response.status}`);
          }
        }
    },
    data() {
      return {
        username: '',
        password: '',
        confirm: '',
        first_name: '',
        middle_name: '',
        last_name: '',
        email: '',
        contact: '',
        address: ''
      }
    }
  }
  </script>
  
  <style scoped lang="scss">
  #container {
    position: absolute;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #EBEBEB;
  
    h1, h4 {
      color: #2984CE;
    }
  }
  
  #login-form-container {
    display: flex;
    flex-direction: row;
    width: 100%;
  }
  
  #login-container {
    display: flex;
    height: 80%;
    width: 65%;
    border-radius: 15px;
    box-shadow: 2px 2px 2px 2px #DDD;
  }
  
  #left-section {
    flex: 45%;
    flex-grow: 1;
    padding: 2%;
    text-align: left;
    background-color: white;
    border-top-left-radius: 15px;
    border-bottom-left-radius: 15px;
  }
  
  #right-section {
    flex: 55%;
    flex-grow: 1;
    text-align: center;
    color: white;
    background-color: #2984CE;
    border-top-right-radius: 15px;
    border-bottom-right-radius: 15px;
    padding: 2%;
    align-items: center;
    justify-content: center;
  
    h1 {
      color: white;
    }
  
    img {
      margin-top: 7.5%;
    }
  }
  
#login-form {
    margin-top: 10%;
    height: 50%;
    width: 100%;
    margin-bottom: 5%;
    overflow-y: scroll;
  
    input {
        margin-bottom: 5%;
        width: 90%;
        border: none;
        border-bottom: 1px solid #333;
        padding: 1%;
        box-sizing: border-box; /* Ensure consistent box sizing */
    }
}

#login-form::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#login-form::-webkit-scrollbar-thumb {
    background-color: #2984CE;
    border-radius: 15px;
}
  
#forgot-section {
    width: 100%;
    text-align: right;
    margin-bottom: 5%;
}
  
#button-container {
    width: 100%;
    text-align: center;
  
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
      border: 1px solid black;
      background-color: transparent;
      color: black;
    }
}
</style>
  