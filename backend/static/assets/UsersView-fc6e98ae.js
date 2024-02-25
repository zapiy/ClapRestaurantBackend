import{u as U,A as V}from"./use-swrv-1943a49d.js";import{L as $}from"./LoadingPreview-38bddb96.js";import{P as E}from"./PaginatorControl-9549c4eb.js";import{T as j,a as q}from"./TableViewLine-5f447312.js";import{C as z}from"./ClickableContainer-a587937b.js";import{S as L}from"./SearchControl-e14092d3.js";import{d as W,r as g,w as A,c as v,u as e,F as h,a as s,b as i,e as x,o as u,A as p,f as N,M as P,p as C,s as T,g as f,h as I}from"./index-2d62b16b.js";import{p as w}from"./formatDate-1a01982f.js";import{I as M}from"./InfoView-5a51acd2.js";import"./modulepreload-polyfill-3cfb730f.js";/* empty css               */const R={class:"inner"},ra=W({__name:"UsersView",setup(Q){const r=g(null),_=async()=>{var a;console.log("Switching user");const l=await C(`/user/${(a=r.value)==null?void 0:a.uuid}`,{data:{op:"switch"}});r.value=await l.json(),await d()},F=async()=>{const l=r.value,a=await T(["jpg","jpeg","png"]),o=new FormData;o.append("avatar",a);const n=await C(`/user/${l==null?void 0:l.uuid}`,{data:o});n.status!=200&&(n.status>=500?f.notify("Error on server side, try later!!!"):n.status==406&&f.notify("Validation error, most likely this email is registered, use the search")),r.value=await n.json(),await d()},b=(l=!1)=>{const a=r.value;r.value=null,f.showDialog({title:"Add user",inputs:{full_name:{placeholder:"Full Name",min:1,max:150,value:l?a==null?void 0:a.full_name:null},email:{placeholder:"Email",type:"email",max:120,value:l?a==null?void 0:a.email:null},birthday:{placeholder:"Birthday",type:"date",value:l?a==null?void 0:a.birthday:null},working_at:{placeholder:"Start Working Day",type:"date",value:l?a==null?void 0:a.working_at:Date.now()}},handle:async function(o){return(await C(`/user/${(a==null?void 0:a.uuid)??"new"}`,{data:o})).status!=200?(f.notify("Error on server side, try later!!!"),!1):(await d(),!0)}})},m=g(1),c=g(),{data:y,mutate:d}=U("/users",l=>{const a={p:m.value};return c.value&&(a.q=c.value),I(l,a)});return A(m,()=>d()),A(c,()=>d()),(l,a)=>{var o,n,D;return u(),v("div",R,[e(y)!=null?(u(),v(h,{key:0},[s(e(V),{title:"Users"},{center:i(()=>[s(L,{query:c.value,"onUpdate:query":a[0]||(a[0]=t=>c.value=t)},null,8,["query"])]),actions:i(()=>[s(e(p),{text:"Add user",onClick:b})]),default:i(()=>[s(e(j),{header:["Full Name","Birthday","Start Working Day","Status"]},{default:i(()=>[(u(!0),v(h,null,N(e(y).view,t=>(u(),x(e(q),{key:t.uuid,onClick:k=>r.value=t,rows:[t.full_name,e(w)({date:t.birthday,useDate:!0}),e(w)({date:t.working_at,useDate:!0}),t==null?void 0:t.status]},null,8,["onClick","rows"]))),128))]),_:1})]),_:1}),s(e(E),{current:m.value,"onUpdate:current":a[1]||(a[1]=t=>m.value=t),max:((n=(o=e(y))==null?void 0:o.paginator)==null?void 0:n.max)??1},null,8,["current","max"])],64)):(u(),x(e($),{key:1})),s(e(P),{visible:r.value!=null,onClose:a[4]||(a[4]=t=>r.value=null),title:(D=r.value)==null?void 0:D.full_name},{actions:i(()=>[s(e(p),{text:"Cancel",size:"ex",color:"cancel",onClick:a[2]||(a[2]=t=>r.value=null)}),r.value.status=="leave"?(u(),x(e(p),{key:0,text:"Restore",size:"ex",color:"confirm",onClick:_})):(u(),v(h,{key:1},[s(e(p),{text:"Fired",size:"ex",color:"cancel",onClick:_}),s(e(p),{text:"Edit",size:"ex",onClick:a[3]||(a[3]=()=>b(!0))})],64))]),default:i(()=>{var t,k,S,B;return[s(e(z),{onClick:F,image:(t=r.value)==null?void 0:t.avatar},null,8,["image"]),s(e(M),{items:{Birthday:e(w)({date:(k=r.value)==null?void 0:k.birthday,useDate:!0}),"Start working day":e(w)({date:(S=r.value)==null?void 0:S.working_at,useDate:!0}),Status:(B=r.value)==null?void 0:B.status}},null,8,["items"])]}),_:1},8,["visible","title"])])}}});export{ra as default};