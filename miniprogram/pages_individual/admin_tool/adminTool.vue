<template>
  <view class="indexPage" style="padding-top: 24rpx; padding-left: 5%; padding-right: 5%; height: fit-content">
    <view style="margin-bottom: 20%">
      <img src="../../static/fh.svg" style="width: 35rpx; height: 35rpx; margin-right: 5%;" @click="goBack" alt/> <text style="font-weight: bold; vertical-align: center;">管理员工具</text>
    </view>
    <view class="itemList">
      <view class="itembox" style="height: fit-content; background-color: #F0F0F0; padding: 2% 5%">
        <view style="font-weight: bold; display: flex; justify-content: space-between; padding: 3%" @click="expandClassrooms = !expandClassrooms">
          教室管理 <text>{{ expandClassrooms ? "−" : "+" }}</text>
        </view>
        <view v-if="expandClassrooms" class="room-panel">
          <u-search placeholder="搜索教室名称或编号" v-model="roomSearch" :clearabled="true" :show-action="false" />
          <view v-if="roomError" class="room-error">{{ roomError }} <text @click="loadClassrooms">重试</text></view>
          <view v-if="roomActionError" class="room-error">{{ roomActionError }}</view>
          <view v-if="!roomError && roomLoading" class="room-hint">正在加载教室…</view>
          <view v-if="!roomError && !roomLoading && !filteredClassrooms.length" class="room-hint">{{ classrooms.length ? "没有找到匹配的教室" : "暂无教室" }}</view>
          <view v-for="room in filteredClassrooms" :key="room.id" class="room-row">
            <view class="room-main"><text class="room-name">{{ room.display || "未命名教室" }}</text><text class="room-id">{{ room.id }} · {{ placeName(room.place) }}</text></view>
            <view class="room-actions"><text :class="room.available === false ? 'room-off' : 'room-on'">{{ room.available === false ? "已停用" : "可预约" }}</text><button class="room-button" @click="editRoom(room)">编辑</button><button class="room-button" @click="confirmRoomAvailability(room)">{{ room.available === false ? "重新开放" : "停用" }}</button></view>
          </view>
          <button class="room-add" @click="newRoom">＋ 新建教室</button>
          <view v-if="roomFormOpen" class="room-form">
            <view class="room-form-title">{{ roomEditing ? "编辑教室" : "新建教室" }}</view>
            <view class="room-field" v-if="!roomEditing"><text>教室编号</text><input v-model="roomForm.id" :disabled="roomSaving || roomImageBusy" placeholder="稳定且唯一的编号" /></view>
            <view class="room-field" v-else><text>教室编号</text><text class="room-id">{{ roomForm.id }}（不可修改）</text></view>
            <view class="room-field"><text>显示名称</text><input v-model="roomForm.display" :disabled="roomSaving || roomImageBusy" placeholder="例如：南楼 201" /></view>
            <view class="room-field"><text>所在地点</text><picker :disabled="roomSaving || roomImageBusy" :range="placeOptions" range-key="label" :value="placeIndex" @change="onPlaceChange"><view class="picker-value">{{ placeOptions[placeIndex].label }}　⌄</view></picker></view>
            <view class="room-image" v-if="roomImagePreview">
              <image class="room-image-preview" :src="roomImagePreview" mode="aspectFill" />
              <view class="room-image-controls"><button class="room-button" :disabled="roomSaving || roomImageBusy" @click="chooseRoomImage">更换照片</button><button class="room-button remove-image" :disabled="roomSaving || roomImageBusy" @click="removeRoomImage">移除</button></view>
            </view>
            <button v-else class="room-button image-picker" :disabled="roomSaving || roomImageBusy" @click="chooseRoomImage">{{ roomImageBusy ? "正在处理照片…" : "选择教室照片" }}</button>
            <view v-if="roomImageBusy" class="room-note image-status">{{ roomImageLocalPath || roomForm.pic_url ? "正在上传照片…" : "正在处理照片…" }}</view>
            <view class="room-note">可从相册选择或拍照，图片最大 5MB。照片只会在点击“保存”后关联到教室。</view>
            <view v-if="roomImageError" class="room-error">{{ roomImageError }} <text @click="chooseRoomImage">重试</text></view>
            <view class="room-field"><text>功能标签（选填）</text><input v-model="roomForm.func_tag" :disabled="roomSaving || roomImageBusy" placeholder="填写已有标签代码，逗号分隔" /></view>
            <view class="room-field"><text>允许预约</text><switch :disabled="roomSaving || roomImageBusy" :checked="roomForm.available" color="#82007e" @change="roomForm.available = $event.detail.value" /></view>
            <view class="room-note">标签代码须使用系统已有值。开放状态只控制教室是否可预约；用户仍须具备现有权限。新增教室不会自动授予预约权限。</view>
            <view v-if="roomFormError" class="room-error">{{ roomFormError }}</view>
            <view class="room-form-actions"><button class="room-button" :disabled="roomSaving || roomImageBusy" @click="closeRoomForm">取消</button><button class="room-button primary" :disabled="roomSaving || roomImageBusy" @click="saveRoom">{{ roomSaving ? "保存中…" : "保存" }}</button></view>
          </view>
        </view>
      </view>
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
              <text>教室</text><text style="color: grey">{{ classroomDisplay(item.classroom_id) }}</text>
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
      expandClassrooms: false,
      roomLoading: false,
      roomError: "",
      roomActionError: "",
      roomSearch: "",
      roomFormOpen: false,
       roomSaving: false,
       roomImageBusy: false,
       roomImageError: "",
       roomImageLocalPath: "",
       roomImageOperation: 0,
      roomFormError: "",
      roomEditing: false,
      roomForm: { id: "", display: "", place: "south", pic_url: "", func_tag: "", available: true },
      placeOptions: [{key:"south",label:"南楼"},{key:"office2",label:"第二办公楼"},{key:"north",label:"北楼"},{key:"book_bar",label:"书吧"},{key:"science",label:"科学馆"},{key:"exp",label:"实验楼"},{key:"art",label:"艺术馆"},{key:"outdoors",label:"室外"}],
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
  computed: {
    filteredClassrooms() {
      const q = (this.roomSearch || "").toLowerCase();
      return this.classrooms.filter(room => String(room.id || "").toLowerCase().includes(q) || String(room.display || "").toLowerCase().includes(q));
    },
     placeIndex() { const i = this.placeOptions.findIndex(x => x.key === this.roomForm.place); return i < 0 ? 0 : i; },
     roomImagePreview() { return this.roomImageLocalPath || this.roomImageUrl(this.roomForm.pic_url); }
  },
  onLoad() {
    this.loadClassrooms();
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
  onUnload() { this.resetRoomImageOperation(); },
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
    placeName(key) { const found = this.placeOptions.find(x => x.key === key); return found ? found.label : "未知地点"; },
    classroomDisplay(id) { const room = this.classrooms.find(x => x.id === id); return room ? room.display : "教室信息暂不可用（" + id + "）"; },
    onPlaceChange(event) { this.roomForm.place = this.placeOptions[Number(event.detail.value)].key; },
    loadClassrooms() {
      this.roomLoading = true; this.roomError = "";
      wx.request({ url: "https://nkapi.ememememem.space/query/classroom", method: "POST", data: {cond: {}}, success: res => {
        if (Array.isArray(res.data)) this.classrooms = res.data.map(x => Object.assign({available: true}, x));
        else this.roomError = "教室列表暂时无法读取，请稍后重试。";
      }, fail: () => { this.roomError = "网络连接失败，教室列表未能加载。"; }, complete: () => { this.roomLoading = false; } });
    },
    roomImageUrl(id) { return id ? "https://nkapi.ememememem.space/img/" + encodeURIComponent(id) : ""; },
    resetRoomImageOperation() { this.roomImageOperation += 1; this.roomImageBusy = false; this.roomImageError = ""; this.roomImageLocalPath = ""; },
    newRoom() { if (this.roomSaving || this.roomImageBusy) return; this.resetRoomImageOperation(); this.roomActionError = ""; this.roomEditing = false; this.roomFormError = ""; this.roomForm = {id:"", display:"", place:"south", pic_url:"", func_tag:"", available:true}; this.roomFormOpen = true; },
    editRoom(room) { if (this.roomSaving || this.roomImageBusy) return; this.resetRoomImageOperation(); this.roomActionError = ""; this.roomEditing = true; this.roomFormError = ""; this.roomForm = Object.assign({available:true, pic_url:"", func_tag:""}, room); if (!this.placeOptions.some(x => x.key === this.roomForm.place)) this.roomForm.place = "south"; this.roomFormOpen = true; },
    closeRoomForm() { if (this.roomSaving || this.roomImageBusy) return; this.resetRoomImageOperation(); this.roomFormOpen = false; },
    removeRoomImage() { if (this.roomSaving || this.roomImageBusy) return; this.roomImageOperation += 1; this.roomImageLocalPath = ""; this.roomImageError = ""; this.roomForm.pic_url = ""; },
    chooseRoomImage() {
      if (this.roomSaving || this.roomImageBusy || !this.roomFormOpen) return;
      this.roomImageBusy = true; this.roomImageError = "";
      const operation = ++this.roomImageOperation;
      const fail = message => { if (operation !== this.roomImageOperation) return; this.roomImageBusy = false; this.roomImageError = message; };
      wx.chooseImage({count:1, sizeType:["compressed"], sourceType:["album", "camera"],
        success: result => {
          if (operation !== this.roomImageOperation) return;
          const path = result && result.tempFilePaths && result.tempFilePaths[0];
          if (!path) { fail("未能读取所选照片，请重试。"); return; }
          wx.getFileSystemManager().readFile({filePath:path, success: file => {
            if (operation !== this.roomImageOperation) return;
            const bytes = file && file.data;
            if (!bytes || typeof bytes.byteLength !== "number") { fail("照片读取失败，请重新选择。"); return; }
            if (bytes.byteLength > 5 * 1024 * 1024) { fail("照片不能超过 5MB，请选择较小的图片。"); return; }
            wx.login({success: login => {
              if (operation !== this.roomImageOperation) return;
              if (!login || !login.code) { fail("无法取得登录凭证，请重新选择照片重试。"); return; }
              wx.request({url:"https://nkapi.ememememem.space/upload/classroom-image", method:"POST", data:bytes, header:{"X-Wechat-Code":login.code,"content-type":"application/octet-stream"},
                success: response => {
                  if (operation !== this.roomImageOperation) return;
                  const body = response && response.data;
                  if (body && body.success === true && typeof body.pic_url === "string" && body.pic_url) {
                    this.roomForm.pic_url = body.pic_url; this.roomImageLocalPath = path; this.roomImageBusy = false; this.roomImageError = "";
                  } else {
                    const messages = {unauthorized:"身份验证失败，请重新选择照片重试。", image_too_large:"照片不能超过 5MB，请选择较小的图片。", invalid_image:"图片格式无效，请选择 JPEG、PNG 或 WebP 图片。", image_storage_error:"照片暂时无法保存到服务器，请重试。"};
                    fail(messages[body && body.error] || "照片上传失败，请重试。");
                  }
                }, fail: () => fail("网络连接失败，照片尚未上传，请重试。")
              });
            }, fail: () => fail("无法取得登录凭证，请重新选择照片重试。")});
          }, fail: () => fail("照片读取失败，请重新选择后重试。")});
        }, fail: error => {
          if (operation !== this.roomImageOperation) return;
          if (error && (error.errMsg || "").indexOf("cancel") >= 0) { this.roomImageBusy = false; this.roomImageError = ""; }
          else fail("无法打开相册或相机，请重试。");
        }
      });
    },
    errorMessage(code) { const messages = {unauthorized:"管理员身份验证失败，请重新登录。", forbidden:"当前账号无权管理教室。", duplicate_id:"该教室编号已存在。", unknown_classroom:"教室不存在，列表可能已更新。", invalid_place:"请选择有效地点。", invalid_id:"教室编号格式无效。", invalid_display:"请填写有效的显示名称。", invalid_pic_url:"教室照片无效，请重新选择照片。", invalid_func_tag:"功能标签无效，请使用系统已有标签代码。", invalid_available:"开放状态无效，请重新选择。", database_error:"服务器暂时无法保存，请稍后重试。"}; return messages[code] || "保存失败，请检查填写内容后重试。"; },
    confirmRoomAvailability(room) {
      if (this.roomSaving || this.roomImageBusy) return;
      const enabling = room.available === false;
      uni.showModal({title: enabling ? "重新开放教室？" : "停用教室？", content: enabling ? "重新开放后，符合现有权限的用户可以预约。" : "停用后将不能新建预约；已有预约会保留，不会被删除。", success: res => { if (res.confirm) this.mutateRoom(room, enabling, true, false); }});
    },
    saveRoom() {
      if (this.roomSaving || this.roomImageBusy) return;
      if (!this.roomForm.id.trim() || !this.roomForm.display.trim()) { this.roomFormError = "请填写教室编号和显示名称。"; return; }
      if (!this.placeOptions.some(x => x.key === this.roomForm.place)) { this.roomFormError = "请选择有效地点。"; return; }
      this.mutateRoom(this.roomForm, this.roomForm.available, this.roomEditing, true);
    },
    mutateRoom(room, available, editing, fromForm) {
      if (this.roomSaving || this.roomImageBusy) return;
      this.roomSaving = true; this.roomFormError = ""; this.roomActionError = "";
      const setFailure = message => { if (fromForm && this.roomFormOpen) this.roomFormError = message; else this.roomActionError = message; };
      wx.login({ success: login => {
        if (!login.code) { this.roomSaving = false; setFailure("无法取得登录凭证，请重试。"); return; }
        const data = {code:login.code, id:String(room.id).trim(), display:String(room.display || "").trim(), place:room.place, pic_url:room.pic_url || "", func_tag:room.func_tag || "", available:Boolean(available)};
        wx.request({url:"https://nkapi.ememememem.space/" + (editing ? "alter/classroom" : "addition/classroom"), method:"POST", data, success: res => {
          if (res.data && res.data.success === true) { if (fromForm) this.roomFormOpen = false; this.loadClassrooms(); wx.showToast({title:"保存成功", icon:"success"}); }
          else setFailure(this.errorMessage(res.data && (res.data.error || (res.data.detail && res.data.detail[0] && res.data.detail[0].msg))));
        }, fail: () => { setFailure("网络连接失败，内容尚未保存，请重试。"); }, complete: () => { this.roomSaving = false; }});
      }, fail: () => { this.roomSaving = false; setFailure("无法取得登录凭证，请重试。"); }});
    },
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
            if (!res.data["success"]) {
              wx.showToast({
                title: "服务器错误",
                icon: "error",
                duration: 3000
              });
              return
            }
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
          if (!res.data["success"]) {
            wx.showToast({
              title: "服务器错误",
              icon: "error",
              duration: 3000
            });
            return
          }
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
  background: #f7f5f8;
  padding-top: calc(var(--status-bar-height, 0px) + env(safe-area-inset-top) + 24rpx) !important;
  overflow-y: auto;

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
  .itembox { border-radius: 12rpx; box-shadow: 0 2rpx 8rpx rgba(87, 27, 72, .08); }
  .itemList .itembox { background: #fff !important; color: #29232c !important; border: 1px solid #eee8f0; max-width: 100%; box-sizing: border-box; }
  input { min-width: 0; height: 76rpx; line-height: 44rpx; border: 1px solid #e7e1e9; border-radius: 10rpx; padding: 14rpx 16rpx !important; box-sizing: border-box; }
  button { background: #82007e; color: #fff; border: 0; border-radius: 12rpx; min-height: 64rpx; white-space: normal; }
  .room-panel { padding: 0 3% 3%; }
  .room-row { display: flex; align-items: center; justify-content: space-between; gap: 12rpx; padding: 20rpx 8rpx; border-bottom: 1px solid #eee8f0; }
  .room-main { display: flex; flex-direction: column; min-width: 0; }
  .room-name { font-weight: bold; overflow-wrap: anywhere; }
  .room-id, .room-hint { color: #827b85; font-size: 24rpx; }
  .room-actions { display: flex; align-items: center; flex-wrap: wrap; justify-content: flex-end; gap: 8rpx; }
  .room-on { color: #327b4f; font-size: 23rpx; }
  .room-off, .room-error { color: #b04444; font-size: 24rpx; }
  .room-error text { margin-left: 12rpx; color: #82007e; }
  .room-button { width: auto; min-height: 54rpx; line-height: 54rpx; padding: 0 18rpx; font-size: 23rpx; margin: 0; }
  .room-add { margin-top: 18rpx; width: 100%; }
  .room-form { margin-top: 20rpx; padding: 22rpx; background: #f8f5f9; border-radius: 12rpx; }
  .room-image { display: flex; align-items: center; gap: 18rpx; margin: 14rpx 0; }
  .room-image-preview { width: 190rpx; height: 140rpx; border-radius: 10rpx; background: #eee8f0; }
  .room-image-controls { display: flex; gap: 12rpx; flex-wrap: wrap; }
  .room-button.remove-image { background: #fff; color: #82007e; border: 1px solid #d8c6d8; }
  .image-picker { width: 100%; margin: 10rpx 0; }
  .room-form-title { font-weight: bold; margin-bottom: 14rpx; }
  .room-field { display: flex; align-items: center; justify-content: space-between; gap: 16rpx; padding: 10rpx 0; }
  .room-field > text:first-child { flex-shrink: 0; font-size: 25rpx; }
  .room-field input, .room-field picker { width: 62%; }
  .picker-value { text-align: right; padding: 18rpx; background: white; border-radius: 10rpx; }
  .room-note { color: #827b85; font-size: 23rpx; line-height: 1.5; margin: 12rpx 0; }
  .room-form-actions { display: flex; justify-content: flex-end; gap: 14rpx; margin-top: 14rpx; }
  .room-form-actions button { margin: 0; }
  .room-form-actions .primary { background: #82007e; }
  @media screen and (max-width: 380px) { .room-row { align-items: flex-start; flex-direction: column; } .room-actions { justify-content: flex-start; } }
}
</style>
