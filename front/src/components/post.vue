<template>
    <div class="uk-width-2-3@l uk-first-column">
        <div class="widjet --bio">
            <div class="widjet__head">
                <h3 class="uk-text-lead">{{ data.title }}</h3>
            </div>
            <div>
                <h3 class="author-text">by {{ data.user }}</h3>
            </div>
            <div class="widjet__body"><span>{{ data.content }}</span></div>
            <div class="widjet__body" v-if="data.image != 'http://localhost:8000/media/'"><span><img :src="data.image"
                        alt="image"></span></div>
        </div>
        <div class="widjet --activity">
            <div class="widjet__head">
                <h3 class="uk-text-lead">评论</h3>
            </div>
            <div class="widjet__body" style="margin-top: 10px;" v-for="comment in comments" :key="comment.id">
                <div class="widjet-game">
                    <div class="widjet-game__media">{{ comment.user }}</div>
                    <div class="widjet-game__info">
                        <div class="widjet__body"><span style="font-family: Arial, sans-serif; font-size: 16px;">{{ comment.content }}</span></div>
                        <div><span>{{ timeformat(comment.create_time) }}</span></div>
                    </div>

                </div>
            </div>
            <el-pagination layout="prev, pager, next" :total="total" @current-change="handlePageChange" :current-page="current_page" />

            <div class="widjet__body comment-box">
                <textarea id="comment" placeholder="请输入评论内容..."></textarea>
                <button @click="publish()">发表</button>
                
            </div>
        </div>
    </div>
</template>

<script>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router';
import { get_post_detail } from "../API/get_post_detail.js"
import Server from '../utils/require.js';
import moment from 'moment';
import {ElPagination} from 'element-plus'
import 'moment-timezone'

export default {
    components:{
        ElPagination
    },
    setup() {
        const data = ref({})
        const comments = ref([])
        const total = ref(100)
        const router = useRouter()
        const current_page = ref(1)
        const post_id = computed(() => {
            return router.currentRoute.value.params.id
        })
        onMounted(() => {
            get_post_detail(post_id.value).then(res => {
                data.value = res
            })

            Server.post('/api/comments', {
                post_id: post_id.value,
                current_page:current_page.value
            }).then(res => {
                comments.value = res.data
                total.value = res.total
            })
        })
        function publish() {
            Server.post('/api/publish/comment', {
                post: post_id.value,
                content: document.getElementById('comment').value,
                user: localStorage.getItem('username')
            }).then(response => {
                console.log(response)
                alert(response["msg"])
                Server.post('/api/comments', {
                    post_id: post_id.value,
                    current_page:current_page.value
                }).then(res => {
                    comments.value = res.data
                    total.value = res.total
                    current_page.value=1
                })
            })
        }
        function timeformat(time) {
            console.log(time);
            return moment.utc(time).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        }

        function handlePageChange(num){
            current_page.value = num
            Server.post('/api/comments', {
                post_id: post_id.value,
                current_page:current_page.value
            }).then(res => {
                comments.value = res.data
                total.value = res.total
            })
        }

        return {
            data,
            comments,
            total,
            post_id,
            current_page,
            handlePageChange,
            publish,
            timeformat
        }
    },
}
</script>

<style scoped>
.comment-box {
    margin: 40px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}


.comment-box textarea {
    width: 100%;
    height: 100px;
    resize: vertical;
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 3px;
    box-sizing: border-box;
}

.comment-box button {
    width: 100%;
    padding: 10px;
    background-color: #007BFF;
    color: #fff;
    font-size: 14px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.comment-box button:hover {
    background-color: #0056b3;
}
</style>
