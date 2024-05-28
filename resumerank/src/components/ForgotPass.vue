<template>
  <div id="container">
    <div id="forgot-pass-container">
      <div id="forgot-pass-form-container">
          <div id="left-section">
              <div id="left-section-header">
                <img src="@/assets/icons/ResumeRankLogo3.png" height="10%" width="10%">
                <h1>ResumeRank</h1>
              </div>

              <div id="forgot-pass-form">
                  <h4>Username</h4>
                  <input type="text" placeholder="Enter your username..." v-model="username">

                  <h4>Password</h4>
                  <input type="password" placeholder="Enter your password..." v-model="password">

                  <h4>Confirm Password</h4>
                  <input type="password" placeholder="Confirm your password..." v-model="confirm">
              </div>

              <div id="button-container">
                  <button @click="register()">Submit</button>
                  <p @click="this.$router.push('/')">Return to Homepage</p>
              </div>
          </div>

          <div id="right-section">
            <img src="@/assets/icons/register-icon.jpg" height="100%" width="100%">
          </div>
      </div>
    </div>
  </div>
</template>

<script>
import current_address from '@/address';

export default {
  name: 'RegisterPage',
  methods: {
    async register(){
        const response = await fetch(`${current_address}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'username': this.username,
                'password': this.password,
                'confirm': this.confirm,
            }),
        })

        if(response.ok){
            const responseData = await response.json();
            console.log(responseData.response);

            if (responseData.response == 'Registration successful.'){
                this.$router.push('/');
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
  background-color: #2984CE;

  h1, h4 {
    color: #2984CE;
  }
}

#forgot-pass-form-container {
  display: flex;
  flex-direction: row;
  width: 100%;
}

#forgot-pass-container {
  display: flex;
  height: 70%;
  width: 65%;
  padding: 5%;
  background-color: white;
  border-radius: 15px;
  box-shadow: 2px 2px 2px 2px #DDD;
}

#left-section {
  flex: 45%;
  flex-grow: 1;
  text-align: left;
  background-color: white;
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
}

#left-section-header {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  h1 {
    color: black;
    font-size: 20pt;
  }
}

#right-section {
  flex: 55%;
  flex-grow: 1;
  text-align: center;
  color: white;
  background-color: white;
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  padding: 2%;
  display: flex;
  align-items: center;
  justify-content: center;
}

#forgot-pass-form {
  margin-top: 10%;
  height: 62%;
  width: 100%;
  margin-bottom: 5%;

  input {
    margin-bottom: 5%;
    height: 5vh;
    width: 90%;
    border: none;
    border-radius: 15px;
    background-color: #DCE5EA;
    padding: 2%;
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
  margin-bottom: 10%;

  a {
    text-decoration: none;
    color: black;
  }

  a:visited {
    color: black;
  }
}

#button-container {
  width: 100%;
  text-align: center;

  button {
    background-color: #6FBEE7;
    color: white;
    border: 1px solid transparent;
    border-radius: 15px;
    height: 5vh;
    width: 90%;
    margin-bottom: 3%;
    transition: 0.4s;
    font-weight: bold;
  }

  button:hover {
    border: 1px solid #6FBEE7;
    background-color: transparent;
    color: #6FBEE7;
  }
}
</style>
  