<template>
    <div class="card --horizontal --small">
        <div class="card__box">
            <div class="card__media"><a :href="'/post/'+post_id"><img src=""
                        :alt="title"></a></div>
            <div class="card__info"><a class="card__title" :href="'/post/'+post_id"> {{ title }}</a>
                <div class="card__date"><span>{{ content }}</span></div>
                <div class="card__author"><span>by  </span>{{ author }}</div>
            </div>
            <!-- <div class="card__more"><a href=""><i class="ico_more"></i></a></div> -->
        </div>
    </div>
</template>

<script>
export default {
    props:['title',"author","content","tag","post_id"]
}
</script>

<style>

</style>