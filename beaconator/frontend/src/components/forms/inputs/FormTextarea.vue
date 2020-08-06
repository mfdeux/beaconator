<template>
  <textarea
    :value="value"
    :class="[
      'appearance-none block w-full px-3 py-3 mb-3 focus:outline-none bg-transparent rounded-lg border-2 bg-transparent transition duration-300 ease-out',
      status === 'error' ? 'border-red' : 'border-gray-200',
      tooLong ? 'long' : null,
      focus ? 'shadow-input' : null,
      hover ? 'shadow-input' : null,
    ]"
    class="rounded-none"
    @focus="focus = true"
    @blur="focus = false"
    @mouseover="hover = true"
    @mouseout="hover = false"
    @input="$emit('input', $event.target.value)"
  />
</template>

<script>
export default {
  name: 'FormTextarea',
  props: {
    status: {
      type: String,
    },
    value: {
      type: String,
    },
    tooLong: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    focus: false,
    hover: false,
  }),
};
</script>
