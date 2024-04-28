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
          <input type="file" id="image" @change="handleImageUpload" />
        </div>
        <button type="submit" :disabled="!isFormValid">发布</button>
      </form>
      <div v-if="uploadProgress" class="progress-bar">
        {{ uploadProgress }}%
      </div>
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
          image: null, // 用于存储图片文件
        },
        uploadProgress: 0, // 图片上传进度
      };
    },
    computed: {
      isFormValid() {
        // 确保标题和内容都不为空
        return this.post.title && this.post.content;
      },
    },
    methods: {
      async submitPost() {
        // 这里可以添加验证逻辑，然后调用API发布帖子
        try {
          if (this.post.image) {
            // 假设这里有一个上传图片的方法uploadImage并返回进度
            await this.uploadImage();
          }
          // 发布帖子到服务器
          await Server.post('/api/public/post', this.post);
          this.$router.push('/posts'); // 发布成功后跳转到帖子列表
        } catch (error) {
          console.error('发布失败:', error);
        }
      },
      handleImageUpload(event) {
        // 处理图片上传事件
        const file = event.target.files[0];
        if (file) {
          this.post.image = file;
          // 可以在这里预览图片或直接开始上传
        }
      },
      async uploadImage() {
        // 这是一个示例方法，实际应使用 FormData 和 axios 或其他库上传文件
        const formData = new FormData();
        formData.append('image', this.post.image);
        const config = {
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: progressEvent => {
            this.uploadProgress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
          },
        };
        try {
          const response = await Server.post('/api/upload', formData, config);
          // 假设上传成功后返回了图片URL，你可以将其保存到post对象中
          this.post.imageUrl = response.data.url;
        } catch (error) {
          console.error('图片上传失败:', error);
        } finally {
          this.uploadProgress = 0; // 重置进度条
        }
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