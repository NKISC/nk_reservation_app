<template>
  <view class="indexPage" style="padding-top: 24rpx; padding-left: 5%; padding-right: 5%; height: fit-content">
    <view style="margin-bottom: 40rpx">
      <img src="../../static/fh.svg" style="width: 35rpx; height: 35rpx; margin-right: 5%;" @click="goBack" alt/> <text style="font-weight: bold; vertical-align: center;">获取权限</text>
    </view>
    <view class="form-card">
    <input v-model="password" placeholder="输入权限密码..." style="width: inherit; border-radius: 20rpx; margin: 5% 1%; padding: 1% 5%">
    <view class="form-actions" style="display: flex; justify-content: space-between; margin: 5% 2%">
      <span style="color: grey; font-size: 22rpx">可向相关老师索取权限密码</span>
      <span><button style="background-color: #82007E; color: white; padding: 0 3%; font-size: 11px; height: 50rpx; width: 80rpx; float: right" @click="submitPassword">获取</button></span>
    </view>
    </view>
  </view>

</template>
<script>
export default {
  data() {
    return {
      userInfo: {},
      password: "",
    }
  },
  onLoad() {
    this.userInfo = uni.getStorageSync("userInfo");
  },
  methods: {
    goBack() {
      uni.navigateBack({
        delta: 1
      })
    },
    submitPassword() {
      wx.showToast({
        title: "请求服务器...",
        icon: "loading",
        duration: 3000
      })
      wx.request({
        url: "https://nkapi.ememememem.space/grant_access/",
        method: "POST",
        data: {
          uid: this.userInfo.id,
          display: this.userInfo.display,
          password: this.password,
        },
        success: (res) => {
          if (res.data.success) {
            uni.navigateBack({
              delta: 1
            });
            setTimeout(function () {
              wx.showToast({
                title: "权限已获取！",
                icon: "success",
                duration: 3000
              })
            }, 1000);
          }
          else {
            wx.showToast({
              title: "密码错误...",
              icon: "error",
              duration: 3000
            })
          }
        }
      })
    }
  }
}
</script>
<style scoped lang="scss">
.indexPage {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: #f7f5f8;
  padding-top: calc(var(--status-bar-height, 0px) + env(safe-area-inset-top) + 24rpx) !important;
  overflow-y: auto;
  padding-bottom: env(safe-area-inset-bottom);
  color: #29232c;
  .form-card { background: #fff; border: 1px solid #eee8f0; border-radius: 12rpx; box-shadow: 0 2rpx 8rpx rgba(87,27,72,.08); padding: 24rpx; }
  input { background: #fff !important; border: 1px solid #e7e1e9 !important; border-radius: 12rpx !important; margin: 12rpx 0 !important; height: 88rpx; line-height: 48rpx; padding: 20rpx 24rpx !important; box-sizing: border-box; }
  button { background: #82007e; color: #fff; border: 0; border-radius: 12rpx; min-width: 120rpx; }
}
</style>
