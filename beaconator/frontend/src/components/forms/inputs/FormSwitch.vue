<template>
  <div>
    <div
      class="form-switch inline-block align-middle"
      style="z-index: 2; margin-top: 6px"
    >
      <input
        :id="id"
        :value="value"
        :checked="value"
        :name="id"
        type="checkbox"
        class="form-switch-checkbox"
        @change="$emit('input', $event.target.checked)"
      >
      <label
        :for="id"
        class="form-switch-label"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
      default: false,
    },
    text: String,
  },
  data: () => ({
    id: null,
  }),
  mounted() {
    this.id = this._uid;
  },
};
</script>

<style lang="postcss">
.form-switch {
  @apply relative select-none w-12 mr-4 leading-normal;
}
.form-switch-checkbox {
  @apply hidden;
}
.form-switch-label {
  @apply block overflow-hidden cursor-pointer bg-slate rounded-full h-6;
  transition: background-color 0.2s ease-in;
  margin-top: 0px;
}
.form-switch-label:before {
  @apply absolute block bg-white w-5 h-5 rounded-full;

  right: 54%;
  content: '';
  /* transition: all 0.2s ease-in; */
  margin-top: 2px;
}
.form-switch-checkbox:checked + .form-switch-label,
.form-switch-checkbox:checked + .form-switch-label:before {
}
.form-switch-checkbox:checked + .form-switch-label {
  @apply bg-primary shadow-none border border-transparent;
}
.form-switch-checkbox:checked + .form-switch-label:before {
  right: 5%;
  margin-top: 1px;
}
</style>
