<template>
  <view class="indexPage" style="padding-top: 13%; padding-left: 5%; padding-right: 5%; height: fit-content">
    <view style="margin-bottom: 20%">
      <img src="../../static/fh.svg" style="width: 35rpx; height: 35rpx; margin-right: 5%;" @click="goBack" alt/> <text style="font-weight: bold; vertical-align: center;">获取权限</text>
    </view>
    <input v-model="password" placeholder="输入权限密码..." style="width: inherit; border: black solid 2px; border-radius: 20rpx; margin: 5% 1%; padding: 1% 5%">
    <view style="display: flex; justify-content: space-between; margin: 5% 2%">
      <span style="color: grey; font-size: 22rpx">可向相关老师索取权限密码</span>
      <span><button style="background-color: #82007E; color: white; padding: 0 3%; font-size: 11px; height: 50rpx; width: 80rpx; float: right" @click="submitPassword">获取</button></span>
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
      wx.request({
        url: "https://nkapi.ememememem.space/grant_access/",
        method: "POST",
        data: {
          uid: this.userInfo.id,
          display: this.userInfo.display,
          password: this.password,
        },
        success: (res) => {
          if (res.success) {
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
  background-size: 100%;
}
</style>