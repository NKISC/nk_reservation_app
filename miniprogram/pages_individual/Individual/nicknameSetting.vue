<template>
  <view class="indexPage" style="padding-top: 13%; padding-left: 5%; padding-right: 5%; height: fit-content">
    <view style="margin-bottom: 20%">
      <img src="../../static/fh.svg" style="width: 35rpx; height: 35rpx; margin-right: 5%;" @click="goBack" alt/> <text style="font-weight: bold; vertical-align: center;">昵称设置</text>
    </view>
    <view style="display: flex; justify-content: space-between; margin: 2%">
      <text style="font-weight: bold">昵称</text><input v-model="user.display" style="background-color: white; color: black; text-align: right; padding: 1%" />
    </view>
    <u-button style="background-color: #82007E" text="确认" shape="circle" color="#82007E" @click="alterUserInfo"></u-button>

  </view>

</template>
<script>
import USwitch from "../../uni_modules/uview-ui/components/u-switch/u-switch.vue";
import UButton from "../../uni_modules/uview-ui/components/u-button/u-button.vue";

export default {
  name: "nicknameSetting",
  components: {UButton, USwitch},
  data() {
    return {
      user: undefined,
    }
  },
  onShow() {
    this.user = uni.getStorageSync("user");
    uni.removeStorageSync("user");
  },
  methods: {
    goBack() {
      uni.navigateBack({
        delta: 1
      })
    },
    alterUserInfo() {
      wx.showToast({
        title: "请求服务器...",
        icon: "loading",
        duration: 3000
      })
      if (this.user.permission.charAt(this.user.permission.length - 1) === ',')
        this.user.permission = this.user.permission.substring(0, this.user.permission.length - 1);
      wx.request({
        url: "https://nkapi.ememememem.space/alter/user",
        method: "POST",
        data: {
          "uid": this.user.id,
          "display": this.user.display,
          "permission": this.user.permission.split(","),
        },
        success: (res) => {
          uni.navigateBack({
            delta: 1
          })
          setTimeout(function () {
            wx.showToast({
              title: "修改成功！",
              icon: "success",
              duration: 3000
            })
          }, 100);
        }
      })
    },
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

  .mark {
    z-index: 1000;
    opacity: 1;
    position: fixed;
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
  }
}
</style>