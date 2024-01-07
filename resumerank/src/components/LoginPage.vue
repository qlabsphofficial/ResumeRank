<template>
  <div id="container">
    <div id="login-container">
      <div id="image-container"></div>

      <div id="login-form-container">
        <div id="left-section">
          <h1>Login</h1>
          <p>ResumeRank Login Page</p>

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
            <button>Login</button>
            <p @click="this.$router.push('/register')">Not registered yet? Sign up here.</p>
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
  name: 'LoginPage',
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
  height: 40%;
  width: 100%;
  margin-bottom: 3%;

  input {
    margin-bottom: 5%;
    width: 90%;
    border: none;
    border-bottom: 1px solid #333;
    padding: 2%;
    box-sizing: border-box; /* Ensure consistent box sizing */
  }
}

#forgot-section {
  width: 100%;
  text-align: right;
  margin-bottom: 7.5%;
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
