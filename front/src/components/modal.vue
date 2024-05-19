<template>
  <div class="modal-bg" v-show="show">
		<div class="modal-container">
			<div class="modal-header">
			</div>
			<div class="modal-main">
                <h2 class="uk-modal-title">ABOUT</h2>
                <div class="uk-margin-small-left uk-margin-small-bottom uk-margin-medium-top">
                    <h4>开发</h4>
                    <ul>
                        <li><span>前端:vue</span></li>
                        <li><span>后端:django</span></li>
						<li><span>文本分类:textcnn</span></li>
						<li><span>模型部署:flask</span></li>
                    </ul>
                    <ul>
                        <li><a href="https://github.com/zengjiayu119981/Capstone-project">github:zengjiayu119981</a></li>
                    </ul>
                </div>
				<button type="button" @click="close">关 闭</button>
            </div>
			
		</div>
	</div>
</template>

<script>

export default {
	props:["show",],
	setup(props,context){
		function close() {
			context.emit("hideModal");	
		}
		function submit() {
			context.emit("submit")
		}
		return {
			close,
		}
	}
};
</script>

<style scoped>
.modal-bg{
	position: fixed;
	top: 0;
	right: 0;
	bottom: 0;
	left: 0;
	display: flex;
	justify-content: center;
	align-items: center;
	background: rgba(0, 0, 0, .4);
	z-index:999;
}
.modal-container{
	border-radius: 8px;
	background: #fff;
}

.modal-main {
	padding: 20px 40px;
}

</style>