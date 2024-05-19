<template>
    <div class="uk-grid uk-grid-stack" data-uk-grid>
    <div class="uk-width-2-3@l uk-first-column">
      <div class="widjet__head">
        <h3 class="uk-text-lead">{{ title }}</h3>
        <div><button @click="publish()" class="btn btn-success">添加</button></div>
      </div>
      <div v-for="item of list" :key="item.id" >
        <post_card :title="item.title" :author="item.user" :content="item.content"  :post_id = "item.post_id" :image="item.image">
        </post_card>
      </div>
      
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref, watchEffect } from 'vue';
import {useRouter} from 'vue-router';
import post_card from './post_card.vue';
import { get_posts_list } from '../API/get_posts_list';
export default {
  components:{
    post_card,
  },
  setup() {
    const list =ref([])
    const page = ref(1)
    const page_num =ref(1)
    const router = useRouter()
    const title = computed(()=>{
      return router.currentRoute.value.params.title
    })
    onMounted(()=>{
      get_posts_list(title.value).then(res=>{
        list.value = res.data
        page_num.value = res.page_num
      })
    })
    watchEffect(()=>{
      console.log(title.value)
    })
    function publish(){
      router.push({name:'post_publish',params:{title:title.value}})
    }

    return {
      list,
      title,
      page_num,
      publish,
    }
  },
};
</script>

<style></style>