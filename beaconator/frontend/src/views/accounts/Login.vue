<template>
  <div>
    <login-form @input="onSubmit" />
  </div>
</template>

<script>
import axios from 'axios';
import LoginForm from '../../components/forms/accounts/LoginForm';

export default {
  components: {
    LoginForm,
  },
  methods: {
    async onSubmit(form) {
      try {
        const { data } = await axios.post('http://127.0.0.1:8000/api/login', form);
        this.$store.dispatch('LOGIN_USER', data.token);
      } catch (error) {
        console.log(error);
      }
    },
  },
  head() {
    return {
      title: 'Login',
    };
  },
};
</script>
