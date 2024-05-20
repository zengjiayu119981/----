<template>
    <div class="uk-width-2-3@l uk-first-column">
        <h1>我的个人主页</h1>
        <h2>个人信息</h2>
        <div class="widjet__body">
            <div class="user-info" style="margin-bottom: 20px;" v-if="!isEditing">
                <div class="user-info__box">
                    <div class="user-info__title">用户名： {{ userInfo.username }}</div>
                    <div class="user-info__title">性 &nbsp;  别： {{ userInfo.gender }}</div>
                    <div class="user-info__title">签 &nbsp;  名： {{ userInfo.signature }}</div>
                    <button style="margin-top: 10px;" v-if="userInfo.username" class="uk-button uk-button-primary" @click="startEditing">修改</button>
                </div>
            </div>
            <form v-else >
                <div class="user-info__title">用户名： {{ userInfo.username }}</div>
                <div class="user-info__title">性&nbsp;别： <input type="select" v-model="changeinfo.gender" list="typelist">
                    <datalist id="typelist">
                        <option>男</option>
                        <option>女</option>
                    </datalist>
                </div>
                <div class="user-info__title">签&nbsp;名： <textarea v-model="changeinfo.signature"></textarea></div>
                <button type="button" @click="saveChanges">确认</button>
                <button type="button" @click.prevent="cancelChanges">取消</button>
            </form>
        </div>
        <h2>我的帖子</h2>
        <ul class="posts">
            <li v-for="(post, index) in posts" :key="index" class="post">
                <h4><a :href="'/post/'+post.post_id">{{ post.title }}</a></h4>
                <p>{{ post.content }}</p>
                <a class="uk-button uk-button-danger" @click="post_delete(post.post_id)">
                    <i class="bi bi-trash"></i>
                    <span class="uk-margin-small-left">删除</span>
                </a>
            </li>
        </ul>
        <div><el-pagination layout="prev, pager, next" :total="posts_total" @current-change="post_handlePageChange" :current-page="posts_currentpage"/></div>
        
        <h2>我的评论</h2>
        <ul class="comments">
            <li v-for="(comment, index) in comments" :key="index" class="comment">
                <h3><a :href="'/post/'+comment.post">回复帖子:  {{ comment.post_title }}</a></h3>
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
    const posts_total=ref(1);
    const comments_total =ref(1)
    const posts_currentpage = ref(1);
    const comments_currentpage = ref(1);
    const isEditing = ref(false);
    const userInfo = ref({
        username: '',
        gender: '男',
        signature: '',
    });
    const changeinfo=ref({
        username: '',
        gender: '',
        signature: '',
    })

    function startEditing(){
        isEditing.value = true;
    }

    function saveChanges(){
        Server.post("/api/user/update",{
            "username":localStorage.getItem('username'),
            "gender":changeinfo.value.gender,
            "signature":changeinfo.value.signature,
        }).then(response =>{
            userInfo.value.gender =changeinfo.value.gender =response.data.gender;
            userInfo.value.signature = changeinfo.value.signature = response.data.signature;
            if(response.msg=='更新成功')
                alert(response.msg)
            else alert("更新失败")
        })
        isEditing.value = false
    }

    function cancelChanges(){
        isEditing.value = false
    }

    onMounted(() => {
        get_posts_list();
        get_comments_list();
        user_info();
        userInfo.value.username = localStorage.getItem('username');
        changeinfo.value.username=userInfo.value.username
        changeinfo.value.signature=userInfo.value.signature
    });

    function user_info(){
        Server.get("/api/user/info",{
            params:{
                "username":localStorage.getItem('username'),
            }
        }).then(response =>{
            userInfo.value.gender = response.gender;
            userInfo.value.signature = response.signature;
        })
    }

    function post_delete(post_id){
        Server.post("/api/user/post/delete",{  
            post_id:post_id,
            currentpage:posts_currentpage.value,
            "username":localStorage.getItem('username'),
        }).then(response =>{
            posts.value = response.data;
            posts_total.value = response.page_num;
            posts_currentpage.value = 1
        })
    }
    
    function comment_delete(comment_id){
        Server.post("/api/user/comment/delete",{  
            comment_id,
            currentpage:comments_currentpage.value,
            "username":localStorage.getItem('username'),
        }).then(response =>{
            comments.value = response.data;
            comments_total.value = response.page_num;
            comments_currentpage.value = 1
        })
    }



    function get_posts_list() {
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

  function post_handlePageChange(pageNum) {
    
        posts_currentpage.value= pageNum;
        get_posts_list();
    }

    return {
        posts,
        comments,
        posts_total,
        comments_total,
        posts_currentpage,
        comments_currentpage,

        userInfo,
        changeinfo,

        isEditing,
        startEditing,
        saveChanges,
        cancelChanges,


        post_delete,
        comment_delete,
        post_handlePageChange,
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
textarea{
    width: 100%;
    height: 100px;
    resize: vertical;
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 3px;
    box-sizing: border-box;
}
</style>
