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
                <a href="04_profile.html">发表评论</a>
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
import 'moment-timezone'

export default {
    setup() {
        const data = ref({})
        const comments = ref([])
        const page_num = ref(1)
        const router = useRouter()
        const post_id = computed(() => {
            return router.currentRoute.value.params.id
        })
        onMounted(() => {
            get_post_detail(post_id.value).then(res => {
                data.value = res
            })

            Server.post('/api/comments', {
                post_id: post_id.value
            }).then(res => {
                comments.value = res.data
                page_num.value = res.page_num
            })
        })
        function publish() {
            Server.post('/api/publish/comment', {
                post: post_id.value,
                content: document.getElementById('comment').value,
                user: localStorage.getItem('username')
            }).then(response => {
                console.log(response)
                alert(response["message"])
                Server.post('/api/comments', {
                    post_id: post_id.value
                }).then(res => {
                    comments.value = res.data
                    page_num.value = res.page_num
                })
            })
        }
        function timeformat(time) {
            console.log(time);
            return moment.utc(time).tz('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss')
        }
        return {
            data,
            comments,
            page_num,
            post_id,
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
