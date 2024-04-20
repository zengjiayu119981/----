<template>
  <div class="login">
        <header class="login__header">
            <h2>
                <svg class="icon">
                    <use xlink:href="#icon-lock" />
                </svg>注册
            </h2>
            <h4>
                {{ msg }}
            </h4>
        </header>
        <div  class="login__form" >
            <div>
                <label for="email">用户名</label>
                <input v-model="user_name" type="text"  name="user_name" placeholder="用户名">
            </div>
            <div>
                <label for="password">密码</label>
                <input v-model="password" type="password"  name="password" placeholder="密码">
            </div>
            <div>
                <button @click="register_users()" >注册</button>
            </div>
        </div>
    </div>
  
</template>
<script>
import "./assets/style.css"
import { user_register } from '../src/API/register.js'
import { ref } from 'vue';

export default {
    name: 'Login',
    setup(){
        const user_name = ref("")
        const password = ref("")
        const msg = ref("")
        function register_users() {
            user_register(user_name.value, password.value).then(
                function (response) {
                    msg.value = response.msg
                    if(response.msg=='register_success')
                        window.location=='/login/'
                })
                .catch(function (error) {
                    msg.value = error.message
                    console.log(error)
                })
        }
        return{
            user_name,
            password,
            msg,
            register_users,
        }
    },
    }

</script>