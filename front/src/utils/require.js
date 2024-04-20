//1. 导入axios对象
import axios from "axios";
//2. 创建对象实例，create方法
import { VueCookies } from "vue-cookies";
const Server = axios.create({
    //请求接口的基础地址
    baseURL: 'http://localhost:8000/', 
    headers: {'X-CSRFToken': $cookies.get('csrftoken'),'Content-Type': 'application/x-www-form-urlencoded'},
    //设置超时时间
    timeout: 4000 
})

Server.defaults.withCredentials=true

Server.interceptors.request.use(config => {

    // 给管理后台的接口设置header头，添加Authorzation属性
    var username = localStorage.getItem('username');
    var authorization = localStorage.getItem('authorization');
    var typ = localStorage.getItem('type');
      // 若 localStorage 中含有这两个字段，则添加入请求头
    if (username && authorization) {
        console.log(username,authorization);
          config.headers.authorization = authorization;
          config.headers.username = username;
          config.headers.type = typ;
      }
    return config;
    
}, error => {
    // 出现异常
    return Promise.reject(error);
})

// 响应拦截器
Server.interceptors.response.use(response =>{

    // 后台正常响应的状态，如果是200， 说明后台处理没有问题
   /*  if (response.status == 200) {
        return response.data;
    } */
    // return response.data 可以在这里统一的获取后台响应的数据进行返回，而这里面就没有请求头那些

    return response.data
}, error => {
    return Promise.reject(error);
})


export default Server // 导出自定义创建 axios 对象
