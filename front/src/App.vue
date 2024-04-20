<template>
  <div id="page-home">
    <preloadVue></preloadVue>
    <div class="page-wrapper">
        <pageheader></pageheader>
        <pagecontent></pagecontent>  
    </div>
  </div>
</template>

<script>
  import pageheader from './components/pageheader.vue';
  import pagecontent from './components/pagecontent.vue';
  import preloadVue from './components/preload.vue';
  export default {
    components:{
      pageheader,
      pagecontent,
      preloadVue,
    },
  };
</script>
  
<style scoped>

</style>
