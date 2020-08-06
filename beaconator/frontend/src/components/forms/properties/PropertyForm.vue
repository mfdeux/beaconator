<template>
  <div>
    <form @submit.prevent="onSubmit">
      <div>
        <label>Name</label>
        <form-input
          id="username"
          v-model="form.input.name"
          required
        />
        <ul
          v-if="$v.form.input.name.$error"
          class="error"
        >
          <li v-if="!$v.form.input.name.required">
            This field is required.
          </li>
        </ul>
      </div>
      <div class="mt-4">
        <label>Image</label>
        <form-select
          v-model="form.input.image"
          :options="form.options.images"
        />
      </div>
      <div class="mt-4">
        <p
          v-if="form.input.image === 'pixel'"
          class="text-sm text-gray-500"
        >
          A pixel is a 1x1 image, you will not be able to see it.
        </p>
        <img :src="`http://127.0.0.1:8000/api/other/images?type=${form.input.image}`">
      </div>
      <div class="mt-4">
        <label>Code</label>
        <form-select
          v-model="form.input.ga_code_id"
          :options="$store.state.options.codes"
        />
        <ul
          v-if="$v.form.input.ga_code_id.$error"
          class="error"
        >
          <li v-if="!$v.form.input.ga_code_id.required">
            This field is required.
          </li>
        </ul>
      </div>
      <div class="mt-4">
        <label>Extra Params</label>
        <form-textarea v-model="form.input.extra_params" />
      </div>
      <div class="mt-6">
        <label>Active</label><form-switch v-model="form.input.active" />
      </div>
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
import FormSelect from '../inputs/FormSelect';
import FormTextarea from '../inputs/FormTextarea';
import FormSwitch from '../inputs/FormSwitch';

export default {
  components: {
    FormInput,
    FormSelect,
    FormTextarea,
    FormSwitch,
  },
  mixins: [formMixin],
  data: () => ({
    form: {
      input: {
        name: null,
        image: 'pixel',
        ga_code_id: null,
        extra_params: null,
        active: true,
      },
      options: {
        images: [
          { value: 'pixel', name: 'Pixel' },
          { value: 'gif', name: 'GIF' },
          { value: 'flat', name: 'Flat' },
          { value: 'flat-gif', name: 'Flat GIF' },
        ],
      },
    },
  }),
  validations: {
    form: {
      input: {
        name: {
          required,
        },
        ga_code_id: {
          required,
        },
      },
    },
  },
};
</script>
