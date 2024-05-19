<template>
  <header class="page-header">
    <div class="page-header__inner">
      <div class="page-header__sidebar">
        <div class="page-header__menu-btn">
          <button class="menu-btn ico_menu is-active"></button>
        </div>
        <div class="page-header__logo">
          <img src="../assets/img/logo.jpg" alt="logo" /><span
            class="page-header__logo_text"
            >在线论坛</span
          >
        </div>
      </div>

      <div class="page-header__content">
        <div class="page-header__search">
          <div class="search">
            <div class="search__input">
              <input type="search" name="search" placeholder="Search" />
            </div>
            <div class="search__btn">
              <button type="button"><i class="bi bi-search"></i></button>
            </div>
          </div>
        </div>

        <div class="page-header__action" style="position: relative;right: 50px;">
          <a class="action-btn" href="06_chats.html"
            ><i class="bi bi-chat-left-text"></i><span></span
          ></a>

          <a class="static-btn" href="07_friends.html"
            ><i class="bi bi-bell"></i><span></span
          ></a>
          
          <div class="dropdown" >
            <button class="btn" type="button" data-toggle="dropdown" >
              <i class="bi bi-person-square">{{username}}</i><span></span>
            </button>
            <div class="dropdown-menu" >
              <a class="dropdown-item" v-if="username=='未登录'" href="/login/">登录</a>
              <a class="dropdown-item" href="#" @click="logout">退出登录</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { computed, onMounted, ref } from 'vue';

export default {
  setup() {
    const username = computed(() => {
      let name = localStorage.getItem('username')
      if (name != null)
        return name
      return "未登录"
    })
    function logout() {
      localStorage.removeItem('username')
      localStorage.removeItem('authorization')
      window.location= "/"
    }
    return {
      username,
      logout
    }
    
  }
};
</script>

<style>

</style>