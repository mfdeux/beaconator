<template>
  <div>
    <form @submit.prevent="onSubmit">
      <div>
        <label>Password</label>
        <form-input
          v-model="form.input.password"
          type="password"
          autocomplete="current-password"
        />
        <ul
          v-if="$v.form.input.password.$error"
          class="error"
        >
          <li v-if="!$v.form.input.password.required">
            This field is required.
          </li>
        </ul>
      </div>

      <div class="mt-6">
        <button type="submit">
          Login
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import formMixin from '../../../mixins/form';
import FormInput from '../inputs/FormInput';

export default {
  components: {
    FormInput,
  },
  mixins: [formMixin],
  data: () => ({
    form: {
      input: {
        password: null,
      },
    },
  }),
  validations: {
    form: {
      input: {
        password: {
          required,
        },
      },
    },
  },
};
</script>
