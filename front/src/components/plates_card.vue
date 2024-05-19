<template>
  <div class="card --horizontal favourites-game">
        <div class="card__box">
          <div class="card__media">
            <a :href="'/plate/'+title"
              ><img :src="'http://localhost:8000/media/plate/'+title+'.jpg'" :alt="title"
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


export default {
    props:["title"],
}
</script>

<style>

</style>