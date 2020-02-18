<template>
  <div id="app">
    <Head></Head>
    
      <!-- <router-link to="/map">Map</router-link> -->
      <router-view></router-view>
    
  </div>
</template>

<script>
import Head from './components/Head.vue'

export default {
  name: 'App',
  components: {
    Head
  }
}
</script>
