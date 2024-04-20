<template>
  <aside class="sidebar is-show" id="sidebar">
    <div class="sidebar-box">
      <ul class="uk-nav">
        <li>
          <router-link to="/home"><i class="bi bi-house-door"></i><span>主页</span></router-link>
        </li>
        <li class="uk-nav-header">Main</li>
        <li>
          <router-link to="/plates"><i class="bi bi-receipt-cutoff"></i><span>论坛</span></router-link>
        </li>
        <li>
          <router-link to="/friends"><i class="bi bi-person-video2"></i><span>朋友</span></router-link>
        </li>
        <li>
          <a href="08_wallet.html"
            ><i class="bi bi-heart"></i><span>我关心的</span></a
          >
        </li>
        
        <li class="uk-nav-header">Support</li>
        <li >
          <a @click="submit()"
            ><i class="bi bi-info-circle-fill" ></i><span>关于</span></a
          >
        </li>
      </ul>
    </div>
    <modal :show="show" @hideModal="hideModal" >
    
    </modal>
  </aside>
  
</template>

<script>
import { ref } from 'vue';
import modal from './modal.vue';
export default {
    components:{
      modal
    },
    setup(){
      const show = ref(false)
      function hideModal() {
			  show.value = false;
		  }
		  function submit() {
			  show.value = true;	
		  }
      return{
        hideModal,
        submit,
        show
      }
    }
};
</script>

<style>

</style>