<template>
  <div class="page-content">
    <sidebar></sidebar>
    <main class="page-main">
     	  <router-view />
    </main>
  </div>
</template>

<script>
import sidebar from './sidebar.vue';
export default {
    components:{
        sidebar,
    }
};
</script>

<style>

</style>