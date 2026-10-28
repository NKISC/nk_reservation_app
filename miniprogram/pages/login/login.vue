<template>
	<view class="loginPage">
		<view class="hero"></view>
		<view class="login-card">
			<view class="card-title">欢迎使用</view>
			<view class="card-copy">微信登录由应用自动完成，请稍后继续使用。</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() { return {}; },
		created() {},
		methods: {}
	}
</script>

<style lang="scss" scoped>
	.loginPage {
		position: absolute;
		top: 0;
		right: 0;
		bottom: 0;
		left: 0;
		overflow: auto;
		padding-top: calc(var(--status-bar-height, 0px) + env(safe-area-inset-top) + 16rpx);
		box-sizing: border-box;
		padding-bottom: env(safe-area-inset-bottom);
		background: #f7f5f8;
	}
	.hero { height: 0; }
	.login-card {
		margin: 0 32rpx;
		padding: 40rpx 36rpx;
		background: #fff;
		border: 1px solid #eee8f0;
		border-radius: 12rpx;
		box-shadow: 0 2rpx 8rpx rgba(87, 27, 72, 0.08);
	}
	.card-title { color: #82007E; font-size: 36rpx; font-weight: bold; }
	.card-copy { margin-top: 14rpx; color: #9E9E9E; font-size: 27rpx; line-height: 1.6; }
</style>
