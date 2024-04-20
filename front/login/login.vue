<template>
    <div class="login">
        <header class="login__header">
            <h2>
                <svg class="icon">
                    <use xlink:href="#icon-lock" />
                </svg>登录
            </h2>
            <h3>
                {{ msg }}
            </h3>
        </header>
        <div class="login__form">
            <div>
                <label for="email">用户名</label>
                <input v-model="user_name" type="text" name="user_name" placeholder="用户名">
            </div>
            <div>
                <label for="password">密码</label>
                <input v-model="password" type="password" name="password" placeholder="密码">
            </div>
            <div>
                <button @click="login_users()">登录</button>
            </div>
            <div>

                <a href="/register/">
                    <button>注册</button>
                </a>
            </div>
            <div>
                <button @click="login_users()">管理员登录</button>
            </div>
        </div>
    </div>

</template>
<script>
import "./assets/style.css"
import { user_login } from '../src/API/login.js'
import { ref } from 'vue';

export default {
    name: 'Login',
    setup() {
        const user_name = ref("")
        const password = ref("")
        const msg = ref("")
        function login_users() {
            user_login(user_name.value, password.value).then(
                function (data) {
                    console.log(data)
                    if (data.msg == 'login_success') {
                        let username = data.name;
                        let authorization = data.token;
                        let typ = data.type;
                        console.log(username,authorization);
                        localStorage.setItem("username", username);
                        localStorage.setItem("authorization", authorization)
                        localStorage.setItem("type", typ)
                        window.location = "/";
                    }
                    msg.value = data.msg
                }).catch(function (error) {
                    msg.value = error.message
                    console.log(error)
                })

        }
        return {
            user_name,
            password,
            msg,
            login_users,
        }
    },
}

</script>