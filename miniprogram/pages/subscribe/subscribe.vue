<template>
	<view class="indexPage">
		<view class="content">
			<view class="nav">
				<view v-for="item,index in navList" :key="index">
					<view class="navItem" :class="{ active: navMode === item }" @click="setNavMode(item)">{{item}}
						<span class="line"></span>
					</view>
				</view>
			</view>
			<view class="main">
				<view style="box-sizing: border-box;padding-left: 30rpx;">
					<u-search placeholder="地点" v-model="search" :clearabled="true" :show-action="false"></u-search>
				</view>
				<view class="Choose">
					<view class="flex-container">
						<view class="items-wrapper" :class="{ 'show-all': isOpen }">
							<view v-for="(item,index) in ChooseItem" :key="index" class="item">
								<view class="ChooseItem" :class="{ active: ChooseMode === item }" @click="setChooseMode(item)">{{item}}
								</view>
							</view>
						</view>
						<view v-if="canShowMore">
							<u-icon name="arrow-down" color="#9E9E9E" size="20" :class="{ 'rotate': isOpen }" class="icon"
								@click="toggleDropdown"></u-icon>
							<view class="dropdown-content" :style="{ display: isOpen ? 'block' : 'none' }">
								<view class="items-wrappers">
									<view v-for="(item,index) in newChooseItem" :key="index" class="item">
										<view class="ChooseItem" :class="{ active: ChooseMode === item }" @click="setChooseMode(item)">
											{{item}}
										</view>
									</view>
								</view>
							</view>
						</view>
					</view>
				</view>
				<view class="w_list">
					<view :class="{ 'mark': isOpen }"></view>
					<view class="navTitle">{{navMode}}</view>
					<view class="list">
						<view v-for="item,index in southItem" :key="index" v-if="navMode === '南楼'">
							<view class="listItem" v-if="item.display.includes(search)">
								<view style="width: 170rpx;height: 100%;background-color: #F5F5F5;border-radius: 12rpx;">
                  <image :src="'https://nkapi.ememememem.space/img/' + item.pic_url" style="width: inherit; height: inherit"/>
                </view>
								<view style="margin-left: 10rpx;width: calc(100% - 170rpx);">
									<view style="font-weight: bold;height: 50rpx;">{{item.display}}</view>
									<view style="display: flex;height: 38rpx;">
										<view v-for="(i,indexs) in (item.func_tag != null ? item.func_tag.split(',') : [])" :key="indexs">
                      <!-- It would somehow only work this way... -->
											<view
												style="font-size: 27rpx;margin-right: 10rpx;background-color: #F5F5F5;color: #9E9E9E;padding: 0rpx 20rpx;box-sizing: border-box;" v-if="i !== ''">
												{{tag_display[i]}}
											</view>
										</view>
									</view>
									<view
										style="display: flex;justify-content: space-between;height: calc(100% - 88rpx);align-items: center;">
										<view style="font-size: 30rpx;color: #9E9E9E;margin-top: 20rpx;">{{item.num}}</view>
										<view style="width: 50rpx;height: 50rpx;">
											<image src="../../static/yy_qw.svg" style="width: 100%;height: 100%;" @click="toyy" />
										</view>
									</view>
								</view>
							</view>
						</view>
						<view v-for="item,index in northItem" :key="index" v-if="navMode === '北楼'">
              <view class="listItem" v-if="item.display.includes(search)">
								<view style="width: 170rpx;height: 100%;background-color: #F5F5F5;border-radius: 12rpx;">
                  <image :src="'https://nkapi.ememememem.space/img/' + item.pic_url" style="width: inherit; height: inherit"/>
                </view>
								<view style="margin-left: 10rpx;width: calc(100% - 170rpx);">
									<view style="font-weight: bold;height: 50rpx;">{{item.display}}</view>
									<view style="display: flex;height: 38rpx;">
                    <view v-for="(i,indexs) in (item.func_tag != null ? item.func_tag.split(',') : [])" :key="indexs">
                      <view
                          style="font-size: 27rpx;margin-right: 10rpx;background-color: #F5F5F5;color: #9E9E9E;padding: 0rpx 20rpx;box-sizing: border-box;" v-if="i !== ''">
                        {{tag_display[i]}}
                      </view>
                    </view>
									</view>
									<view
										style="display: flex;justify-content: space-between;height: calc(100% - 88rpx);align-items: center;">
										<view style="font-size: 30rpx;color: #9E9E9E;margin-top: 20rpx;">{{item.num}}</view>
										<view style="width: 50rpx;height: 50rpx;">
											<image src="../../static/yy_qw.svg" style="width: 100%;height: 100%;" @click="toyy" />
										</view>
									</view>
								</view>
							</view>
						</view>
						<view v-for="item,index in office2Item" :key="index" v-if="navMode === '第二办公楼'">
              <view class="listItem" v-if="item.display.includes(search)">
								<view style="width: 170rpx;height: 100%;background-color: #F5F5F5;border-radius: 12rpx;">
                  <image :src="'https://nkapi.ememememem.space/img/' + item.pic_url" style="width: inherit; height: inherit"/>
                </view>
								<view style="margin-left: 10rpx;width: calc(100% - 170rpx);">
									<view style="font-weight: bold;height: 50rpx;">{{item.display}}</view>
									<view style="display: flex;height: 38rpx;">
                    <view v-for="(i,indexs) in (item.func_tag != null ? item.func_tag.split(',') : [])" :key="indexs">
                      <view
                          style="font-size: 27rpx;margin-right: 10rpx;background-color: #F5F5F5;color: #9E9E9E;padding: 0rpx 20rpx;box-sizing: border-box;" v-if="i !== ''">
                        {{tag_display[i]}}
                      </view>
                    </view>
									</view>
									<view
										style="display: flex;justify-content: space-between;height: calc(100% - 88rpx);align-items: center;">
										<view style="font-size: 30rpx;color: #9E9E9E;margin-top: 20rpx;">{{item.num}}</view>
										<view style="width: 50rpx;height: 50rpx;">
											<image src="../../static/yy_qw.svg" style="width: 100%;height: 100%;" @click="toyy" />
										</view>
									</view>
								</view>
							</view>
						</view>
            <view v-for="item,index in scienceItem" :key="index" v-if="navMode === '科学馆'">
              <view class="listItem" v-if="item.display.includes(search)">
                <view style="width: 170rpx;height: 100%;background-color: #F5F5F5;border-radius: 12rpx;">
                  <image :src="'https://nkapi.ememememem.space/img/' + item.pic_url" style="width: inherit; height: inherit"/>
                </view>
                <view style="margin-left: 10rpx;width: calc(100% - 170rpx);">
                  <view style="font-weight: bold;height: 50rpx;">{{item.display}}</view>
                  <view style="display: flex;height: 38rpx;">
                    <view v-for="(i,indexs) in (item.func_tag != null ? item.func_tag.split(',') : [])" :key="indexs">
                      <view
                          style="font-size: 27rpx;margin-right: 10rpx;background-color: #F5F5F5;color: #9E9E9E;padding: 0rpx 20rpx;box-sizing: border-box;" v-if="i !== ''">
                        {{tag_display[i]}}
                      </view>
                    </view>
                  </view>
                  <view
                      style="display: flex;justify-content: space-between;height: calc(100% - 88rpx);align-items: center;">
                    <view style="font-size: 30rpx;color: #9E9E9E;margin-top: 20rpx;">{{item.num}}</view>
                    <view style="width: 50rpx;height: 50rpx;">
                      <image src="../../static/yy_qw.svg" style="width: 100%;height: 100%;" @click="toyy" />
                    </view>
                  </view>
                </view>
              </view>
            </view>
            <view v-for="item,index in bookBarItem" :key="index" v-if="navMode === '书吧'">
              <view class="listItem" v-if="item.display.includes(search)">
                <view style="width: 170rpx;height: 100%;background-color: #F5F5F5;border-radius: 12rpx;">
                  <image :src="'https://nkapi.ememememem.space/img/' + item.pic_url" style="width: inherit; height: inherit"/>
                </view>
                <view style="margin-left: 10rpx;width: calc(100% - 170rpx);">
                  <view style="font-weight: bold;height: 50rpx;">{{item.display}}</view>
                  <view style="display: flex;height: 38rpx;">
                    <view v-for="(i,indexs) in (item.func_tag != null ? item.func_tag.split(',') : [])" :key="indexs">
                      <view
                          style="font-size: 27rpx;margin-right: 10rpx;background-color: #F5F5F5;color: #9E9E9E;padding: 0rpx 20rpx;box-sizing: border-box;" v-if="i !== ''">
                        {{tag_display[i]}}
                      </view>
                    </view>
                  </view>
                  <view
                      style="display: flex;justify-content: space-between;height: calc(100% - 88rpx);align-items: center;">
                    <view style="font-size: 30rpx;color: #9E9E9E;margin-top: 20rpx;">{{item.num}}</view>
                    <view style="width: 50rpx;height: 50rpx;">
                      <image src="../../static/yy_qw.svg" style="width: 100%;height: 100%;" @click="toyy" />
                    </view>
                  </view>
                </view>
              </view>
            </view>
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
				isOpen: false,
				canShowMore: false,
				wk: null,
				nk: null,
				navList: ['南楼', '第二办公楼', '北楼', '书吧', '科学馆'],
				navMode: '南楼',
				search: "",
				ChooseItem: ['舞蹈', '功能1', '功能2', '功能3', '功能4', '功能5', '功能6'],
				newChooseItem: [],
				ChooseMode: '舞蹈',
				ChooseNum: 0,
        southItem: [],
        office2Item: [],
        northItem: [],
        bookBarItem: [],
        scienceItem: [],
        tag_display: {},
				listItem1: [{
					name: "AAA舞蹈教室",
					nav: ['舞蹈', '标签1'],
					num: "204",
				}, {
					name: "NGA舞蹈教室",
					nav: ['舞蹈', '标签1'],
					num: "205",
				}],
				listItem2: [{
					name: "AAA舞蹈教室",
					nav: ['舞蹈', '标签1'],
					num: "204",
				}, {
					name: "ANB舞蹈教室",
					nav: ['舞蹈', '标签1'],
					num: "206",
				}, ],
				listItem: [{
						name: "AAA舞蹈教室",
						nav: ['舞蹈', '标签1'],
						num: "204",
					},
					{
						name: "NGA舞蹈教室",
						nav: ['舞蹈', '标签1'],
						num: "205",
					},
					{
						name: "ANB舞蹈教室",
						nav: ['舞蹈', '标签1'],
						num: "206",
					},
					{
						name: "AAA舞蹈教室",
						nav: ['舞蹈', '标签1'],
						num: "207",
					},
					{
						name: "AAA舞蹈教室",
						nav: ['舞蹈', '标签1'],
						num: "208",
					},
					{
						name: "AAA舞蹈教室",
						nav: ['舞蹈', '标签1'],
						num: "209",
					},
				],
			}
		},
    onLoad() {
      wx.request({
        url: "https://nkapi.ememememem.space/query/func_tags",
        method: "GET",
        success: (res) => {
          this.tag_display = res.data;
        }
      })

      wx.request({
        url: "https://nkapi.ememememem.space/query/classroom",
        method: "POST",
        data: {
          cond: {}
        },
        success: (res) => {
          let cls = res.data;
          let classroomItems = {"south": [], "office2": [], "north": [], "book_bar": [], "science": []}
          let i;
          for (i = 0; i < cls.length; i++) classroomItems[cls[i]["place"]].push(cls[i]);
          this.southItem = classroomItems.south;
          this.office2Item = classroomItems.office2;
          this.bookBarItem = classroomItems.book_bar;
          this.scienceItem = classroomItems.science;
          this.northItem = classroomItems.north;
        }
      })
    },
		mounted() {
			this.$nextTick(() => {
				this.checkOverflow();
			});
		},
		created() {},
		methods: {
			toggleDropdown() {
				this.isOpen = !this.isOpen;
			},
			//菜单
			setNavMode(mode) {
				this.navMode = mode
			},
			//tabs
			setChooseMode(mode) {
				this.ChooseMode = mode
				this.isOpen = false
			},
			toyy() {
				uni.navigateTo({
					url: `/pages/Individual/ReservationDetails`,
				})
			},
			checkOverflow() {
				const query = uni.createSelectorQuery().in(this);
				query.select('.Choose').boundingClientRect(containerData => {
					this.wk = containerData.width
				}).exec();
				query.select('.ChooseItem').boundingClientRect(containerData => {
					this.nk = containerData.width + 10
				}).exec();

				let num = this.wk / this.nk
				this.ChooseNum = parseInt(num);

				let ChooseItemArray = this.ChooseItem.slice(0, this.ChooseNum);
				this.newChooseItem = this.ChooseItem.slice(this.ChooseNum);

				if (this.ChooseItem.length >= this.ChooseNum) {
					this.canShowMore = true;
				} else {
					this.canShowMore = false;
				}
			},
		}
	}
</script>

<style lang="scss" scoped>
	// .dropdown {
	// 	position: relative;
	// 	display: inline-block;
	// }
	.dropdown-content {
		display: none;
		position: absolute;
		background-color: #f9f9f9;
		min-width: 100%;
		box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
		padding: 12px 16px;
	}

	.indexPage {
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
		background: url('../../static/title.svg') no-repeat;
		background-size: 100%;

		.content {
			display: flex;
			width: 100%;
			height: calc(100% - 200rpx);
			margin-top: 200rpx;
			overflow: auto;

			.nav {
				width: 20%;
				height: 100%;
				background-color: #efebf4;
				border-top-right-radius: 12rpx;
				padding-top: 75rpx;
				box-sizing: border-box;

				.navItem {
					width: 100%;
					height: 80rpx;
					line-height: 80rpx;
					text-align: center;
					font-size: 30rpx;
					font-weight: bold;
					color: #9D979D;
					margin-bottom: 20rpx;
					position: relative;

					.line {
						position: absolute;
						left: 5rpx;
						width: 4rpx;
						height: 80%;
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
					background: #fff;
					color: #82007E;
					font-weight: bold;
				}
			}

			.main {
				width: 80%;
				height: 100%;
				background-color: #ffffff;
				box-sizing: border-box;
				// padding-right: 30rpx;

				.Choose {
					width: 100%;
					margin-top: 10rpx;
					position: relative;
					z-index: 1000;

					.flex-container {
						.item {
							.ChooseItem {
								padding: 5rpx 20rpx;
								box-sizing: content-box;
								color: #9E9E9E;
								background-color: #F5F5F5;
								border-radius: 30rpx;
								font-size: 30rpx;
								margin-left: 10rpx;
								margin-bottom: 10rpx;
							}

							.ChooseItem.active {
								background: #FAE4FF;
								color: #830080;
								font-weight: bold;
							}
						}

						.items-wrapper {
							display: flex;
							flex-wrap: wrap;
							overflow: hidden;
							max-height: 50rpx;
							transition: max-height 0.3s ease;
							margin-left: 30rpx;
						}

						.items-wrappers {
							display: flex;
							flex-wrap: wrap;
							overflow: hidden;
							transition: max-height 0.3s ease;
						}
					}

					.icon {
						position: absolute;
						top: 8rpx;
						right: 0;
						flex-shrink: 0;
						margin-left: 10px;
						transition: transform 0.3s ease;
						transform-origin: center center;
						margin-right: 20rpx;
					}

					.icon.rotate {
						transform: rotate(180deg);
					}
				}

				.navTitle {
					margin-top: 10rpx;
					font-size: 36rpx;
					font-weight: bold;
					margin-left: 30rpx;
				}

				.w_list {
					position: relative;
					width: 100%;
					height: calc(100% - 150rpx);
					margin-top: 20rpx;

					.mark {
						z-index: 500;
						position: absolute;
						top: 0;
						bottom: 0;
						left: 0;
						right: 0;
						background: rgba(0, 0, 0, 0.25);
					}

					.list {
						width: 100%;
						height: calc(100% - 60rpx);
						padding: 0 30rpx;
						box-sizing: border-box;
						overflow: auto;

						.listItem {
							width: 98%;
							height: 200rpx;
							background: #FFFFFF;
							box-shadow: 0px 1px 2px 0px rgba(87, 27, 72, 0.15);
							border-radius: 12rpx;
							border: 1px solid #f2f2f2;
							margin-bottom: 30rpx;
							padding: 20rpx;
							box-sizing: border-box;
							display: flex;
							align-items: center;
						}
					}
				}
			}
		}
	}
</style>