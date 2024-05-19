<template>
    <div class="uk-grid uk-grid-stack" data-uk-grid>
    <div class="uk-width-2-3@l uk-first-column">
      <div class="widjet__head">
        <h3 class="uk-text-lead">{{ title }}</h3>
        <div><button @click="publish()" class="btn btn-success">发帖</button></div>
      </div>
      <div v-for="item of list" :key="item.id" >
        <post_card :title="item.title" :author="item.user" :content="item.content"  :post_id = "item.post_id" :image="item.image">
        </post_card>
      </div>
      <div><el-pagination layout="prev, pager, next" :total="total" @current-change="handlePageChange" :current-page="currentpage" /></div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref, watchEffect } from 'vue';
import {useRouter} from 'vue-router';
import post_card from './post_card.vue';
import {ElPagination} from 'element-plus'
import Server from '../utils/require';
export default {
  components:{
    post_card,
    ElPagination
  },
  setup() {
    const list =ref([])
    const current_page = ref(1)
    const total =ref(1)
    const router = useRouter()
    const title = computed(()=>{
      return router.currentRoute.value.params.title
    })
    onMounted(()=>{
      Server.post("api/posts/list",{
        title:title.value,
        current_page:current_page.value
      }).then(res=>{
        list.value = res.data
        total.value = res.total
      })
    })

    function handlePageChange(page){
      current_page.value = page
      Server.post("api/posts/list",{
        title:title.value,
        current_page:current_page.value
      }).then(res=>{
        list.value = res.data
        total.value = res.total
      })
    }

    function publish(){
      router.push({name:'post_publish',params:{title:title.value}})
    }

    return {
      list,
      title,
      total,
      current_page,
      handlePageChange,
      publish,
    }
  },
};
</script>

<style></style>