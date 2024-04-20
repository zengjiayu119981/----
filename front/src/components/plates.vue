<template>
  <div class="uk-grid uk-grid-stack" data-uk-grid>
    <div class="uk-width-2-3@l uk-first-column">
      <div class="widjet__head">
        <h3 class="uk-text-lead">论坛</h3>
      </div>
      <div v-for="item of list" :key="item.title" >
        <plates_card :title="item.title">
        </plates_card>
      </div>
      
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { get_plates_list } from '../API/get_plates_list.js';
import plates_card from './plates_card.vue';
export default {
  components:{
    plates_card,
  },
  
  setup() {
    const list =ref([
    ])
    onMounted(()=>{
      get_plates_list().then(res=>{
        list.value = res
      })
    })
    return {
      list
    }
  },
};
</script>

<style>
</style>