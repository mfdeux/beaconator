import { objDiff } from '../utils';

export default {
  props: {
    initialData: {
      type: null,
    },
    diffInitial: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    initialData: {
      handler(current) {
        this.form.input = { ...this.form.input, ...this.initialData };
      },
      deep: true,
      immediate: true,
    },
  },
  methods: {
    focusFirstStatus(component = this) {
      if (component.status) {
        component.$el.focus();
        return true;
      }

      let focused = false;

      component.$children.some((childComponent) => {
        focused = this.focusFirstStatus(childComponent);
        return focused;
      });

      return focused;
    },
    validate() {
      this.$v.$touch();
      this.$nextTick(() => this.focusFirstStatus());
    },
    onClear() {
      this.$v.form.input.$reset();
      this.form.input = Object.assign({}, this.form.default);
    },
    onSubmit() {
      this.validate();
      if (this.$v.form.$pending || this.$v.form.$error) return;
      if (this.initialData && this.diffInitial) {
        this.$emit('input', objDiff(this.initialData, this.form.input));
        return;
      }
      this.$emit('input', this.form.input);
    },
  },
};
