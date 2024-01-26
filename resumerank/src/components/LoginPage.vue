<template>
  <div id="container">
    <div id="login-container">
      <div id="image-container"></div>

      <div id="login-form-container">
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
          <p>Not registered yet? Sign up here.</p>
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
<<<<<<< Updated upstream
}

#login-container {
  height: 70%;
  width: 25%;
  padding: 2%;
=======
  background-color: #54ADE5;

  h1 {
    color: #54ADE5;
  }
}

#login-form-container {
  display: flex;
  flex-direction: row;
  width: 100%;
}

#login-container {
  display: flex;
  height: 85%;
  width: 80%;
>>>>>>> Stashed changes
  border-radius: 15px;
  box-shadow: 2px 2px 2px 2px #DDD;
  text-align: left;
}

#login-form {
  margin-top: 10%;
  height: 60%;

  input {
    margin-bottom: 5%;
    width: 90%;
    border: none;
    border-bottom: 1px solid #333;
    padding: 1%;
  }
}

#forgot-section {
  width: 100%;
  text-align: right;
  margin-top: 3%;
  margin-bottom: 7.5%;
}

#button-container {
  width: 100%;
  text-align: center;

  button {
<<<<<<< Updated upstream
    background-color: black;
=======
    background-color: #54ADE5;
>>>>>>> Stashed changes
    color: white;
    border: 1px solid transparent;
    border-radius: 15px;
    height: 5vh;
    width: 40%;
    margin-bottom: 3%;
    transition: .4s;
    font-weight: bold;
  }

  button:hover {
<<<<<<< Updated upstream
    border: 1px solid black;
=======
    border: 1px solid #54ADE5;
>>>>>>> Stashed changes
    background-color: transparent;
    color: black;
  }
}
<<<<<<< Updated upstream
=======

#sign-up-cta {
  color: #54ADE5;
  transition: .4s;
}

#sign-up-cta:hover {
  color: black;
  text-decoration: underline;
}
>>>>>>> Stashed changes
</style>
