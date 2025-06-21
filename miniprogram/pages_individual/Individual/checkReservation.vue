<template>
  <view class="indexPage">
    <view class="bg-container" :style="background" />
    <view class="header">
      <view class="content">
        <view class="title">{{ reservingClassroom.display }}</view>
        <view style="height: 200rpx;"></view>
        <view style="display: flex;margin-top: 20rpx;align-items: center;">
          <image src="../../static/gr_ditu2.svg" style="width: 30rpx;height: 30rpx;" />
          <view style="margin-left: 10rpx;font-size: 40rpx;color: #9D979D;font-weight: bold;">{{ reservingPlaceDisplay }}</view>
        </view>
        <view class="nav">
          <view v-for="item,index in navList" :key="index">
            <view class="navItem" v-if="item !== null">{{item}}</view>
          </view>
        </view>
        <view class="main">

          <view class="main_data">
            预约日期：
            <view>
              <view class="main_qsrq_lable" style="color: #7E7E7E">
                  {{transitionData(buildDate(new Date(checkingRecord.time_stamp * 1000)))}} {{ checkingRecord.noon ? "中午" : "下午" }}
              </view>
            </view>
          </view>
        </view>
        <view style="font-weight: normal; font-size: 20rpx;
                color: white; background-color: orange; border-radius: 20rpx; width: fit-content; padding: 0.5% 2%; margin-top: 3%"
              v-if="cycRecordIds.find(group => group['record_id'].includes(checkingRecord.id.toString() + ','))">
          周期
        </view>
      </view>
    </view>
    <view class="footer">
      <view style="width: 160rpx; height: 40rpx; padding: 10rpx; background-color: #82007E; color: white; text-align: center; border-radius: 25rpx" @click="goBack">返回列表</view>
      <view style="width: 160rpx; height: 40rpx; padding: 10rpx; background-color: #82007E; color: white; text-align: center; border-radius: 25rpx" @click="goAlter">修改预约</view>
      <view style="width: 160rpx; height: 40rpx; padding: 10rpx; background-color: #82007E; color: white; text-align: center; border-radius: 25rpx" @click="goConfirmCancel">取消预约</view>
    </view>
    <MyDialog v-if="showCancel" @close='closeCancel'>
      <view style="margin-bottom: 40rpx;">
        <view style="font-size: 33rpx;font-weight: bold;margin: auto">确认取消预约吗？</view>
      </view>
      <image src="../../static/queding.svg" style="width: 300rpx;height: 100rpx;" @click='confirmCancel' />

    </MyDialog>
    <view class="mark" v-if="showCycOpt">
      <view style="display: flex;flex-direction: column;">
        <view class="box" style="height: 400rpx; padding: 10%; margin: -200rpx; width: 550rpx">
          该预约为周期预约。<br/>要删除以后的预约吗？
          <view style="margin-top: 100rpx; display: flex; justify-content: space-between; width: 100%">
            <view style="width: 200rpx; height: 40rpx; padding: 10rpx; background-color: #82007E; color: white; text-align: center; border-radius: 25rpx" @click="confirmCancel(true)">仅本次预约</view>
            <view style="width: 200rpx; height: 40rpx; padding: 10rpx; background-color: #82007E; color: white; text-align: center; border-radius: 25rpx" @click="confirmCancelCyc">此后所有预约</view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import MyDialog from '@/components/MyDialog.vue';
import uniDatetimePicker from '@/uni_modules/uni-datetime-picker/components/uni-datetime-picker/uni-datetime-picker';
import {
  formatDate
} from '../../pages/Individual/Individual.js'
export default {
  components: {
    MyDialog,
    uniDatetimePicker
  },
  data() {
    const {
      today,
      tomorrow,
      tomorrows
    } = formatDate();
    return {
      showCancel: false,
      showCycOpt: false,
      tag_display: {},
      checkingRecord: {},
      reservingClassroom: {},
      reservingPlaceDisplay: "",
      navList: [],
      navMode: '',
      list: [{
        name: 'apple',
        disabled: false
      },
        {
          name: 'banner',
          disabled: false
        },
      ],
      form: {
        timePeriod: "",
        isCyclic: [],
        cyclicMethod: "",
        singleStart: tomorrow,
        singleEnd: tomorrow,
      },
      datetimeStart: today,
      datetimeEnd: tomorrows,
      limitDate: new Date(),
      background: "",
      cycRecordIds: [],
    }
  },
  onShow() {
    this.limitDate = new Date();
    this.limitDate.setDate(new Date().getDate() + 60);
    this.limitDate = this.buildDate(this.limitDate);
    this.tag_display = uni.getStorageSync('tag_display');
    this.checkingRecord = uni.getStorageSync('checkingRecord');

    wx.request({
      url: "https://nkapi.ememememem.space/query/classroom",
      method: "POST",
      data: {
        cond: {"id": this.checkingRecord.classroom_id}
      },
      success: (res) => {
        this.reservingClassroom = res.data[0];
        this.background = "background: url(https://nkapi.ememememem.space/img/" + this.reservingClassroom.pic_url + ") no-repeat";
        this.navList = this.reservingClassroom.func_tag.split(",");
        this.navList.pop();
        this.navList = this.navList.map(x => this.tag_display[x]);
        wx.request({
          url: "https://nkapi.ememememem.space/query/display",
          method: "POST",
          data: {
            cond: {"query": [[this.reservingClassroom.place, "place"]]}
          },
          success: (res) => {
            this.reservingPlaceDisplay = res.data[0]
          }
        })
      }
    })
    wx.request({
      url: "https://nkapi.ememememem.space/query/cyclical",
      method: "POST",
      data: {
        initiator: ""
      },
      success: (res) => {
        this.cycRecordIds = res.data
      }
    })
  },
  methods: {
    buildDate: (d) =>
        `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`,
    transitionData(dateStr) {
      const [year, month, day] = dateStr.split('-');
      const formattedDate = `${year}年${month}月${day}日`;
      return formattedDate
    },
    changeStart() {
      if (new Date(this.form.singleEnd) < new Date(this.form.singleStart)) this.form.singleEnd = this.buildDate(new Date(this.form.singleStart));
      formatDate()
    },
    checkboxChange(e) {
      if (!(e > 0)) {
        this.form.cyclicMethod = ""
      }
    },
    setNavMode(mode) {
      this.navMode = mode
    },
    goBack() {
      // uni.navigateTo({
      // 	url: `/pages/Individual/Individual`,
      // })
      uni.navigateBack({
        delta: 1
      });
    },
    goConfirmCancel() {
      this.showCancel = true;
    },
    closeCancel() {
      this.showCancel = false;
    },
    confirmCancel(bypassCyc = false) {
      if (!bypassCyc && this.cycRecordIds.find(group => group['record_id'].includes(this.checkingRecord.id.toString() + ','))) {
        this.showCycOpt = true
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
            cond: {"id": this.checkingRecord.id}
          },
          success: (res) => {
            uni.navigateBack({
              delta: 1
            });
            setTimeout(function () {
              wx.showToast({
                title: "删除成功",
                icon: "success",
                duration: 3000
              });
            }, 1000);
          }
        })
      }
    },
    confirmCancelCyc() {
      wx.showToast({
        title: "请求服务器...",
        icon: "loading",
        duration: 10000,
      })
      wx.request({
        url: "https://nkapi.ememememem.space/delete/cyclical",
        method: "POST",
        data: {
          initiator: this.checkingRecord.id,
        },
        success: (res) => {
          uni.navigateBack({
            delta: 1
          });
          setTimeout(function () {
            wx.showToast({
              title: "删除成功",
              icon: "success",
              duration: 3000
            });
          }, 1000);
        }
      })
    },
    goAlter() {
      uni.setStorageSync("alteringRecord", this.checkingRecord);
      uni.setStorageSync("alteringClassroom", this.reservingClassroom);
      uni.navigateTo({
        url: "/pages_individual/Individual/alterReservationDetails",
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.tag {
  background-color: #f5f5f5;
  padding: 5rpx 20rpx;
  box-sizing: border-box;
  font-size: 25rpx;
  color: #9E9E9E;
}

.mark_data {
  margin-bottom: 40rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  .mark_data_title {
    font-size: 30rpx;
    font-weight: bold;
  }

  .mark_data_sj {
    font-size: 28rpx;
    color: #9E9E9E;
  }
}

.data {
  color: #82007E !important;
}

.bg-container {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: url('https://cdn.jsdelivr.net/gh/emforinfinityenergy/contents/picture/gr_bg.jpeg') no-repeat;
  background-size: 100%;
  z-index: -100;
  height: 32%;
  overflow: hidden;
}

.indexPage {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;

  .header {
    width: 100%;
    height: 83%;
    padding: 0 40rpx;
    box-sizing: border-box;
  }

  .title {
    width: 100%;
    height: 200rpx;
    display: flex;
    align-items: flex-end;
    font-size: 50rpx;
    font-weight: bold;
    color: white;
  }

  .nav {
    margin-top: 30rpx;
    display: flex;

    .navItem {
      background: #F5F5F5;
      color: #9E9E9E;
      border-radius: 24rpx;
      margin-right: 20rpx;
      padding: 5rpx 35rpx;
      box-sizing: border-box;
      font-size: 28rpx;
    }

    .navItem.active {
      background: #EBE9FF;
      color: #82007E;
      font-weight: bold;
    }
  }

  .main {
    margin-top: 30rpx;
    width: 100%;
    // height: 550rpx;
    background-color: #F9F5F7;
    padding: 30rpx;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    // justify-content: space-around;

    .main_data {
      font-size: 36rpx;
      font-weight: bold;
    }

    .main-label {
      font-weight: bold;
      font-size: 30rpx;
    }

    .main_sjd {
      color: #9E9E9E;
      font-weight: bold;
      font-size: 25rpx;
    }

    .main_cfpl {
      margin-bottom: 10rpx;
      font-weight: bold;
      font-size: 28rpx;
      color: #414141;
    }

    .main_qsrq {
      font-weight: bold;
      font-size: 28rpx;
      color: #414141;
      margin-top: 20rpx;
      margin-bottom: 10rpx;
    }

    .main_qsrq_lable {
      height: 50rpx;
      line-height: 50rpx;
      color: #4e00a0;
      font-size: 30rpx;
    }
  }

  .footer {
    margin-top: 90rpx;
    width: 100%;
    height: 10%;
    border-top: 3px solid #eaeaea;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 50rpx;
    box-sizing: border-box;
  }
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
  }
}
</style>