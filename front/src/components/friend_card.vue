<template>
  <div class="uk-grid-margin">
    <div class="user-item --active">
      <div class="user-item__avatar">
        <img src="" alt="user" />
      </div>
      <div class="user-item__box">
        <div class="user-item__name">
          <a href="06_chats.html">{{ name }}</a>
        </div>
      </div>
      <div class="user-item__more">
        <a class="bi bi-arrow-right" href="#!"></a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    props:["name"]
};
</script>

<style>
</style>