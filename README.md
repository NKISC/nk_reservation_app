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

## Classroom management

Open **管理员工具 → 教室管理** to create or edit classrooms and stop or reopen
bookings. Classroom IDs remain fixed after creation. Disabling a classroom hides
it from the booking list and rejects new single and recurring bookings without
deleting existing reservations. Existing booking permissions still apply; creating
a classroom does not grant users access to it.

In the classroom editor, choose a photo from the album or camera instead of
entering an image ID. Images can be previewed, replaced, or removed. Uploads accept
JPEG, PNG, and WebP up to 5 MiB and 20 million pixels, and are converted to JPEG.
Click **保存** after uploading or removing a photo to save the classroom change.
Removing or replacing a photo does not delete existing image files.

The new `/addition/classroom` and `/alter/classroom` endpoints require a fresh
WeChat login code and check the corresponding user's `admin` permission on the
server. Configure the backend's `appid` and `appSecret` files for this to work.
This check is specific to the new endpoints, not an authorization overhaul of the
older admin APIs. The old `/delete/classroom/` endpoint now returns HTTP 410;
disable classrooms instead of deleting them.

Image uploads also require a fresh admin login code. The
`/upload/classroom-image` endpoint accepts raw image bytes with an
`X-Wechat-Code` header and returns the internal `pic_url` used by classroom saves.
It requires Pillow (`python -m pip install Pillow`) and write access to the
working directory's `img/` folder. Keep that folder in persistent storage/backups;
generated uploads are ignored by Git.

Availability uses a separate, automatically created SQLite table; existing rooms
default to available. `/query/classroom` includes disabled rooms for reservation
display; pass `available_only: true` alongside `cond` for the booking list.

With backend dependencies and `httpx` installed, run the isolated regression tests from the
repository root (no live database or WeChat access required):

```sh
python -m unittest discover -s test -p 'test_classroom*.py' -v
node test/test_classroom_image_ui.cjs
```
