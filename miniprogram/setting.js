module.exports = {
  Title: '重庆南开中学',
  icon: "",
  // 代理地址
  BaseURL: process.env.NODE_ENV === 'production' ? '/Api' : '',
  isOutTime: process.env.NODE_ENV === "production" ? true : false,
  // 配置webSocket地址
  WebSocketURL:
    process.env.NODE_ENV === "production"
      ? ""
      : "",
  /**
   * 单用户登录和多用户登录
   * 单用户登录：1
   * 多用户登录：2
   */
  loginUserType: 1,
  /**
   * @type {boolean} true | false	
   * @description 是否在侧边栏中显示徽标
   */
  sidebarLogo: false,
  /**
   * UI界面大小:small / medium / large / ' '
   */
  uiSize: "small",
  /**
   * 表格大小：medium / small / mini/ ' '
   */
  tablesize: "small",

  /**
   * 表格高度
   */
  tableHeight: "calc(100vh - 330px)",

  /**
   * 按钮大小:medium / small / mini/ ' '
   */
  buttonsize: "small",
};
