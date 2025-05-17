import axios from "axios";
import { BaseURL } from "../setting.js";

// 创建axios实例
const instance = axios.create({
  baseURL: BaseURL,
  timeout: 10000,
});

// 添加请求拦截器
instance.interceptors.request.use(
  (config) => {
    // // 在发送请求之前做些什么
    // if (window.sessionStorage.getItem("TOKENSTR")) {
    //   config.headers["Authorization"] = window.sessionStorage.getItem("TOKENSTR");
    // }

    return config;
  },
  (error) => {
  }
);

// 添加响应拦截器
instance.interceptors.response.use(
  (response) => {
  },
  (error) => {
  }
);

export default instance;
