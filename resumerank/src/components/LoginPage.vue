<template>
  <div id="container">
    <div id="login-container">
      <div id="image-container"></div>

      <div id="login-form-container">
        <div id="left-section">
          <img src="@/assets/icons/login-icon.webp" height="80%" width="80%">
        </div>

        <div id="right-section">
          <div id="right-section-hero">
            <img src="@/assets/icons/ResumeRankLogo3.png" height="10%" width="10%">
            <h1>ResumeRank</h1>
          </div>

          <div id="login-form">
            <h4>Username</h4>
            <input type="text" placeholder="Enter your username..." v-model="username">

            <h4>Password</h4>
            <input type="password" placeholder="Enter your password..." v-model="password">
          </div>

          <div id="forgot-section">
            <a href="">Forgot Password?</a>
          </div>

          <div id="button-container">
            <button @click="login()">Login</button>
            <p @click="this.$router.push('/register')">Don't have an account? <span id="sign-up-cta">Sign up.</span></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  methods: {
    async login() {
      try {
          const response = await fetch(`http://127.0.0.1:8000/login?username=${this.username}&password=${this.password}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          }
          });

          console.log('test works');

          if (response.ok) {
              const responseData = await response.json();

              if (responseData && responseData.response === 'Login successful.') {
                  console.log('im here')
                  this.$router.push({ name: 'dashboard', params: { user_id: responseData.user_data.id } });
              } else {
                  this.message = 'LOGIN FAILED.';
                  setTimeout(() => { this.message = 'LOGIN'}, 2000);
              }
          } else {
              console.log('Login Failed. Status:', response.status);
          }
      } catch (error) {
          console.error('An error occurred during login:', error.message);
      }
    }
  },
  data() {
    return {
      username: '',
      password: ''
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

  h1 {
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
  width: 75%;
  border-radius: 15px;
  box-shadow: 2px 2px 2px 2px #DDD;
}

#left-section {
  flex: 60%;
  flex-grow: 1;
  display: flex;
  padding: 2%;
  align-items: center;
  justify-content: center;
  background-color: white;
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
}

#right-section {
  flex: 40%;
  flex-grow: 1;
  text-align: left;
  background-color: white;
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  padding: 2%;
  align-items: center;
  justify-content: center;

  h1 {
    color: black;
    margin-left: 5%;
  }
}

#right-section-hero {
  margin-top: 15%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
}

#login-form {
  margin-top: 10%;
  height: 30%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
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

#forgot-section {
  width: 100%;
  text-align: left;
  margin-bottom: 10%;

  a {
    text-decoration: none;
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

#sign-up-cta {
  color: #6FBEE7;
  transition: .4s;
}

#sign-up-cta:hover {
  color: black;
  text-decoration: underline;
}
</style>
