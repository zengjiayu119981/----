<template>
    <div class="post-form">
      <h2>发布新帖子</h2>
      <form @submit.prevent="submitPost">
        <div class="form-group">
          <label for="title">标题：</label>
          <input type="text" id="title" v-model="post.title" required />
        </div>
        <div class="form-group">
          <label for="content">内容：</label>
          <textarea id="content" v-model="post.content" required></textarea>
        </div>
        <div class="form-group">
          <label for="image">图片上传：</label>
          <input type="file" ref="image" @change="handleImageUpload" />
        </div>
        <div class="form-group">
          <img v-if="imageUrl" :src="imageUrl" alt="预览图片">
        </div>
        <button type="submit" :disabled="!isFormValid">发布</button>
      </form>
    </div>
  </template>
  
  <script>
  import Server from '../utils/require'
  export default {
    data() {
      return {
        post: {
          title: '',
          content: '',
          plate:'',
          user:'',
          plate:'',
        },
        imageUrl: '',
        uploadProgress: 0, // 图片上传进度
      };
    },
    computed: {
      isFormValid() {
        // 确保标题和内容都不为空
        return this.post.title && this.post.content;
      },
    },
    mounted() {
      // 获取板块信息
      this.post.plate = this.$route.params.title;
      this.post.user = localStorage.getItem('username');
    },
    methods: {
      async submitPost() {
        // 这里可以添加验证逻辑，然后调用API发布帖子
        try {
          const form_data = new FormData();
          if (this.imageUrl) {
            form_data.append('image', this.$refs.image.files[0]);
          }
          else {
            form_data.append('image', '');
          }
          form_data.append('title', this.post.title);
          form_data.append('content', this.post.content);
          form_data.append('plate', this.post.plate);
          form_data.append('user', this.post.user);

          // 发布帖子到服务器
          await Server.post('/api/public/post', form_data,{
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }).then(response => {
            if (response["message"]=='未查询到登录信息'){
              alert("未查询到登录信息")
            }
            else {
              alert(response["message"])
              this.$router.push('/plate/'+this.post.plate); // 发布成功后跳转到帖子列表
            }
              
          });
          
        } catch (error) {
          console.error('发布失败:', error);
        }
      },
      handleImageUpload(event) {
        // 处理图片上传事件
        const file = event.target.files[0];
        if (file) {
          this.imageUrl = file;
        }
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageUrl = e.target.result;
        };
        reader.readAsDataURL(file);
      },
      
    },
  };
  </script>
  
  <style scoped>
  /* 添加一些基本样式 */
  .form-group {
    margin-bottom: 1rem;
  }
  .progress-bar {
    margin-top: 1rem;
  }
  #content {
    /* 增加宽度和高度 */
    width: 100%; /* 使其占据父元素的全部宽度 */
    height: 200px; /* 设置一个具体的高度，比如200像素，你可以根据需要调整 */

    /* 可选：增加一些额外的样式改善用户体验 */
    resize: vertical; /* 允许用户垂直调整大小 */
    padding: 10px; /* 内边距，让文本区域更舒适 */
    font-size: 16px; /* 字体大小 */
    border-radius: 5px; /* 边框圆角 */
    border: 1px solid #ccc; /* 边框样式 */
}
  </style>