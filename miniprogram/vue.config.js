module.exports = {
	// transpileDependencies: true,
	lintOnSave: false,
	productionSourceMap: false,
	devServer: {
		port: 8081,
		proxy: {
			'/': {
				ws: true,
				//目标地址
				target: 'http://192.168.0.100:8010',
				//发送请求host会被设置target
				changeOrigin: true,
				// 不重写请求地址
				pathReWrite: {
					"^/": "/",
				},
			},
		},

	},
}