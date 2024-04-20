import { createRouter, createWebHistory } from 'vue-router'
const home = ()=>import('../components/home.vue')
const plates = ()=>import('../components/plates.vue')
const friends = ()=>import('../components/friends.vue')
const plate = ()=>import('../components/plate_template.vue')
const post = ()=>import('../components/post.vue')


const routes=[
    {path:'/',component: home},
    {path:'/home',component: home},
    {path:'/plates',component: plates},
    {path:'/friends',component: friends},
    {path:'/plate/:title',component: plate},
    {path:'/post/:id',component: post}
]

const router = createRouter({  
    history: createWebHistory(),  
    routes
})



export default router