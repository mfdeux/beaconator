<template>
  <div
    :class="[focus ? 'shadow-input' : null, hover ? 'shadow-input' : null]"
    class="rounded-lg border-2 border-slate bg-transparent transition duration-300 ease-out hover:shadow-input"
    style="padding: 1px 0px;"
  >
    <div class="flex items-center justify-between pr-2">
      <input
        :type="type"
        :value="value"
        :class="['w-full py-2 px-3 rounded-lg', status === 'error' ? 'border-red' : '']"
        class="flex-grow focus:outline-none bg-transparent"
        @focus="focus = true"
        @blur="focus = false"
        @mouseover="hover = true"
        @mouseout="hover = false"
        @input="$emit('input', $event.target.value)"
      >
      <button
        v-if="value && clearable"
        type="button"
        class="py-1 px-1 rounded-full ml-2 focus:outline-none text-light"
        @click="handleClear"
      >
        <close-icon :size="22" />
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FormInput',
  props: {
    status: {
      type: String,
    },
    type: {
      type: String,
      default: 'text',
    },
    value: {
      type: String,
    },
    clearable: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    focus: false,
    hover: false,
  }),
  methods: {
    handleClear() {
      this.$emit('input', null);
    },
    handleFocus(e) {
      console.log(e);
    },
  },
};
</script>
