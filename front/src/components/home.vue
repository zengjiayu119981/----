<template>
    <div class="uk-width-2-3@l uk-first-column">
        <h1>我的个人主页</h1>
        <h2>个人信息</h2>
        <div class="widjet__body">
            <div class="user-info" style="margin-bottom: 20px;">
                <div class="user-info__box">
                    <div class="user-info__title">用户名： {{ username }}</div>
                    <div class="user-info__text">性别： {{ gender }}</div>
                    <div class="user-info__text">签名： {{ signature }}</div>
                </div>
            </div>
            <a v-if="username != '未登录'" :href="'/profile'" class="uk-button uk-button-danger">
                <i class="bi bi-pencil-fill"></i>
                <span class="uk-margin-small-left">修改</span>
            </a>
        </div>
        <h2>我的帖子</h2>
        <ul class="posts">
            <li v-for="(post, index) in posts" :key="index" class="post">
                <h3><a :href="'/post/'+post.post_id">{{ post.title }}</a></h3>
                <p>{{ post.content }}</p>
                <a class="uk-button uk-button-danger">
                    <i class="bi bi-trash"></i>
                    <span class="uk-margin-small-left">删除</span>
                </a>
            </li>
        </ul>
        <div><el-pagination layout="prev, pager, next" :total="posts_num"/></div>
        
        <h2>我的评论</h2>



        <div><el-pagination layout="prev, pager, next" total="10" /></div>
    </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue';
import Server from '../utils/require';
import {ElPagination} from "element-plus"
export default {
components:{
    ElPagination
},
setup() {

    const posts=ref([]);
    const posts_num=ref(100);

    onMounted(() => {
        get_post_list();
    });
    function get_post_list() {
        Server.get('/api/user/posts',{
            params:{
                "username":localStorage.getItem('username')
            }
        }).then(response => {
            posts.value = response.data;
            posts_num.value = response.page_num
        });
    }

    const username = computed(
        () => {
            let name = localStorage.getItem('username');
            if (name) return name
            else return "未登录"
        }
    );

    return {
        username,
        posts,
        posts_num,
    }
}
}
</script>

<style scoped>
.posts {
  list-style-type: none; /* 移除默认的列表样式 */
  margin: 0; /* 移除默认的外边距 */
  padding: 0; /* 移除默认的内边距 */
  border: 1px solid #ccc; /* 添加外边框 */
  border-radius: 4px; /* 添加圆角 */
}

.post {
  padding: 15px; /* 添加内边距以提高可读性 */
  margin-bottom: 10px; /* 在每个列表项之间添加一些间距 */
  border: 1px solid #ddd; /* 添加内边框，颜色稍微淡一些 */
  border-radius: 4px; /* 与外边框保持一致的圆角 */
}
</style>
