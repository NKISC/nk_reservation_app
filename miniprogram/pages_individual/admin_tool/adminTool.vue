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
        <u-search placeholder="用户ID/显示名" v-model="userSearch" :clearabled="true" :show-action="false" v-if="expandUser"/>
        <u-search placeholder="权限代码" v-model="permSearch" :clearabled="true" :show-action="false" v-if="expandUser"/>
        <view v-for="(item, index) in users" :key="index" v-if="expandUser">
          <view class="itembox" style="height: fit-content; width: inherit; background-color: #3A3A3A; color: white; margin: 3%; padding: 3%; font-size: 15px"
          v-if="(item.id.includes(userSearch) || item.display.includes(userSearch)) && item.permission.includes(permSearch)">
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

    <view class="itemList">
      <view class="itembox" style="height: fit-content; background-color: #F0F0F0; padding: 2% 5%">
        <view style="font-weight: bold; display: flex; justify-content: space-between; padding: 3%" @click="switchReservationDisplay">
          预约管理 <span>{{ expandReservation ? "-" : "+" }}</span>
        </view>
        <view v-if="expandReservation" style="height: 10rpx" />
        <view v-if="expandReservation" class="itembox" style="display: flex; justify-content: center; height: fit-content; width: inherit; background-color: #3A3A3A; color: white; margin: 3%; padding: 3%; font-size: 15px">
          <button style="background-color: #82007E; color: white; padding: 0 3%; font-size: 11px; height: 50rpx; width: fit-content; float: right" @click="generateSchedule">生成本周排班表</button>
          <button style="background-color: #82007E; color: white; padding: 0 3%; font-size: 11px; height: 50rpx; width: fit-content; float: right" @click="generateStatistics">查看社团预约数据</button>
        </view>
        <view v-for="(item, index) in reservations" :key="index" v-if="expandReservation">
          <view class="itembox" style="height: fit-content; width: inherit; background-color: #3A3A3A; color: white; margin: 3%; padding: 3%; font-size: 15px">
            <view style="font-weight: bold; color: grey; margin: 2%">{{ item.id }}</view>
            <view style="display: flex; justify-content: space-between; margin: 2%">
              <text>教室</text><text style="color: grey">{{ classrooms.find(x => x.id === item.classroom_id).display }}</text>
            </view>
            <view style="display: flex; justify-content: space-between; margin: 2%">
              <text>时间</text><text style="color: grey;">{{ buildDate(new Date(item.time_stamp * 1000)) }} {{ item.noon ? "中午" : "下午" }}</text>
            </view>
            <view style="display: flex; justify-content: space-between; margin: 2%">
              <text>预约用户ID后8位</text><text style="color: grey;">{{ item.applicant_id.slice(-8) }}</text>
            </view>
            <view style="display: flex; justify-content: space-between; margin: 2%">
              <text>预约用户显示名</text><text style="color: grey;">{{ users.find(x => x.id === item.applicant_id).display }}</text>
            </view>
            <view style="font-weight: normal; font-size: 20rpx;
                color: white; background-color: orange; border-radius: 20rpx; width: fit-content; padding: 0.5% 2%; margin-top: 3%"
                  v-if="cycRecordIds.find(group => group['record_id'].includes(item.id.toString() + ','))">
              周期
            </view>
            <view style="height: 50rpx">
              <button style="background-color: #82007E; color: white; padding: 0 3%; font-size: 11px; height: 50rpx; width: fit-content; float: right" @click="confirmCancel(index, false)">取消预约</button>
            </view>
          </view>
        </view>
      </view>
      <view class="mark" v-if="showCycOpt">
        <view style="display: flex;flex-direction: column;">
          <view class="box" style="height: 400rpx; padding: 10%; margin: -200rpx; width: 550rpx">
            该预约为周期预约。<br/>要删除以后的预约吗？
            <view style="margin-top: 100rpx; display: flex; justify-content: space-between; width: 100%">
              <view style="width: 200rpx; height: 40rpx; padding: 10rpx; background-color: #82007E; color: white; text-align: center; border-radius: 25rpx" @click="confirmCancel(deleting_index, true)">仅本次预约</view>
              <view style="width: 200rpx; height: 40rpx; padding: 10rpx; background-color: #82007E; color: white; text-align: center; border-radius: 25rpx" @click="confirmCancelCyc(deleting_index)">此后所有预约</view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <view class="itemList">
      <view class="itembox" style="height: fit-content; background-color: #F0F0F0; padding: 2% 5%">
        <view style="font-weight: bold; display: flex; justify-content: space-between; padding: 3%" @click="switchPpmDisplay">
          权限密码管理 <span>{{ expandPPM ? "-" : "+" }}</span>
        </view>
        <view v-if="expandPPM" style="height: 10rpx" />
        <view v-if="expandPPM" class="itembox" style="display: flex; justify-content: center; height: fit-content; width: inherit; background-color: #3A3A3A; color: white; margin: 3%; padding: 3%; font-size: 15px">
          <button style="background-color: #82007E; color: white; padding: 0 3%; font-size: 11px; height: 50rpx; width: fit-content; float: right" @click="go_create_ppm">创建新密码</button>
        </view>
        <view v-for="(item, index) in ppm" :key="index" v-if="expandPPM">
          <view class="itembox" style="height: fit-content; width: inherit; background-color: #3A3A3A; color: white; margin: 3%; padding: 3%; font-size: 15px">
            <view style="display: flex; justify-content: space-between; margin: 2%">
              <text>密码</text><text style="color: grey;" >{{ ppm[index].password }}</text>
            </view>
            <view style="display: flex; justify-content: space-between; margin: 2%">
              <text>权限</text><text style="color: grey;" >{{ ppm[index].permission }}</text>
            </view>
            <view style="display: flex; justify-content: space-between; margin: 2%">
              <text>一次性</text><text style="color: grey;" >{{ ppm[index].isDisposable ? "是" : "否"}}</text>
            </view>
            <view style="height: 50rpx">
              <button style="background-color: #82007E; color: white; padding: 0 3%; font-size: 11px; height: 50rpx; width: fit-content; float: right" @click="delete_ppm(index)">删除密码</button>
            </view>
          </view>
        </view>
      </view>
      <view class="mark" v-if="showPpmCreate">
        <view class="itembox" style="height: fit-content; width: 80%; background-color: #3A3A3A; color: white; margin: 3%; padding: 3%; font-size: 15px">
          <view style="display: flex; justify-content: space-between; margin: 2%">
            <text>密码</text><input v-model="new_password" style="background-color: white; color: black; text-align: right; padding: 1%" />
          </view>
          <view style="display: flex; justify-content: space-between; margin: 2%">
            <text>权限</text><input v-model="new_permission" style="background-color: white; color: black; text-align: right; padding: 1%" />
          </view>
          <view style="display: flex; justify-content: space-between; margin: 2%">
            <text>一次性</text><u-switch v-model="new_isDisposable" active-color="#82007E"></u-switch>
          </view>
          <view style="height: 50rpx; display: flex; justify-content: space-between;">
            <button style="background-color: #82007E; color: white; padding: 0 3%; font-size: 11px; height: 50rpx; width: fit-content; float: right" @click="cancel_ppm_create">取消</button>
            <button style="background-color: #82007E; color: white; padding: 0 3%; font-size: 11px; height: 50rpx; width: fit-content; float: right" @click="create_ppm">创建</button>
          </view>
        </view>
      </view>
    </view>
<!--
<view class="itembox" style="height: fit-content; width: inherit; background-color: #3A3A3A; color: white; margin: 3%; padding: 3%; font-size: 15px">
            <view style="display: flex; justify-content: space-between; margin: 2%">
              <text>密码</text><input v-model="ppm[index].password" style="background-color: white; color: black; text-align: right; padding: 1%" />
            </view>
            <view style="display: flex; justify-content: space-between; margin: 2%">
              <text>权限</text><input v-model="ppm[index].permission" style="background-color: white; color: black; text-align: right; padding: 1%" />
            </view>
            <view>
              <u-switch v-model="ppm[index].isDisposable"></u-switch>
            </view>
          </view>
-->
  </view>

</template>
<script>
import USwitch from "../../uni_modules/uview-ui/components/u-switch/u-switch.vue";
import UButton from "../../uni_modules/uview-ui/components/u-button/u-button.vue";

export default {
  name: "adminTool",
  components: {UButton, USwitch},
  data() {
    return {
      expandUser: false,
      expandReservation: false,
      expandPPM: false,
      users: [],
      ppm: [],
      userSearch: "",
      permSearch: "",
      reservations: [],
      classrooms: [],
      cycRecordIds: [],
      showCycOpt: false,
      showPpmCreate: false,
      new_password: "",
      new_permission: "",
      new_isDisposable: false,
      deleting_index: 0,
      buildDate: (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`,
    }
  },
  onLoad() {
    wx.request({
      url: "https://nkapi.ememememem.space/query/classroom",
      method: "POST",
      data: {
        "cond": {}
      },
      success: (res) => {
        this.classrooms = res.data
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
    wx.request({
      url: "https://nkapi.ememememem.space/query/ppm/",
      method: "GET",
      success: (res) => {
        this.ppm = res.data
      }
    })
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
    wx.request({
      url: "https://nkapi.ememememem.space/query/record",
      method: "POST",
      data: {
        "cond": {"by_id": true}
      },
      success: (res) => {
        this.reservations = res.data;
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
    switchReservationDisplay() {
      this.expandReservation = !this.expandReservation
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
    },
    confirmCancel(index, bypassCyc) {
      if (!bypassCyc && this.cycRecordIds.find(group => group['record_id'].includes(this.reservations[index].id.toString() + ',')) !== undefined) {
        this.showCycOpt = true
        this.deleting_index = index
      }
      else {
        wx.showToast({
          title: "请求服务器...",
          icon: "loading",
          duration: 10000,
        })
        wx.request({
          url: "https://nkapi.ememememem.space/delete/record",
          method: "POST",
          data: {
            cond: {"id": this.reservations[index].id}
          },
          success: (res) => {
            setTimeout(function () {
              wx.showToast({
                title: "删除成功",
                icon: "success",
                duration: 3000
              });
            }, 1000);
            this.showCycOpt = false;
            this.reservations.splice(index, 1);
          }
        })
      }
    },
    confirmCancelCyc(index) {
      wx.showToast({
        title: "请求服务器...",
        icon: "loading",
        duration: 10000,
      })
      wx.request({
        url: "https://nkapi.ememememem.space/delete/cyclical",
        method: "POST",
        data: {
          initiator: this.reservations[index].id.toString(),
        },
        success: (res) => {
          this.showCycOpt = false;
          setTimeout(function () {
            wx.showToast({
              title: "删除成功",
              icon: "success",
              duration: 3000
            });
          }, 1000);
          wx.request({
            url: "https://nkapi.ememememem.space/query/record",
            method: "POST",
            data: {
              "cond": {"by_id": true}
            },
            success: (res) => {
              this.reservations = res.data;
            }
          })
        }
      })
    },
    generateSchedule() {
      wx.showToast({
        title: "请求服务器...",
        icon: "loading",
        duration: 3000
      })
      wx.request({
        url: "https://nkapi.ememememem.space/query/generate_schedule/",
        method: "GET",
        success: (res) => {
          wx.showToast({
            title: "生成成功！",
            icon: "success",
            duration: 2000
          })
          wx.downloadFile({
            url: "https://nkapi.ememememem.space/query/schedule/",
            success: (res) => {
              wx.openDocument({
                filePath: res.tempFilePath,
                fileType: "xlsx",
                showMenu: true
              })
            }
          })
        }
      })
    },
    generateStatistics() {
      wx.showToast({
        title: "请求服务器...",
        icon: "loading",
        duration: 3000
      })
      wx.request({
        url: "https://nkapi.ememememem.space/query/generate_statistics/",
        method: "GET",
        success: (res) => {
          wx.showToast({
            title: "生成成功！",
            icon: "success",
            duration: 2000
          })
          wx.previewImage({
            urls: ["https://nkapi.ememememem.space/query/statistics?time=" + new Date().getTime()],
          })
        }
      })
    },
    delete_ppm(index) {
      wx.showToast({
        title: "请求服务器...",
        icon: "loading",
        duration: 3000
      })
      wx.request({
        url: "https://nkapi.ememememem.space/delete/ppm/",
        method: "POST",
        data: {
          "cond": {"password": this.ppm[index].password}
        },
        success: (res) => {
          wx.showToast({
            title: "删除成功！",
            icon: "success",
            duration: 2000
          })
          this.ppm.splice(index, 1)
        }
      })
    },
    go_create_ppm() {
      this.showPpmCreate = true;
    },
    cancel_ppm_create() {
      this.showPpmCreate = false;
      this.new_permission = "";
      this.new_password = "";
      this.new_isDisposable = false;
    },
    create_ppm() {
      if (this.new_permission.includes(" ") || this.new_password.includes(" ") || this.new_password === "" || this.new_permission === "") {
        wx.showToast({
          title: "输入包含空格！",
          icon: "error",
          duration: 3000
        })
        return
      }
      wx.showToast({
        title: "请求服务器...",
        icon: "loading",
        duration: 3000
      })
      wx.request({
        url: "https://nkapi.ememememem.space/addition/ppm/",
        method: "POST",
        data: {
          "cond": {"password": this.new_password, "isDisposable": this.new_isDisposable, "permission": this.new_permission},
        },
        success: (res) => {
          wx.showToast({
            title: "添加成功！",
            icon: "success",
            duration: 2000
          })
          wx.request({
            url: "https://nkapi.ememememem.space/query/ppm/",
            method: "GET",
            success: (res) => {
              this.ppm = res.data
            }
          })
        }
      })
      this.showPpmCreate = false;
    },
    switchPpmDisplay() {
      this.expandPPM = !this.expandPPM;
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