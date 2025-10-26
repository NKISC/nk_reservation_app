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
							label="周期预约"></u-checkbox>
					</u-checkbox-group>

					<view v-if="form.isCyclic.length > 0" style="margin-top: 20rpx; width: 100%">
						<view class="main_cfpl">重复频率：</view>
						<view style="height: 60rpx;display: flex;flex-direction: column;">
							<u-line color="#9E9E9E"/>
              <u-checkbox-group v-model="form.cycForm">
                <div style="display: flex; justify-content: space-between; flex-wrap: wrap; width: 100%">
                  <span v-for="(item, index) in form.cycDay" v-if="index !== 0" :key="index" style="display: flex; align-items: center">
                    <u-checkbox :name="index" /> <br/>{{ dayRefs[index - 1] }}
                  </span>
                </div>
              </u-checkbox-group>


              <u-line color="#9E9E9E"/>
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
						</view>
            <!--Works for now-->
            <view class="main_qsrq">终止日期：</view>
            <view style="display: flex;justify-content: space-around;">
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
        <view style="margin-top: 5%; font-weight: bold; font-size: 120%; height: fit-content">
          近期活动：
          <view v-for="(item,index) in recentReservations" :key="index">
            <view class="listItem">
              <view style="width: 170rpx;height: 100%;background-color: #F5F5F5;border-radius: 12rpx; float: left">
                <image :src="'https://nkapi.ememememem.space/img/' + reservingClassroom.pic_url" style="width: inherit; height: inherit"/>
              </view>
              <view style="margin-left: 10rpx;width: calc(100% - 170rpx)">
                <view style="font-weight: bold;height: 50rpx;">{{ reservingClassroom.display }}</view>
                <view style="font-weight: normal; font-size: 20rpx; color: grey">{{ buildDate(new Date(item.time_stamp * 1000))}} {{ item.noon ? "中午" : "下午" }}</view>
                <view style="font-weight: normal; font-size: 20rpx; color: black; display: flex; align-items: center; margin-top: 10rpx">
                  <img src="../../static/gr_active.jpeg" style="height: 30rpx; width: 30rpx; margin-right: 15rpx" alt />
                  <text>{{ userList.find(user => user.id === item.applicant_id).display }}</text>
                </view>
                <view style="font-weight: normal; font-size: 20rpx;
                color: white; background-color: orange; border-radius: 20rpx; width: fit-content; padding: 0.5% 2%; margin-top: 3%"
                v-if="cycRecordIds.find(group => group['record_id'].includes(item.id.toString() + ','))">
                  周期
                </view>
              </view>
            </view>
          </view>
          <view v-if="recentReservations.length === 0" style="font-size: 30rpx; display: flex; justify-content: center; color: grey; margin-top: 30%">
            该教室最近无活动
          </view>
        </view>
			</view>
		</view>
    <view :style="bottomMarginStyle">
      <u-line />
    </view>
		<view class="footer">
			<image src="../../static/fh.svg" style="width: 50rpx;height: 50rpx;" @click="goBack" />
			<image src="../../static/ljyy.svg" style="width: 230rpx;height: 90rpx;" @click="openxq" />
		</view>
		<MyDialog v-if="showmark" @close='close'>
			<view style="margin-bottom: 40rpx;">
				<view style="font-size: 33rpx;font-weight: bold;margin: auto">{{ reservingClassroom.display }}</view>
			</view>
			<view class="mark_data">
				<view class="mark_data_title" style="">{{ transitionData(form.singleStart) }}</view>
				<view class="mark_data_title">{{ form.timePeriod === 'zw' ? "中午" : "下午" }}</view>
				<view class="mark_data_sj">{{ form.timePeriod === 'zw' ? "12：20-2：20" : "5：00-6：00" }}</view>
			</view>

			<view class="mark_data">
        <view class="mark_data_title" style="margin-bottom: 10rpx;">每周{{ constructCyclicalDayString() }}重复</view>
				<view class="mark_data_sj" style="font-weight: bold;" v-if="form.isCyclic.length > 0">{{ form.singleStart }}</view>
				<view class="mark_data_title" v-if="form.isCyclic.length > 0">--</view>
				<view class="mark_data_sj" style="font-weight: bold;" v-if="form.isCyclic.length > 0">{{ form.singleEnd }}</view>
        <view class="mark_data_title" style="font-size: 24rpx" v-else>不重复</view>
			</view>

			<image src="../../static/queding.svg" style="width: 300rpx;height: 100rpx;" @click='qd' />
		</MyDialog>
	</view>
</template>

<script>
	import MyDialog from '@/components/MyDialog.vue';
	import uniDatetimePicker from '@/uni_modules/uni-datetime-picker/components/uni-datetime-picker/uni-datetime-picker';
	import {
		formatDate
	} from '../../pages/Individual/Individual.js'
  import ULine from "../../uni_modules/uview-ui/components/u-line/u-line.vue";
	export default {
		components: {
      ULine,
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
        reservingClassroom: {},
        reservingPlaceDisplay: "",
        recentReservations: [],
        cycRecordIds: [],
				navList: [],
				navMode: '',
        bottomMarginStyle: "",
        dayRefs: {0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '日'},
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
          cycDay: [false, false, false, false, false, false, false, false],
          cycForm: [],
					singleStart: (() => new Date(Date.now() + (((8 - new Date().getDay()) % 7 || 7) * 86400000)))(),
					singleEnd: (() => new Date(Date.now() + (((8 - new Date().getDay()) % 7 || 7) * 86400000)))(),
				},
				datetimeStart: (() => new Date(Date.now() + (((8 - new Date().getDay()) % 7 || 7) * 86400000)))(),
        limitDate: new Date(),
        background: "",
        userList: [],
			}
		},
    onLoad() {
      this.limitDate.setDate(new Date().getDate() + 21);
      this.limitDate = this.buildDate(this.limitDate);
      this.form.singleStart = this.buildDate(this.form.singleStart);
      this.form.singleEnd = this.buildDate(this.form.singleEnd);
      this.datetimeStart = this.buildDate(this.datetimeStart);
      this.tag_display = uni.getStorageSync('tag_display');
      this.reservingClassroom = uni.getStorageSync('reservingClassroom');
      uni.removeStorageSync("reservingClassroom");
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
      });
      wx.request({
        url: "https://nkapi.ememememem.space/query/record",
        method: "POST",
        data: {
          cond: {"classroom_id": this.reservingClassroom.id}
        },
        success: (res) => {
          this.recentReservations = res.data
          this.bottomMarginStyle = "margin-top: " + (Math.max(0, (this.recentReservations.length - 1) * 250)) + "rpx"
        }
      });
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
        url: "https://nkapi.ememememem.space/query/user",
        method: "POST",
        data: {
          cond: {},
        },
        success: (res) => {
          this.userList = res.data
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
        this.cyclicalCheckboxChange();
				if (this.form.isCyclic.length > 0) {
					if (this.form.timePeriod && this.form.singleStart && this.form.singleEnd && this.form.cycDay.find(x => x)) {
						this.showmark = true
					}
				} else {
					if (this.form.timePeriod && this.form.singleStart) {
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
        if (this.form.isCyclic.length > 0) {
          wx.request({
            url: "https://nkapi.ememememem.space/addition/add_cyclical_record",
            method: "POST",
            data: {
              "classroom": this.reservingClassroom.id,
              "noon": (this.form.timePeriod === 'zw'),
              "applicant_id": uni.getStorageSync("openid"),
              "beginning_time_stamp": new Date(this.form.singleStart).getTime() / 1000,
              "ending_time_stamp": new Date(this.form.singleEnd).getTime() / 1000,
              "days": this.form.cycDay
            },
            success: (res) => {
              let r = res.data;
              if (r.success) {
                uni.navigateBack({
                  delta: 1
                });
                setTimeout(function () {
                  wx.showToast({
                    title: "预约成功！",
                    icon: "success",
                    duration: 3000
                  })
                }, 1000);
              } else {
                if (r.err_code === 600) {
                  wx.showToast({
                    title: "无对应权限",
                    icon: "error",
                    duration: 3000
                  })
                } else if (r.err_code === 601) {
                  wx.showToast({
                    title: "该时段已被预约",
                    icon: "error",
                    duration: 3000
                  })
                } else if (r.err_code === 100) {
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
        }
        else {
          wx.request({
            url: "https://nkapi.ememememem.space/addition/add_record",
            method: "POST",
            data: {
              "classroom": this.reservingClassroom.id,
              "noon": (this.form.timePeriod === 'zw'),
              "applicant_id": uni.getStorageSync("openid"),
              "time_stamp": new Date(this.form.singleStart).getTime() / 1000,
            },
            success: (res) => {
              let r = res.data;
              if (r.success) {
                uni.navigateBack({
                  delta: 1
                });
                setTimeout(function () {
                  wx.showToast({
                    title: "预约成功！",
                    icon: "success",
                    duration: 3000
                  })
                }, 1000);
              } else {
                if (r.err_code === 600) {
                  wx.showToast({
                    title: "无对应权限",
                    icon: "error",
                    duration: 3000
                  })
                } else if (r.err_code === 601) {
                  wx.showToast({
                    title: "该时段已被预约",
                    icon: "error",
                    duration: 3000
                  })
                } else if (r.err_code === 100) {
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
        }
			},
			close() {
				this.showmark = false
			},
      cyclicalCheckboxChange() {
        for (let i = 1; i < 8; i++) {
          this.form.cycDay[i] = this.form.cycForm.includes(i);
        }
      },
      constructCyclicalDayString() {
        let ret = [];
        for (let i = 1; i < 8; i++) if (this.form.cycDay[i]) ret.push(this.dayRefs[i - 1]);
        return ret.join("、");
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

    .listItem {
      width: 98%;
      height: 200rpx;
      background: #FFFFFF;
      box-shadow: 0px 1px 2px 0px rgba(87, 27, 72, 0.15);
      border-radius: 12rpx;
      border: 1px solid #f2f2f2;
      padding: 20rpx;
      box-sizing: border-box;
      display: flex;
      margin: 5% 0;
      font-size: 28rpx;
    }

		.footer {
			margin-top: 90rpx;
			width: 100%;
			height: 10%;
			border-top: 3px solid #eaeaea;
			display: flex;
      position: fixed;
      bottom: 0;
      background-color: white;
			justify-content: space-between;
			align-items: center;
			padding: 0 50rpx;
			box-sizing: border-box;
		}
	}
</style>