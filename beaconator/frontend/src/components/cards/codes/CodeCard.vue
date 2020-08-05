<template>
  <div class="px-4 py-4 shadow rounded-lg flex items-center justify-between">
    <div class="">
      <p class="text-lg font-semibold">
        {{ code.name }}
      </p>
      <p class="text-sm font-medium text-gray-600">
        {{ code.code }}
      </p>
    </div>

    <div class="flex items-center">
      <button
        class="flex items-center py-1 px-1 bg-slate-235 hover:bg-slate-225 outline-none focus:outline-none"
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
    code: {
      type: Object,
    },
  },
};
</script>
