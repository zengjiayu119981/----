<template>
    <div class="uk-width-2-3@l uk-first-column">
        <div class="widjet --bio">
            <div class="widjet__head">
                <h3 class="uk-text-lead">{{data.title}}</h3>
            </div>
            <div>
                <h3 class="author-text">by  {{data.user}}</h3>
            </div>
            <div class="widjet__body"><span>{{data.content}}</span></div>
            <div class="widjet__body"><span></span></div>
        </div>
        <div class="widjet --activity">
            <div class="widjet__head"> 
                <h3 class="uk-text-lead">评论</h3>
                <a href="04_profile.html">发表评论</a>
            </div>
            <div class="widjet__body">
                <div class="widjet-game">
                    <div class="widjet-game__media"><a href="10_game-profile.html"><img src=""
                                alt="image"></a></div>
                    <div class="widjet-game__info"><a class="widjet-game__title" href="10_game-profile.html"> Chrome
                            Fear</a>
                        <div class="widjet-game__record">3 hours on record</div>
                        <div class="widjet-game__last-played">last played on 18 Feb, 2022</div>
                    </div>
                </div>
                <div class="widjet-game-info">
                    <div class="widjet-game-info__title">Achievement Progress</div>
                    <div class="widjet-game-info__progress"><span>50 of 150</span>
                        <div class="progress-box">
                            <div class="progress-line" style="width: 80%"></div>
                        </div>
                    </div>
                    <div class="widjet-game-info__acheivement">
                        <ul>
                            <li><img src="" alt="acheivement"></li>
                            <li><span>+10</span></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="widjet__body">
                <div class="widjet-game">
                    <div class="widjet-game__media"><a href="10_game-profile.html"><img src=""
                                alt="image"></a></div>
                    <div class="widjet-game__info"><a class="widjet-game__title" href="10_game-profile.html"> Retaliate
                            of Prosecution</a>
                        <div class="widjet-game__record">0.2 hours on record</div>
                        <div class="widjet-game__last-played">last played on 25 Apr, 2022</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { onMounted, ref,computed } from 'vue'
import {useRouter} from 'vue-router';
import {get_post_detail} from "../API/get_post_detail.js"
export default {
    setup() {
        const data =ref({})
        const router = useRouter()
        const post_id = computed(()=>{
            return router.currentRoute.value.params.id
        })
        onMounted(() => {
            get_post_detail(post_id.value).then(res => {
                data.value = res
            })
        })
        return {
            data
        }
    },
}
</script>

<style></style>