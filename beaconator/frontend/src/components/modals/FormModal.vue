<template>
  <sidebar-modal
    :open="open"
    @close="handleClose"
  >
    <template v-slot:header>
      <h2 class="sidebar-title">
        {{ title }}
      </h2>
    </template>
    <div v-if="open">
      <component
        :is="form"
        :initial-data="initialData"
        @input="handleFormInput"
      />
    </div>
  </sidebar-modal>
</template>

<script>
import SidebarModal from './SidebarModal';

export default {
  name: 'FormModal',
  components: {
    SidebarModal,
  },
  props: {
    title: {
      type: String,
      default: 'Modal',
    },
    form: Object,
    initialData: {
      type: Object,
      default: null,
    },
    open: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    handleFormInput(form) {
      if (this.initialData) {
        this.$emit('update', form);
      } else {
        this.$emit('create', form);
      }
      this.$emit('input', form);
      this.$emit('update:open');
    },
    handleClose() {
      this.$emit('update:open', false);
      this.$emit('close');
    },
  },
};
</script>
