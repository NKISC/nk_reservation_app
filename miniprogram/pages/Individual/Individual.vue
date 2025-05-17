<template>
	<view class="indexPage">
		<view class="header">
			<view class="tx_bj"></view>
			<view class="user_title">qwe</view>
			<view class="class_title">七年级六班</view>
		</view>
		<view class="content">
			<view class="nav">
				<view v-for="(item,index) in navList" :key="index">
					<view class="navItem" :class="{ active: navMode === item }" @click="setNavMode(item)">
						{{item}}
						<span class="line"></span>
					</view>

				</view>
			</view>
			<view class="itemList" v-if="navMode === '我的预约'">
				<view v-for="item,index in list" :key="index" class="itembox">
					<view style="display: flex;justify-content: space-between;height: 50rpx;align-items: center;">
						<view>{{item.name}}</view>
						<view>{{item.sj}}</view>
					</view>
					<view style="display: flex;position: relative;">
						<image src="../../static/gr_ditu3.svg" style="width: 120rpx;height: 50rpx;">
							<view style="position: absolute;left: 40rpx;top:7rpx;font-size: 25rpx;color: #830080;">{{item.js}}</view>
							<view style="display: flex;margin-top: 5rpx;">
								<view v-for="i,indexs in item.nav" :key="indexs">
									<view class="tabs">
										{{i}}
									</view>
								</view>
							</view>
					</view>
					<view style="display: flex;justify-content: flex-end;height: 80rpx;margin-top: 10rpx;">
						<view @click="toDetails" class="checkBtn">查看</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				navList: ['个人信息', '我的预约', '设置'],
				navMode: '我的预约',
				list: [{
						name: '科技馆',
						sj: "2023-09-14 下午",
						js: "204",
						nav: ['舞蹈', '标签1'],
					},
					{
						name: '科技馆',
						sj: "2023-09-15 下午",
						js: "204",
						nav: ['舞蹈', '标签1'],
					},
					{
						name: '科技馆',
						sj: "2023-09-15 下午",
						js: "204",
						nav: ['舞蹈', '标签1'],
					},
					{
						name: '科技馆',
						sj: "2023-09-15 下午",
						js: "204",
						nav: ['舞蹈', '标签1'],
					},
				],
			}
		},
		methods: {
			setNavMode(mode) {
				this.navMode = mode
			},
			toDetails() {
				uni.navigateTo({
					url: `/pages/Individual/ReservationDetails`,
				})
			},
		}
	}
</script>

<style lang="scss" scoped>
	.indexPage {
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
		background: url('../../static/gr_bg.svg') no-repeat;
		background-size: 100%;

		.header {
			width: 100%;
			height: 650rpx;
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;

			.tx_bj {
				width: 200rpx;
				height: 200rpx;
				background: #fff;
				border-radius: 50%;
				margin-bottom: 10rpx;
			}

			.user_title {
				color: #000;
				font-size: 40rpx;
				font-weight: bold;
				margin-bottom: 10rpx;
			}

			.class_title {
				color: #9E9E9E;
				font-size: 28rpx;
			}
		}

		.content {
			margin-top: -100rpx;
			width: 100%;
			height: calc(100% - 550rpx);

			.nav {
				width: 100%;
				height: 80rpx;
				display: flex;
				justify-content: space-evenly;
				align-items: center;
				font-size: 36rpx;
				font-weight: bold;
				color: #7E7E7E;

				.navItem {
					display: flex;
					justify-content: center;
					width: 100%;
					height: 80rpx;
					position: relative;

					.line {
						position: absolute;
						bottom: 0;
						width: 15rpx;
						height: 15rpx;
						background-color: #830080;
						margin: 10rpx 0;
						border-radius: 6px;
						opacity: 0;
						transition: opacity 0.3s ease;
					}

					&.active .line {
						opacity: 1;
					}
				}

				.navItem.active {
					color: #000;
					font-weight: bold;
				}
			}

			.itemList {
				width: 100%;
				height: calc(100% - 80rpx);
				overflow: auto;
				display: flex;
				flex-direction: column;
				align-items: center;
				margin-top: 20rpx;

				.itembox {
					width: 90%;
					height: 200rpx;
					background-color: #F9F5F7;
					margin-bottom: 30rpx;
					padding: 20rpx;
					box-sizing: border-box;
				}
			}
		}

		.tabs {
			background-color: #fff;
			font-size: 25rpx;
			margin-left: 10rpx;
			color: #9E9E9E;
			width: 80rpx;
			height: 40rpx;
			line-height: 40rpx;
			text-align: center;
		}

		.checkBtn {
			width: 150rpx;
			height: 50rpx;
			line-height: 50rpx;
			background-color: #82007E;
			color: #fff;
			text-align: center;
			border-radius: 12rpx;
		}
	}
</style>