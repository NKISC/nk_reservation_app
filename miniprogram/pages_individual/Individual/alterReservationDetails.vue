<template>
  <view class="indexPage">
    <view class="bg-container" :style="background" />
    <view class="header">
      <view class="content">
        <view class="title">{{ alteringClassroom.display }}</view>
        <view style="height: 200rpx;"></view>
        <view style="display: flex;margin-top: 20rpx;align-items: center;">
          <image src="../../static/gr_ditu2.svg" style="width: 30rpx;height: 30rpx;" />
          <view style="margin-left: 10rpx;font-size: 40rpx;color: #9D979D;font-weight: bold;">{{ alteringPlaceDisplay }}</view>
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
              <view class="main_qsrq_lable">
                <uni-datetime-picker v-model="form.singleStart" type="date" :start="datetimeStart" :end="limitDate"
                                     @change='changeStart'>
                  {{transitionData(form.singleStart)}}
                </uni-datetime-picker>
              </view>
            </view>
          </view>

          <view style="height: 100rpx;margin-top: 20rpx;">
            <u-radio-group v-model="form.timePeriod" style="display: flex;justify-content: space-around;">
              <u-radio name="zw" :active-color="'#82007E'">
                <view>
                  <view class="main_label" :class="{ data: form.timePeriod === 'zw' }">中午</view>
                  <view class="main_sjd">12：20-2：20</view>
                </view>
              </u-radio>
              <u-radio name="xw" style="margin-left: 50rpx;" :active-color="'#82007E'">
                <view>
                  <view class="main_label" :class="{ data: form.timePeriod === 'xw' }">下午</view>
                  <view class="main_sjd">5：00-6： 00</view>
                </view>
              </u-radio>
            </u-radio-group>
          </view>

          <u-checkbox-group v-model="form.isCyclic" @change="checkboxChange" style="margin-top: 20rpx;">
            <u-checkbox :customStyle="{marginBottom: '8px'}" shape="circle" :active-color="'#82007E'"
                        label="是否重复"></u-checkbox>
          </u-checkbox-group>

          <view v-if="form.isCyclic.length > 0" style="margin-top: 20rpx;">
            <view class="main_cfpl">重复频率：</view>
            <view style="height: 60rpx;display: flex;flex-direction: column;">
              <u-line color="#9E9E9E" />
              <u-radio-group v-model="form.cyclicMethod" style="display: flex;justify-content: space-around;">
                <u-radio name="mz" shape="square" :active-color="'#82007E'">
                  <view style="color: #7E7E7E;font-size: 28rpx;font-weight: bold;">每周</view>
                </u-radio>
                <u-radio name="my" shape="square" :active-color="'#82007E'">
                  <view style="color: #7E7E7E;font-size: 28rpx;font-weight: bold;">每月</view>
                </u-radio>
              </u-radio-group>
              <u-line color="#9E9E9E" />
            </view>
          </view>

          <view v-if="form.isCyclic.length > 0" style="margin-top: 20rpx;">
            <view class="main_qsrq">起始日期：</view>
            <view style="display: flex;justify-content: space-around;">
              <view>
                <u-line color="#9E9E9E" />
                <view class="main_qsrq_lable" style="color: #7E7E7E">
                  {{transitionData(form.singleStart)}}
                </view>
                <u-line color="#9E9E9E" />
              </view>
              <view style="font-size: 40rpx;">--</view>
              <view>
                <u-line color="#9E9E9E" />
                <view class="main_qsrq_lable">
                  <uni-datetime-picker ref="picker" v-model="form.singleEnd" type="date" :start="form.singleStart" :end="limitDate">
                    {{transitionData(form.singleEnd)}}
                  </uni-datetime-picker>
                </view>
                <u-line color="#9E9E9E" />
              </view>
            </view>
          </view>

        </view>
      </view>
    </view>
    <view class="footer">
      <image src="../../static/fh.svg" style="width: 50rpx;height: 50rpx;" @click="goBack" />
      <image src="../../static/ljyy.svg" style="width: 230rpx;height: 90rpx;" @click="openxq" />
    </view>
    <MyDialog v-if="showmark" @close='close'>
      <view style="margin-bottom: 40rpx;">
        <view style="font-size: 33rpx;font-weight: bold;margin: auto">{{ alteringClassroom.display }}</view>
        <view style="display: flex;margin-top: 10rpx;">
          <view class="nav">
            <view v-for="item,index in navList" :key="index">
              <view style="font-size: 22rpx; width: 90%" class="navItem" v-if="item !== null">{{item}}</view>
            </view>
          </view>
        </view>
      </view>
      <view class="mark_data">
        <view class="mark_data_title" style="">{{ transitionData(form.singleStart) }}</view>
        <view class="mark_data_title">{{ form.timePeriod === 'zw' ? "中午" : "下午" }}</view>
        <view class="mark_data_sj">{{ form.timePeriod === 'zw' ? "12：20-2：20" : "5：00-6：00" }}</view>
      </view>


      <view style="width: 160rpx; height: 40rpx; padding: 10rpx; background-color: #82007E; color: white; text-align: center; border-radius: 25rpx" @click="qd">修改预约</view>
    </MyDialog>
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
      showmark: false,
      tag_display: {},
      alteringClassroom: {},
      alteringRecord: {},
      alteringPlaceDisplay: "",
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
    }
  },
  onLoad() {
    this.limitDate.setDate(new Date().getDate() + 60);
    this.limitDate = this.buildDate(this.limitDate);
    this.tag_display = uni.getStorageSync('tag_display');
    this.alteringClassroom = uni.getStorageSync('alteringClassroom');
    this.alteringRecord = uni.getStorageSync("alteringRecord");
    uni.removeStorageSync("alteringClassroom");
    uni.removeStorageSync("alteringRecord");
    this.background = "background: url(https://nkapi.ememememem.space/img/" + this.alteringClassroom.pic_url + ") no-repeat";
    let buildDate = (d) =>
        `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
    this.form.singleStart = buildDate(new Date(this.alteringRecord.time_stamp * 1000));
    this.navList = this.alteringClassroom.func_tag.split(",");
    this.navList.pop();
    this.navList = this.navList.map(x => this.tag_display[x]);
    wx.request({
      url: "https://nkapi.ememememem.space/query/display",
      method: "POST",
      data: {
        cond: {"query": [[this.alteringClassroom.place, "place"]]}
      },
      success: (res) => {
        this.alteringPlaceDisplay = res.data[0]
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
    openxq() {
      if (this.form.isCyclic.length > 0) {
        if (this.form.timePeriod && this.form.cyclicMethod && this.form.singleStart && this.form.singleEnd) {
          this.showmark = true
        }
      } else {
        if (this.form.timePeriod && this.form.singleStart && this.form.singleEnd) {
          this.showmark = true
        }
      }


    },
    qd() {
      wx.showToast({
        title: "请求服务器...",
        icon: "loading",
        duration: 3000
      })
      wx.request({
        url: "https://nkapi.ememememem.space/alter/record",
        method: "POST",
        data: {
          "record_id": this.alteringRecord.id,
          "noon": (this.form.timePeriod === 'zw'),
          "time_stamp": new Date(this.form.singleStart).getTime() / 1000,
        },
        success: (res) => {
          let r = res.data;
          if (r.success) {
            uni.navigateBack({
              delta: 2
            });
            setTimeout(function () {
              wx.showToast({
                title: "修改成功！",
                icon: "success",
                duration: 3000
              })
            }, 1000);
          }
          else {
            if (r.err_code === 600) {
              wx.showToast({
                title: "无对应权限",
                icon: "error",
                duration: 3000
              })
            }
            else if (r.err_code === 601) {
              wx.showToast({
                title: "该时段已被预约",
                icon: "error",
                duration: 3000
              })
            }
            else if (r.err_code === 100) {
              wx.showToast({
                title: "服务器错误",
                icon: "error",
                duration: 3000
              })
            }
          }
          this.showmark = false;
        }
      })
    },
    close() {
      this.showmark = false
    },
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
}
</style>