# WeChat mini-program builds

Build the Vue 2 uni-app WeChat mini-program from the repository checkout without HBuilderX:

```sh
cd miniprogram
npm ci
npm run build:mp-weixin:dev
npm run build:mp-weixin
```

The one-off development build writes to `miniprogram/dist/dev/mp-weixin`; the production
build writes to `miniprogram/dist/build/mp-weixin`. Import the corresponding directory
into WeChat DevTools. For an incremental development build, run `npm run dev:mp-weixin`
and leave it running while editing.

Set a real WeChat mini-program AppID in `manifest.json` before using WeChat login or
uploading. Production use also requires appropriate request/upload domains and a
configured backend; building does not contact the backend or validate credentials.
