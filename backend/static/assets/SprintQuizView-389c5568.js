import{u as C,A as g}from"./use-swrv-1943a49d.js";import{L as h}from"./LoadingPreview-38bddb96.js";import{P as v}from"./PaginatorControl-9549c4eb.js";import{T as x,a as $}from"./TableViewLine-5f447312.js";import{C as b}from"./ClickableContainer-a587937b.js";import{d as z,i as V,r as q,w as p,c as u,u as e,F as m,a as n,b as d,e as f,o as s,f as B,h as L,k as y}from"./index-2d62b16b.js";import"./modulepreload-polyfill-3cfb730f.js";/* empty css               */const A={class:"inner"},W=z({__name:"SprintQuizView",setup(P){const _=V(),o=q(1),{data:a,error:k,mutate:w}=C(`/sprints/quiz/${_.params.uuid}/users`,r=>L(r,{p:o.value}));return p(o,()=>w()),p(k,r=>{(r==null?void 0:r.code)==404&&y.push({path:"/sprints"})}),(r,i)=>{var c,l;return s(),u("div",A,[e(a)!=null?(s(),u(m,{key:0},[n(e(b),{image:e(a).quiz.image},null,8,["image"]),n(e(g),{title:e(a).quiz.name},{default:d(()=>[n(e(x),{header:["User Name","Current Status","Incorrect Attempts"]},{default:d(()=>[(s(!0),u(m,null,B(e(a).view,t=>(s(),f(e($),{key:t.uuid,rows:[t.full_name,{text:t.current_status,color:t.current_status==="correct"?"confirm":t.current_status==="incorrect"?"cancel":"blue"},t.incorrect_attempts],onClick:S=>r.$router.push(`/sprint/quiz/${r.$route.params.uuid}/${t.uuid}`)},null,8,["rows","onClick"]))),128))]),_:1})]),_:1},8,["title"]),n(e(v),{current:o.value,"onUpdate:current":i[0]||(i[0]=t=>o.value=t),max:((l=(c=e(a))==null?void 0:c.paginator)==null?void 0:l.max)??1},null,8,["current","max"])],64)):(s(),f(e(h),{key:1}))])}}});export{W as default};