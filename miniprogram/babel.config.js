module.exports = {
	presets: [[
		'@vue/cli-plugin-babel/preset',
		{
			// Usage-based core-js injection targets browsers; mini-program runtimes
			// provide their own platform APIs and may not define DOMException.
			useBuiltIns: process.env.UNI_PLATFORM === 'h5' ? 'usage' : 'entry'
		}
	]]
}
