<template>
  <view class="indexPage" style="padding-top: 13%; padding-left: 5%; padding-right: 5%; height: fit-content">
    <view style="margin-bottom: 20%">
      <img src="../../static/fh.svg" style="width: 35rpx; height: 35rpx; margin-right: 5%;" @click="goBack" alt/> <text style="font-weight: bold; vertical-align: center;">管理员工具</text>
    </view>
    <view class="itemList">
      <view class="itembox" style="height: fit-content; background-color: #F0F0F0; padding: 2% 5%">
        <view style="font-weight: bold; display: flex; justify-content: space-between; padding: 3%" @click="switchUserDisplay">
          用户管理 <span>{{ expandUser ? "-" : "+" }}</span>
        </view>
        <view v-if="expandUser" style="height: 10rpx"></view>
        <view v-for="(item, index) in users" :key="index" v-if="expandUser">
          <view class="itembox" style="height: fit-content; width: inherit; background-color: #3A3A3A; color: white; margin: 3%; padding: 3%; font-size: 15px">
            <view style="font-weight: bold; color: grey; margin: 2%">{{ item.id }}</view>
            <view style="display: flex; justify-content: space-between; margin: 2%">
              <text>显示名</text><input v-model="users[index].display" style="background-color: white; color: black; text-align: right; padding: 1%" />
            </view>
            <view style="display: flex; justify-content: space-between; margin: 2%">
              <text>权限</text><input v-model="users[index].permission" style="background-color: white; color: black; text-align: right; padding: 1%" />
            </view>
            <view style="height: 50rpx">
              <button style="background-color: #82007E; color: white; padding: 0 3%; font-size: 11px; height: 50rpx; width: fit-content; float: right" @click="alterUserInfo(index)">提交修改</button>
            </view>
          </view>
        </view>
      </view>
    </view>

  </view>

</template>
<script>
export default {
  name: "adminTool",
  data() {
    return {
      expandUser: false,
      users: []
    }
  },
  onShow() {
    wx.request({
      url: "https://nkapi.ememememem.space/query/user",
      method: "POST",
      data: {
        "cond": {}
      },
      success: (res) => {
        this.users = res.data;
      }
    })
  },
  methods: {
    goBack() {
      uni.navigateBack({
        delta: 1
      })
    },
    switchUserDisplay() {
      this.expandUser = !this.expandUser
    },
    alterUserInfo(index) {
      wx.showToast({
        title: "请求服务器...",
        icon: "loading",
        duration: 3000
      })
      if (this.users[index].permission.charAt(this.users[index].permission.length - 1) === ',')
        this.users[index].permission = this.users[index].permission.substring(0, this.users[index].permission.length - 1);
      wx.request({
        url: "https://nkapi.ememememem.space/alter/user",
        method: "POST",
        data: {
          "uid": this.users[index].id,
          "display": this.users[index].display,
          "permission": this.users[index].permission.split(","),
        },
        success: (res) => {
          wx.showToast({
            title: "修改成功！",
            icon: "success",
            duration: 2000
          })
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