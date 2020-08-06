<template>
  <div id="app">
    <nav
      class="w-full pin fixed left-0 top-0 bg-gray-800"
      style="z-index:9999"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <div class="flex items-baseline">
              <router-link
                class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 focus:outline-none transition duration-300 ease-out"
                active-class="text-white bg-gray-900"
                to="/properties"
              >
                Properties
              </router-link>
              <router-link
                class="ml-4 px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 focus:outline-none transition duration-300 ease-out"
                active-class="text-white bg-gray-900"
                to="/codes"
              >
                Codes
              </router-link>
            </div>
          </div>
          <div>
            <button
              v-if="$store.state.auth"
              class="text-gray-300 focus:outline-none"
              @click="$store.dispatch('LOGOUT_USER')"
            >
              <logout-variant-icon />
            </button>
          </div>
        </div>
      </div>
    </nav>
    <header class="bg-white shadow mt-16">
      <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
        <h1 class="text-2xl font-semibold leading-tight text-gray-900">
          {{ title }}
        </h1>
      </div>
    </header>
    <main>
      <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <router-view :key="$router.path" />
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data: () => ({
    title: null,
  }),
  watch: {
    $route: {
      handler(to, from) {
        this.title = to.name;
      },
    },
  },
  mounted() {
    this.title = this.$route.name;
  },
};
</script>

<style lang="scss">
#app {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
