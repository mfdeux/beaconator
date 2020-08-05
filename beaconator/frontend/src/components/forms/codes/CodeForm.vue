<template>
  <div>
    <form @submit.prevent="onSubmit">
      <div>
        <label>Name</label>
        <form-input v-model="form.input.name" />
        <ul v-if="$v.form.input.name.$error" class="error">
          <li v-if="!$v.form.input.name.required">
            This field is required.
          </li>
        </ul>
      </div>

      <div class="mt-4">
        <label>Code</label>
        <form-input v-model="form.input.code" />
        <ul v-if="$v.form.input.code.$error" class="error">
          <li v-if="!$v.form.input.code.required">
            This field is required.
          </li>
        </ul>
      </div>
      <div class="mt-6"><label>Active</label><form-switch v-model="form.input.active" /></div>

      <div class="mt-6">
        <button type="submit">
          Save
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import formMixin from '../../../mixins/form';
import FormInput from '../inputs/FormInput';
import FormSwitch from '../inputs/FormSwitch';

export default {
  components: {
    FormInput,
    FormSwitch,
  },
  mixins: [formMixin],
  data: () => ({
    form: {
      input: {
        name: null,
        code: null,
        active: true,
      },
    },
  }),
  validations: {
    form: {
      input: {
        name: {
          required,
        },
        code: {
          required,
        },
      },
    },
  },
};
</script>
