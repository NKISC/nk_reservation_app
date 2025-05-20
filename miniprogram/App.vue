<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
      wx.login({
        success(code_res) {
          wx.request({
            url: "https://nkapi.ememememem.space/login",
            method: "POST",
            data: {
              "code": code_res.code,
            },
            success(res) {
              uni.setStorageSync("openid", res.data.openid);
            }
          })
        }
      })
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style lang="scss">
	/* 注意要写在第一行，同时给style标签加入lang="scss"属性 */
	@import "@/uni_modules/uview-ui/index.scss";
	uni-app {
		font-family: Alimama FangYuanTi VF-SemiBold;
	}
</style>
