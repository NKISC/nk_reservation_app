<template>
	<view class="indexPage">
		<view class="header">
      <button style="width: auto; padding: 0" open-type="chooseAvatar" @chooseavatar="onChooseAvatar"><u-avatar size="90" :src="avatarUrl" shape="square"></u-avatar></button>

<!--          <img class="avatar" style="height: 120%; width: 120%;" :src="avatarUrl" alt="" />-->
			<view class="user_title">{{ userInfo.display }}</view>
      <view style="color: grey; font-size: 9px">{{ uid.slice(-8) }}</view>
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
				<view v-for="(item,index) in recordList" :key="index" class="itembox">
					<view style="display: flex;justify-content: space-between;height: 50rpx;align-items: center;">
						<view>{{ recordHash[index].display }}</view>
            <view>{{ buildDate(new Date(item.time_stamp * 1000)) }} {{ item.noon ? "中午" : "下午" }}</view>
					</view>
					<view style="display: flex;position: relative;">
						<image src="../../static/gr_ditu3.svg" style="width: 120rpx;height: 50rpx;" />
							<view style="position: absolute;left: 40rpx;top:7rpx;font-size: 25rpx;color: #830080;">{{ recordPlace[index] }}</view>
							<view style="display: flex;margin-top: 5rpx;">
								<view v-for="(i,indexs) in item.nav" :key="indexs">
									<view class="tabs">
										{{i}}
									</view>
								</view>
							</view>
					</view>
          <view style="font-weight: normal; font-size: 20rpx;
                color: white; background-color: orange; border-radius: 20rpx; width: fit-content; padding: 0.5% 2%; margin-top: 3%"
                v-if="cycRecordIds.find(group => group['record_id'].includes(item.id.toString() + ','))">
            周期
          </view>
					<view style="display: flex;justify-content: flex-end;height: 80rpx" v-if="item.time_stamp >= today.getTime() / 1000">
						<view @click="toDetails(item)" class="checkBtn">查看</view>
					</view>
				</view>
			</view>

      <view v-if="navMode === '个人信息'">
        <view class="itemList">
          <view class="itembox" style="height: fit-content; background-color: #F0F0F0; padding-left: 5%; padding-right: 5%">
            <view style="font-weight: bold; display: flex; justify-content: space-between;" @click="switchPermissionDisplay">
              权限组 <span>{{ expandPermission ? "-" : "+" }}</span>
            </view>
            <view v-if="expandPermission" style="height: 10rpx"></view>
            <view v-for="(item, index) in userPermissionDisplay" :key="index" v-if="expandPermission">
              <view class="itembox" v-if="userPermissions[index] !== ''" style="height: fit-content; width: inherit">
                <view style="font-weight: bold">{{ item }}</view>
              </view>
            </view>
          </view>
        </view>
      </view>

      <view v-if="navMode === '设置'">
        <view class="itembox" v-if="userPermissions.includes('admin')" style="height: fit-content; background-color: #F0F0F0; padding: 3% 5% 3% 5%" @click="goToAdminTool">
          <view style="font-weight: bold; display: flex; justify-content: space-between;">
            管理员工具 <span> > </span>
          </view>
        </view>
        <view class="itembox" style="height: fit-content; background-color: #F0F0F0; padding: 3% 5% 3% 5%" @click="goToAccessGrant">
          <view style="font-weight: bold; display: flex; justify-content: space-between;">
            获取权限 <span> > </span>
          </view>
        </view>
      </view>
		</view>
	</view>
</template>

<script>
	import UAvatar from "../../uni_modules/uview-ui/components/u-avatar/u-avatar.vue";

  export default {
    components: {UAvatar},
		data() {
			return {
				navList: ['个人信息', '我的预约', '设置'],
				navMode: '我的预约',
        userInfo: {},
        uid: "",
        cycRecordIds: [],
        userPermissions: [],
        userPermissionDisplay: [],
        recordList: [],
        recordHash: [],
        recordPlace: [],
        today: new Date(),
        expandPermission: false,
        avatarUrl: "https://mmbiz.qpic.cn/mmbiz/icTdbqWNOwNRna42FI242Lcia07jQodd2FJGIYQfG0LAJGFxM4FbnQP6yfMxBgJ0F3YRqJCJ1aPAK2dQagdusBZg/0",
        buildDate: (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
			}
		},
    onShow() {
      this.today = new Date();
      this.today.setHours(0, 0, 0, 0);
      this.avatarUrl = wx.getStorageSync("avatarUrl");
      this.uid = wx.getStorageSync("openid");
      this.recordHash = []
      wx.request({
        url: "https://nkapi.ememememem.space/query/user",
        method: "POST",
        data: {
          cond: {"id": this.uid}
        },
        success: (res) => {
          this.userInfo = res.data[0];
          this.userPermissions = this.userInfo.permission.split(",");
          wx.request({
            url: "https://nkapi.ememememem.space/query/display",
            method: "POST",
            data: {
              cond: {"query": this.userPermissions.map(x => [x, "permission"])}
            },
            success: (rep) => {
              this.userPermissionDisplay = rep.data;
            }
          })
        }
      })
      wx.request({
        url: "https://nkapi.ememememem.space/query/record",
        method: "POST",
        data: {
          cond: {"applicant_id": this.uid}
        },
        success: (res) => {
          this.recordList = res.data;
          wx.request({
            url: "https://nkapi.ememememem.space/query/classroom",
            method: "POST",
            data: {
              cond: {}
            },
            success: (rel) => {
              for (let i = 0; i < this.recordList.length; i++)
                for (let j = 0; j < rel.data.length; j++)
                  if (rel.data[j]["id"] === this.recordList[i]["classroom_id"]) {
                    this.recordHash.push(rel.data[j]);
                    break;
                  }
              wx.request({
                url: "https://nkapi.ememememem.space/query/display",
                method: "POST",
                data: {
                  "cond": {"query": this.recordHash.map(x => [x.place, "place"])}
                },
                success: (rep) => {
                  this.recordPlace = rep.data;
                }
              })
            }
          })
        }
      })
      wx.request({
        url: "https://nkapi.ememememem.space/query/cyclical",
        method: "POST",
        data: {
          cond: {"record_id": [""]}
        },
        success: (res) => {
          this.cycRecordIds = res.data
        }
      })
    },
		methods: {
			setNavMode(mode) {
				this.navMode = mode
			},
			toDetails(record) {
        uni.setStorageSync("checkingRecord", record);
        uni.navigateTo({
					url: `/pages_individual/Individual/checkReservation`,
				})
			},
      onChooseAvatar(e) {
        this.avatarUrl = e.detail.avatarUrl;
        wx.setStorageSync("avatarUrl", this.avatarUrl);
      },
      switchPermissionDisplay() {
        this.expandPermission = !this.expandPermission;
      },
      goToAdminTool() {
        uni.navigateTo({
          url: '/pages_individual/admin_tool/adminTool',
        })
      },
      goToAccessGrant() {
        uni.setStorageSync("userInfo", this.userInfo);
        uni.navigateTo({
          url: '/pages_individual/access_grant/accessGrant',
        })
      }
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
		background: url('https://cdn.jsdelivr.net/gh/emforinfinityenergy/contents/picture/gr_bg.jpeg') no-repeat;
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