<template>
  <div class="uk-grid uk-grid-stack" data-uk-grid="">
    <div class="uk-width-2-3@xl uk-first-column">
      <div class="widjet --filters">
        <div class="widjet__head">
          <h3 class="uk-text-lead">Friends</h3>
        </div>
        <div class="widjet__body">
          <div class="uk-grid uk-flex-middle uk-grid-small" data-uk-grid="">
            <div class="uk-width-expand@s uk-first-column">
              <div class="search">
                <div class="search__input">
                  <i class="ico_search"></i
                  ><input type="search" name="search" placeholder="Search" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="uk-grid uk-grid-small uk-child-width-1-2@m" data-uk-grid="">
        
        <div v-for="item of list" :key="item.id" >
        <friend_card :name="item.name">
        </friend_card>
        </div>

        
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import friend_card from './friend_card.vue';  
export default {
  components:{
    friend_card
  },
  setup() {
    const list=ref([
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
        {
            name:'zeng'
        },
    ])
    return {
      list  
    }
  },
};
</script>

<style>
</style>