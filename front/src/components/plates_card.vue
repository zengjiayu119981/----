<template>
  <div class="card --horizontal favourites-game">
        <div class="card__box">
          <div class="card__media">
            <a :href="'/plate/'+title"
              ><img src="" :alt="title"
            /></a>
          </div>
          <div class="card__info">
            <a class="card__title" :href="'/plate/'+title">
              {{ title }}</a
            >
          </div>
        </div>
      </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { get_plate_pic } from '../API/get_plate_pic';


export default {
    props:["title"],
    setup(props) {
      onMounted(() => {
        get_plate_pic(props.title).then(res => {
          pic_url.value=res.pic
        })
      })
   
    }
}
</script>

<style>

</style>