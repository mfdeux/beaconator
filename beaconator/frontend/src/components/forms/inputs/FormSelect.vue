<template>
  <div
    :class="[focus ? 'shadow-input' : null, hover ? 'shadow-input' : null]"
    class="w-full flex justify-start appearance-none block w-full px-3 py-3 mb-3 focus:outline-none bg-transparent rounded-lg border-2 bg-transparent transition duration-300 ease-out"
  >
    <select
      :id="id"
      :key="selectKey"
      :value="value"
      :class="['flex-grow focus:outline-none bg-transparent']"
      class="rounded-none"
      @focus="focus = true"
      @blur="focus = false"
      @mouseover="hover = true"
      @mouseout="hover = false"
      @input="handleInput"
    >
      <option
        v-for="(option, i) in formattedOptions"
        :key="i"
        :value="option.value"
      >
        {{ option.name }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'FormSelect',
  props: {
    options: {
      type: Array,
    },
    placeholder: {
      type: String,
    },
    status: {
      type: String,
    },
    value: {
      type: String,
    },
  },
  data() {
    return {
      id: null,
      selectKey: null,
      focus: false,
      hover: false,
    };
  },
  computed: {
    formattedOptions() {
      if (this.placeholder) {
        return [{ name: this.placeholder, value: null, disabled: true }, ...this.options];
      }
      return this.options;
    },
  },
  watch: {
    options: function(newVal, oldVal) {
      this.$forceUpdate();
    },
  },
  mounted() {
    this.id = this._uid;
    this.selectKey = this._uid;
  },
  methods: {
    handleInput(event) {
      this.$emit('input', event.target.value);
    },
  },
};
</script>
