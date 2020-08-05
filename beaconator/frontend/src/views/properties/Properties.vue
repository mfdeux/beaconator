<template>
  <div>
    <div class="flex justify-end">
      <button
        class="px-4 py-2 bg-purple-500 text-white font-semibold rounded"
        @click="showAddModal = true"
      >
        + Add
      </button>
    </div>
    <div v-if="properties" class="mt-4">
      <div v-if="properties.length > 0">
        <property-card
          v-for="property in properties"
          :key="property.id"
          class="mt-4"
          :property="property"
          @edit="onEditReq(property)"
          @delete="onDelete(property.id)"
        />
      </div>
      <div v-else class="px-4 py-4 text-center bg-gray-200 rounded-lg">
        <p class="text-gray-600">
          No properties were found
        </p>
      </div>
    </div>
    <div v-else />
    <form-modal
      :open.sync="showAddModal"
      :initial-data="editing"
      :form="form"
      :title="editing ? 'Edit Property' : 'Add Property'"
      @input="onSubmit"
    />
  </div>
</template>

<script>
import api from '../../mixins/api';
import PropertyForm from '../../components/forms/properties/PropertyForm';
import FormModal from '../../components/modals/FormModal';
import PropertyCard from '../../components/cards/properties/PropertyCard';

export default {
  components: {
    FormModal,
    PropertyCard,
  },
  data: () => ({
    properties: null,
    form: PropertyForm,
    showAddModal: false,
    editing: null,
  }),
  async mounted() {
    try {
      const { data } = await api.getProperties();
      this.properties = data;
    } catch (error) {
      console.log(error);
    }
    try {
      const { data } = await api.getCodes();
      const values = data.map((item) => ({ value: item.id, name: `${item.name} (${item.code})` }));
      this.$store.commit('UPDATE_CODE_OPTIONS', values);
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
        const { data } = await api.createProperty(form);
        if (this.properties) {
          this.properties.push(data);
        } else {
          this.properties = [data];
        }
      } catch (error) {
        console.log(error);
      }
    },
    async onUpdate(id, form) {
      try {
        const { data } = await api.updateProperty(id, form);
        this.editing = null;
        const idx = this.properties.findIndex((item) => item.id === id);
        this.properties[idx] = data;
      } catch (error) {
        console.log(error);
      }
    },
    onEditReq(property) {
      this.editing = property;
      this.showAddModal = true;
    },
    async onDelete(id) {
      try {
        await api.deleteProperty(id);
      } catch (error) {
        console.log(error);
      }
    },
  },
  head() {
    return {
      title: 'Properties',
    };
  },
};
</script>
