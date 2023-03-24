<template>
  <div class="content">
    <div class="block-center" @keyup.enter.prevent="sendAuth">
      <p>Логин</p>
      <input type="text" name="login" v-model="user_form.username">
      <p>Пароль</p>
      <input type="password" name="password" v-model="user_form.password">
      <button type="button" @click.prevent="sendAuth" @keyup.enter="sendAuth">Login</button>
      <p class="error-message" v-if="show_error">Неверный логин/пароль</p>
    </div>
  </div>
</template>

<script>
import TokenService from "src/services/TokenService";


export default {
  name: "LoginPage",
  setup(){

  },
  data() {
    return {
      show_error: false,
      user_form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    sendAuth() {
      TokenService.sendAuth(this.user_form).catch(errors => {
        this.show_error = true;
        return Promise.reject(errors);
      }).then(response => {
        this.$router.push({name: 'Description'});
      });
    }
  }
}
</script>

<style scoped>
.content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
}

</style>
