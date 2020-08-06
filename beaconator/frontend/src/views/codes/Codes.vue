<template>
  <div>
    <div class="flex justify-end">
      <button
        class="flex items-center pl-3 pr-4 py-2 bg-primary hover:bg-primary-dark text-white font-bold rounded-full transition duration-300 ease-out"
        @click="showAddModal = true"
      >
        <plus-icon class="mr-1" />Add
      </button>
    </div>
    <div
      v-if="codes"
      class="mt-6"
    >
      <div v-if="codes.length > 0">
        <code-card
          v-for="code in codes"
          :key="code.id"
          class="mt-4"
          :code="code"
          @edit="onEditReq(code)"
          @delete="onDelete(code.id)"
        />
      </div>
      <div
        v-else
        class="px-4 py-4 text-center bg-gray-200 rounded-lg"
      >
        <p class="text-gray-600">
          No codes were found
        </p>
      </div>
    </div>
    <div v-else />

    <form-modal
      :open.sync="showAddModal"
      :initial-data="editing"
      :form="form"
      :title="editing ? 'Edit Code' : 'Add Code'"
      @input="onSubmit"
    />
  </div>
</template>

<script>
import api from '../../mixins/api';
import CodeForm from '../../components/forms/codes/CodeForm';
import FormModal from '../../components/modals/FormModal';
import CodeCard from '../../components/cards/codes/CodeCard';

export default {
  components: {
    FormModal,
    CodeCard,
  },
  data: () => ({
    codes: null,
    form: CodeForm,
    showAddModal: false,
    editing: null,
  }),
  async mounted() {
    try {
      const { data } = await api.getCodes();
      this.codes = data;
    } catch (error) {
      console.log(error);
    }
  },
  methods: {
    async onSubmit(form) {
      if (this.editing) {
        await this.onUpdate(this.editing.id, form);
      } else {
        await this.onAdd(form);
      }
    },
    async onAdd(form) {
      try {
        const { data } = await api.createCode(form);
        if (this.codes) {
          this.codes.push(data);
        } else {
          this.codes = [data];
        }
      } catch (error) {
        console.log(error);
      }
    },
    async onUpdate(id, form) {
      try {
        const { data } = await api.updateCode(id, form);
        this.editing = null;
        const idx = this.codes.findIndex((item) => item.id === id);
        this.codes[idx] = data;
      } catch (error) {
        console.log(error);
      }
    },
    onEditReq(code) {
      this.editing = code;
      this.showAddModal = true;
    },
    async onDelete(id) {
      try {
        const { data } = await api.deleteCode(id);
        this.codes = this.codes.filter((item) => item.id !== id);
      } catch (error) {
        console.log(error);
      }
    },
  },
  head() {
    return {
      title: 'Codes',
    };
  },
};
</script>
