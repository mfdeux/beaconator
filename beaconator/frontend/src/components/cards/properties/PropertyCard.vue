<template>
  <div class="px-4 py-4 shadow rounded-lg flex items-center justify-between">
    <div class="">
      <p class="text-lg font-semibold">
        {{ property.name }}
      </p>
      <p class="text-md text-gray-600 font-medium mt-2">
        Google Analytics Code: {{ property.ga_code.name }} {{ property.ga_code.code }}
      </p>
      <a :href="url" target="_blank" class="text-sm font-medium text-gray-600 underline">{{
        url
      }}</a>
    </div>

    <div class="flex items-center">
      <button
        class="flex items-center py-1 px-1 bg-slate-235 hover:bg-slate-225 outline-none focus:outline-none"
        @click="onCopy"
      >
        <clipboard-text-outline-icon />
      </button>

      <button
        class="ml-2 flex items-center py-1 px-1 bg-slate-235 hover:bg-slate-225 outline-none focus:outline-none"
        @click="$emit('edit')"
      >
        <pencil-outline-icon />
      </button>
      <button
        class="ml-2 flex items-center py-1 px-1 bg-slate-235 hover:bg-slate-225 outline-none focus:outline-none"
        @click="$emit('delete')"
      >
        <trash-can-outline-icon />
      </button>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    property: {
      type: Object,
    },
  },
  computed: {
    url() {
      if (window.location.port) {
        return `${window.location.protocol}//${window.location.hostname}:${window.location.port}/images/${this.property.code}`;
      }
      return `${window.location.protocol}//${window.location.hostname}/images/${this.property.code}`;
    },
  },
  methods: {
    onCopy() {
      this.$copyText(this.url);
    },
  },
};
</script>
