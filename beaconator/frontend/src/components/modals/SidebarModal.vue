<template>
  <div
    :id="`sidebar-${id}`"
    class="sidebar overflow-y-auto pb-6 px-6 pt-32 lg:pt-20 w-4/5 lg:w-1/3"
    style="visibility: hidden"
  >
    <div
      v-if="close"
      class="flex items-center justify-between mb-4"
    >
      <div>
        <slot name="header" />
      </div>
      <button
        class="flex items-center py-1 px-1 bg-slate-235 hover:bg-slate-225 outline-none focus:outline-none"
        @click="handleClose"
      >
        <close-icon :size="23" />
      </button>
    </div>
    <slot />
  </div>
</template>

<script>
import { TweenMax, Power4 } from 'gsap';
import { bodyFreezeScroll, bodyUnfreezeScroll } from '../../utils/ui';

export default {
  name: 'BaseSidebar',
  props: {
    open: {
      type: Boolean,
      default: false,
    },
    close: {
      type: Boolean,
      default: true,
    },
  },
  data: () => ({
    id: null,
  }),
  watch: {
    open: function(open) {
      const elem = document.getElementById(`sidebar-${this.id}`);
      if (open) {
        elem.style.visibility = 'visible';
        bodyFreezeScroll();
      } else {
        setTimeout(() => {
          bodyUnfreezeScroll();
          elem.style.visibility = 'hidden';
        }, 500);
      }
      const dX = open ? 0 : this.$el.offsetWidth;
      TweenMax.to(this.$el, 0.6, {
        x: dX,
        ease: Power4.easeOut,
      });
    },
  },
  mounted() {
    this.id = this._uid;
    TweenMax.set(this.$el, {
      x: this.$el.offsetWidth,
    });
  },
  methods: {
    handleClose() {
      this.$emit('update:open', !open);
      this.$emit('close');
    },
  },
};
</script>
