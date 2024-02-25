import{u as T,A as P}from"./use-swrv-1943a49d.js";import{L as U}from"./LoadingPreview-38bddb96.js";import{P as D}from"./PaginatorControl-9549c4eb.js";import{T as E,a as F}from"./TableViewLine-5f447312.js";import{C as d}from"./ClickableContainer-a587937b.js";import{d as M,i as R,r as B,w as W,m as j,c as r,u as e,F as u,n as i,a as o,j as w,b as _,e as p,o as n,f as I,A as f,t as L,M as G,p as H,g as J,h as K}from"./index-2d62b16b.js";import{I as O}from"./InfoView-5a51acd2.js";import"./modulepreload-polyfill-3cfb730f.js";/* empty css               */const Q={class:"inner"},X={"d-flex":"h"},Y={key:0,"d-flex":"h"},Z=i("span",null,"Sprint is currently closed because the user has not finished testing yet",-1),ee={key:1,"d-flex":"h"},te=i("span",null,"Sprint closed as unsolved.",-1),se={key:2,"d-flex":"h"},ne=i("span",null,"Sprint closed as solved",-1),oe=i("h1",null,"Description",-1),ae=i("h1",null,"User Answer",-1),ie=i("h1",null,"Answers",-1),le={"d-flex":"h wp"},re=i("h1",null,"Correct Answer",-1),ue=i("h1",null,"User Answer",-1),ye=M({__name:"SprintItem",setup(ce){const N=R(),t=B(null),h=async v=>{var c;if((await H(`/sprint/answer/${(c=t.value)==null?void 0:c.uuid}/verify`,{data:{valid:v}})).status!=200){J.notify("Error on server side, try later!!!");return}t.value=null,await y()},m=B(1),{data:l,mutate:y}=T(`/sprint/${N.params.uuid}/answers`,v=>K(v,{p:m.value}));return W(m,()=>y()),(v,a)=>{var x,g,C,q;const c=j("mdicon");return n(),r("div",Q,[e(l)!=null?(n(),r(u,{key:0},[i("div",X,[o(e(d),{image:e(l).sprint.quiz_image},null,8,["image"]),o(e(d),{image:e(l).sprint.user_image},null,8,["image"])]),e(l).sprint.status=="while_taking"?(n(),r("div",Y,[o(c,{name:"progress-clock"}),Z])):e(l).sprint.status=="incorrect"?(n(),r("div",ee,[o(c,{name:"close"}),te])):e(l).sprint.status=="correct"?(n(),r("div",se,[o(c,{name:"check"}),ne])):w("",!0),o(e(P),{title:e(l).sprint.quiz+" (by "+e(l).sprint.user+")"},{default:_(()=>[o(e(E),{header:["Name","Type","Status"]},{default:_(()=>[(n(!0),r(u,null,I(e(l).view,s=>(n(),p(e(F),{onClick:k=>t.value=s,key:s.uuid,rows:[s.question.name,s.question.type,{text:s.status,color:s.status==="correct"?"confirm":s.status==="incorrect"?"cancel":"blue"}]},null,8,["onClick","rows"]))),128))]),_:1})]),_:1},8,["title"]),o(e(D),{current:m.value,"onUpdate:current":a[0]||(a[0]=s=>m.value=s),max:((g=(x=e(l))==null?void 0:x.paginator)==null?void 0:g.max)??1},null,8,["current","max"]),o(e(G),{visible:t.value!=null,onClose:a[5]||(a[5]=s=>t.value=null),title:(q=(C=t.value)==null?void 0:C.question)==null?void 0:q.name},{actions:_(()=>[e(l).sprint.status=="on_verification"&&t.value.status=="on_verification"?(n(),r(u,{key:0},[o(e(f),{text:"Cancel",size:"ex",color:"cancel",onClick:a[1]||(a[1]=s=>t.value=null)}),o(e(f),{text:"Incorrect",size:"ex",color:"cancel",onClick:a[2]||(a[2]=s=>h(!1))}),o(e(f),{text:"Correct",size:"ex",color:"confirm",onClick:a[3]||(a[3]=s=>h(!0))})],64)):(n(),p(e(f),{key:1,text:"Close",size:"ex",color:"cancel",onClick:a[4]||(a[4]=s=>t.value=null)}))]),default:_(()=>{var s,k,b,A,S,$,V;return[(s=t.value)!=null&&s.question.image?(n(),p(e(d),{key:0,image:(k=t.value)==null?void 0:k.question.image},null,8,["image"])):w("",!0),o(e(O),{items:{Status:(b=t.value)==null?void 0:b.status}},null,8,["items"]),(A=t.value)!=null&&A.question.description?(n(),r(u,{key:1},[oe,i("span",null,L((S=t.value)==null?void 0:S.question.description),1)],64)):w("",!0),(($=t.value)==null?void 0:$.question.type)=="text"?(n(),r(u,{key:2},[ae,i("span",null,L((V=t.value)==null?void 0:V.text_answer),1)],64)):(n(),r(u,{key:3},[ie,i("div",le,[(n(!0),r(u,null,I(t.value.question.answers,z=>(n(),p(e(d),{key:z.uuid,title:z.name},null,8,["title"]))),128))]),re,o(e(d),{title:t.value.question.correct_answer.name},null,8,["title"]),ue,o(e(d),{title:t.value.option_answer.name},null,8,["title"])],64))]}),_:1},8,["visible","title"])],64)):(n(),p(e(U),{key:1}))])}}});export{ye as default};