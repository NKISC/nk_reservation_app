<template>
	<view class="mark">
		<view style="display: flex;flex-direction: column;">
			<view class="box">
				<slot> </slot>
			</view>
		</view>
		<view class="close">
			<view class="clostBtn" @click="close">
				<u-icon name="close" color="#fff" size="40"></u-icon>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {}
		},
		methods: {
			close() {
				this.$emit('close')
			},
		}
	}
</script>

<style lang="scss" scoped>
	.mark {
		z-index: 1000;
		opacity: 1;
		position: absolute;
		height: 100vh;
		width: 100%;
		background: rgba(0, 0, 0, 0.25);
		top: 0;
		left: 0;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		.box {
			width: 500rpx;
			height: 700rpx;
			background-color: #fff;
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;
		}

		.close {
			margin-top: 50rpx;
			width: 500rpx;
			height: 100rpx;
			display: flex;
			align-items: center;
			justify-content: center;

			.clostBtn {
				width: 100rpx;
				height: 100%;
				border: 2px solid #fff;
				border-radius: 50%;
				display: flex;
				justify-content: center;
			}
		}
	}
</style>