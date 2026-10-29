// Focused, dependency-free state test. wx callbacks are held locally; no network calls.
const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
const source = fs.readFileSync('miniprogram/pages_individual/admin_tool/adminTool.vue', 'utf8');
const script = source.match(/<script>([\s\S]*?)<\/script>/)[1].replace(/^import .*;\s*$/gm, '').replace('export default', 'module.exports =');
const loaded = {exports:{}};
const sandbox = {module:loaded, wx:null, uni:null, UButton:{}, USwitch:{}};
vm.runInNewContext(script, sandbox);
const component = loaded.exports;
const methods = component.methods;
const room = {id:'R-7', display:'南楼 201'};
function setup({confirm=true, loginCode='fresh-code', loginFail=false, response={statusCode:200,data:{success:true,deleted_records:4}}, imageBusy=false, hold=false}={}) {
  const requests=[]; let loginCalls=0; let modal; let loginOptions; let requestOptions;
  const ctx = Object.assign(component.data(), {classrooms:[room,{id:'other'}], reservations:[{classroom_id:'R-7'},{classroom_id:'other'}],users:[{id:'u'}],cycRecordIds:[{record_id:'1,'}], roomImageBusy:imageBusy, roomFormOpen:true, roomEditing:true, roomForm:{id:'R-7'}, resetRoomImageOperation(){this.roomImageOperation++;this.roomImageBusy=false;this.roomImageLocalPath='';}});
  const wx={login(o){loginCalls++;loginOptions=o;if(!hold){if(loginFail)o.fail();else o.success({code:loginCode});}},request(o){requests.push(o);if(!requestOptions)requestOptions=o;if(!hold){if(o.success)o.success(response);if(o.complete)o.complete();}},chooseImage(){throw Error('image should be blocked');},showToast(){}};
  const uni={showModal(o){modal=o;o.success({confirm});}};
  Object.keys(methods).forEach(k=>ctx[k]=methods[k].bind(ctx));
  sandbox.wx=wx;sandbox.uni=uni;
  return {ctx,requests,get loginCalls(){return loginCalls;},get modal(){return modal;},get loginOptions(){return loginOptions;},get requestOptions(){return requestOptions;}};
}
function confirm(h){h.ctx.confirmDeleteClassroom(room);}
{
 const h=setup({confirm:false});confirm(h);assert.equal(h.loginCalls,0);assert.equal(h.requests.length,0);assert.equal(h.ctx.classrooms.length,2);
}
{
 const h=setup();confirm(h);const req=h.requests[0];assert.equal(h.loginCalls,1);assert.equal(req.url,'https://nkapi.ememememem.space/delete/classroom/');assert.equal(req.method,'POST');assert.deepEqual(JSON.parse(JSON.stringify(req.data)),{code:'fresh-code',id:'R-7'});assert(!('uid'in req.data)&&!('cond'in req.data));assert(h.modal.content.includes(room.display)&&h.modal.content.includes('周期预约')&&h.modal.content.includes('无法撤销'));assert.deepEqual(h.ctx.classrooms.map(x=>x.id),['other']);assert.equal(h.ctx.reservations.length,1);assert.equal(h.ctx.roomFormOpen,false);assert.equal(h.ctx.roomDeleting,false);assert.deepEqual(h.requests.slice(1).map(x=>x.url),['https://nkapi.ememememem.space/query/classroom','https://nkapi.ememememem.space/query/record','https://nkapi.ememememem.space/query/user','https://nkapi.ememememem.space/query/cyclical']);
}
{
 const h=setup({hold:true});confirm(h);assert.equal(h.ctx.roomDeleting,true);h.ctx.newRoom();h.ctx.editRoom({id:'other'});h.ctx.saveRoom();h.ctx.chooseRoomImage();h.ctx.removeRoomImage();h.ctx.closeRoomForm();h.ctx.confirmDeleteClassroom({id:'other'});h.ctx.confirmRoomAvailability({id:'other'});assert.equal(h.loginCalls,1);assert.equal(h.requests.length,0);assert.equal(h.ctx.roomForm.id,'R-7');h.loginOptions.success({code:'fresh-code'});assert.equal(h.ctx.roomDeleting,true);h.ctx.confirmDeleteClassroom(room);h.ctx.saveRoom();h.ctx.chooseRoomImage();assert.equal(h.requests.length,1);assert.equal(h.loginCalls,1);h.requestOptions.success({statusCode:200,data:{success:true,deleted_records:1}});h.requestOptions.complete();assert.equal(h.ctx.roomDeleting,false);
}
{
 const image=setup({imageBusy:true});confirm(image);assert.equal(image.loginCalls,0);assert.equal(image.ctx.roomDeleting,false);
 const loginFail=setup({loginFail:true});confirm(loginFail);assert(loginFail.ctx.roomActionError);assert.equal(loginFail.ctx.roomDeleting,false);assert.equal(loginFail.ctx.classrooms.length,2);
 const noCode=setup({loginCode:''});confirm(noCode);assert.equal(noCode.requests.length,0);assert(noCode.ctx.roomActionError);assert.equal(noCode.ctx.roomDeleting,false);
 for (const response of [{statusCode:403,data:{success:false,error:'unauthorized'}},{statusCode:200,data:{success:false,error:'unknown_classroom'}},{statusCode:500,data:{success:true,deleted_records:1}}]) { const h=setup({response});confirm(h);assert(h.ctx.roomActionError);assert.equal(h.ctx.classrooms.length,2);assert.equal(h.ctx.reservations.length,2);assert.equal(h.ctx.roomDeleting,false); }
 const network=setup({hold:true});confirm(network);network.loginOptions.success({code:'fresh-code'});network.requestOptions.fail();assert(network.ctx.roomActionError.includes('未能确认'));assert.equal(network.ctx.classrooms.length,2);assert.equal(network.ctx.reservations.length,2);network.requestOptions.complete();assert.equal(network.ctx.roomDeleting,false);
 const otherDraft=setup({response:{statusCode:200,data:{success:true,deleted_records:2}}});otherDraft.ctx.roomForm.id='other';confirm(otherDraft);assert.equal(otherDraft.ctx.roomFormOpen,true);assert.equal(otherDraft.ctx.roomForm.id,'other');
}
console.log('classroom deletion UI checks passed');
