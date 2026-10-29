const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
const source = fs.readFileSync('miniprogram/pages_individual/admin_tool/adminTool.vue', 'utf8');
const script = source.match(/<script>([\s\S]*?)<\/script>/)[1].replace(/^import .*;\n/gm, '');
const sandbox = {module: {exports: {}}, wx: {}, uni: {}, UButton: {}, USwitch: {}};
vm.runInNewContext(script.replace('export default', 'module.exports ='), sandbox);
const component = sandbox.module.exports;
function instance(wx) {
  const target = Object.assign(component.data(), component.methods, {placeOptions: component.data().placeOptions, roomFormOpen: true, roomForm: {pic_url:'prior', id:'r1', display:'Room', place:'south', available:true}, roomEditing:true, roomSaving:false, wx});
  Object.defineProperty(target, 'roomImagePreview', {get: component.computed.roomImagePreview.bind(target)});
  return target;
}
function picker(wx, result) { wx.chooseImage = options => result(options); }

// Picker cancellation is quiet and releases all guards.
let w = {}; picker(w, o => o.fail({errMsg:'chooseImage:fail cancel'}));
let vm1 = instance(w); sandbox.wx = w; vm1.chooseRoomImage();
assert.strictEqual(vm1.roomImageBusy, false); assert.strictEqual(vm1.roomImageError, ''); assert.strictEqual(vm1.roomForm.pic_url, 'prior');

// Successful raw-byte upload updates the internal ID and local preview, while blocking save in flight.
let request; w = {chooseImage:o=>o.success({tempFilePaths:['/tmp/room.png']}), getFileSystemManager:()=>({readFile:o=>o.success({data:new ArrayBuffer(4)})}), login:o=>o.success({code:'fresh'}), request:o=>{request=o;}};
vm1 = instance(w); sandbox.wx = w; vm1.chooseRoomImage(); assert.strictEqual(vm1.roomImageBusy,true); vm1.saveRoom(); assert.strictEqual(vm1.roomSaving,false);
assert.strictEqual(request.url,'https://nkapi.ememememem.space/upload/classroom-image'); assert.strictEqual(request.header['X-Wechat-Code'],'fresh'); assert.strictEqual(request.header['content-type'],'application/octet-stream'); assert(request.data instanceof ArrayBuffer);
request.success({data:{success:true,pic_url:'generated-id'}});
assert.strictEqual(vm1.roomForm.pic_url,'generated-id'); assert.strictEqual(vm1.roomImagePreview,'/tmp/room.png'); assert.strictEqual(vm1.roomImageBusy,false);
vm1.removeRoomImage(); assert.strictEqual(vm1.roomForm.pic_url,''); assert.strictEqual(vm1.roomImagePreview,'');

// Read, login and server failures retain previous ID; each path releases busy state.
for (const mode of ['read','login','empty-login','request','shape','malformed-success','oversize']) {
  w = {chooseImage:o=>o.success({tempFilePaths:['/tmp/new.png']}), getFileSystemManager:()=>({readFile:o=>mode==='read'?o.fail({}):o.success({data:new ArrayBuffer(mode==='oversize'?5*1024*1024+1:2)})}), login:o=>mode==='login'?o.fail({}):o.success({code:mode==='empty-login'?'':'c'}), request:o=>mode==='request'?o.fail({}):o.success({data:mode==='malformed-success'?{success:true}:mode==='shape'?{success:false,error:'invalid_image'}:{success:false,error:'invalid_image'}})};
  vm1=instance(w); sandbox.wx = w; vm1.chooseRoomImage(); assert.strictEqual(vm1.roomImageBusy,false,mode); assert.strictEqual(vm1.roomForm.pic_url,'prior',mode); assert(vm1.roomImageError,mode);
}
// Empty selection hides preview, and all form-changing actions are guarded while picker is pending.
vm1=instance({}); vm1.roomForm.pic_url=''; assert.strictEqual(vm1.roomImagePreview,'');
let pickerCallbacks; w={chooseImage:o=>{pickerCallbacks=o;}}; sandbox.wx=w; vm1=instance(w); vm1.chooseRoomImage();
vm1.newRoom(); vm1.editRoom({id:'other'}); vm1.closeRoomForm(); vm1.removeRoomImage(); assert.strictEqual(vm1.roomForm.id,'r1'); assert.strictEqual(vm1.roomForm.pic_url,'prior'); assert.strictEqual(vm1.roomFormOpen,true);
// Picker errors are visible, but cancel remains quiet.
pickerCallbacks.fail({errMsg:'chooseImage:fail permission denied'}); assert(vm1.roomImageError); assert.strictEqual(vm1.roomImageBusy,false);
// Unload invalidates callbacks so a late response cannot modify the room.
w={chooseImage:o=>o.success({tempFilePaths:['/tmp/x']}),getFileSystemManager:()=>({readFile:o=>o.success({data:new ArrayBuffer(2)})}),login:o=>o.success({code:'c'}),request:o=>{request=o;}};
sandbox.wx=w; vm1=instance(w); vm1.chooseRoomImage(); component.onUnload.call(vm1); request.success({data:{success:true,pic_url:'stale'}}); assert.strictEqual(vm1.roomForm.pic_url,'prior');
// Save performs its own fresh login and sends the uploaded association (not upload credential).
let loginCount=0, saved, uploadRequest; w={chooseImage:o=>o.success({tempFilePaths:['/tmp/x']}),getFileSystemManager:()=>({readFile:o=>o.success({data:new ArrayBuffer(2)})}),login:o=>o.success({code:++loginCount===1?'upload-code':'save-code'}), request:o=>{if(o.url.includes('/upload/')) uploadRequest=o; else saved=o;}};
sandbox.wx=w; vm1=instance(w); vm1.chooseRoomImage(); uploadRequest.success({data:{success:true,pic_url:'newly-uploaded'}}); vm1.mutateRoom(vm1.roomForm,true,true,true);
assert.strictEqual(loginCount,2); assert.strictEqual(saved.data.code,'save-code'); assert.strictEqual(saved.data.pic_url,'newly-uploaded');
// Existing IDs still resolve to the room image endpoint.
vm1=instance({}); assert.strictEqual(vm1.roomImagePreview,'https://nkapi.ememememem.space/img/prior');
console.log('classroom image UI state checks passed');
