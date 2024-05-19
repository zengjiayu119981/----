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
                <a class="uk-button uk-button-danger" @click="post_delete(post.post_id)">
                    <i class="bi bi-trash"></i>
                    <span class="uk-margin-small-left">删除</span>
                </a>
            </li>
        </ul>
        <div><el-pagination layout="prev, pager, next" :total="posts_total"/></div>
        
        <h2>我的评论</h2>
        <ul class="comments">
            <li v-for="(comment, index) in comments" :key="index" class="comment">
                <h3><a :href="'/post/'+comment.post">回复帖子:  {{  }}</a></h3>
                <p>{{ comment.content }}</p>
                <a class="uk-button uk-button-danger" @click="comment_delete(comment.comment_id)">
                    <i class="bi bi-trash"></i>
                    <span class="uk-margin-small-left">删除</span>
                </a>
            </li>
        </ul>


        <div><el-pagination layout="prev, pager, next" :total="comments_total" @current-change="comment_handlePageChange" :current-page="comments_currentpage" /></div>
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
    const comments =ref([])
    const posts_total=ref(100);
    const comments_total =ref(100)
    const posts_currentpage = ref(1);
    const comments_currentpage = ref(1);

    const username = computed(
        () => {
            let name = localStorage.getItem('username');
            if (name) return name
            else return "未登录"
        }
    );

    onMounted(() => {
        get_post_list();
        get_comments_list();
    });

    function post_delete(post_id){
        Server.post("/api/user/post/delete",{
            post_id
        }).then(response =>{
            posts.value = response.data;
            posts_total.value = response.page_num;
            currentpage.value = 1
        })
    }


    function get_post_list() {
        Server.get('/api/user/posts',{
            params:{
                "username":localStorage.getItem('username'),
                currentpage:posts_currentpage.value
            }
        }).then(response => {
            posts.value = response.data;
            posts_total.value = response.total
        });
    }

    function get_comments_list(){
        Server.get('/api/user/comments',{
            params:{
                "username":localStorage.getItem('username'),
                currentpage:comments_currentpage.value
            }
        }).then(response => {
            comments.value = response.data;
            comments_total.value = response.total
        });
    }

    function comment_handlePageChange(pageNum) {
    
        comments_currentpage.value= pageNum;
        get_comments_list();
  }

    return {
        username,
        posts,
        comments,
        posts_total,
        comments_total,
        posts_currentpage,
        comments_currentpage,
        post_delete,
        comment_handlePageChange,
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
.comments {
  list-style-type: none; /* 移除默认的列表样式 */
  margin: 0; /* 移除默认的外边距 */
  padding: 0; /* 移除默认的内边距 */
  border: 1px solid #ccc; /* 添加外边框 */
  border-radius: 4px; /* 添加圆角 */
}

.comment {
  padding: 15px; /* 添加内边距以提高可读性 */
  margin-bottom: 10px; /* 在每个列表项之间添加一些间距 */
  border: 1px solid #ddd; /* 添加内边框，颜色稍微淡一些 */
  border-radius: 4px; /* 与外边框保持一致的圆角 */
}
</style>
