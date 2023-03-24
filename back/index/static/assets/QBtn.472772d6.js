import{c as i,$ as h,ad as I,ah as ee,ai as te,ac as Y,aj as ne,a0 as G,a as N,a1 as ae,K as re,a5 as T,I as le,ak as ue,a9 as ie}from"./index.17c08fe6.js";import{u as D,c as J,a as se,b as oe,d as ce,Q,e as de}from"./QIcon.49739c9a.js";const fe={size:{type:[Number,String],default:"1em"},color:String};function ve(e){return{cSize:i(()=>e.size in D?`${D[e.size]}px`:e.size),classes:i(()=>"q-spinner"+(e.color?` text-${e.color}`:""))}}var ge=J({name:"QSpinner",props:{...fe,thickness:{type:Number,default:5}},setup(e){const{cSize:t,classes:r}=ve(e);return()=>h("svg",{class:r.value+" q-spinner-mat",width:t.value,height:t.value,viewBox:"25 25 50 50"},[h("circle",{class:"path",cx:"50",cy:"50",r:"20",fill:"none",stroke:"currentColor","stroke-width":e.thickness,"stroke-miterlimit":"10"})])}});function me(e,t){const r=e.style;for(const n in t)r[n]=t[n]}function be(e,t=250){let r=!1,n;return function(){return r===!1&&(r=!0,setTimeout(()=>{r=!1},t),n=e.apply(this,arguments)),n}}function V(e,t,r,n){r.modifiers.stop===!0&&Y(e);const u=r.modifiers.color;let m=r.modifiers.center;m=m===!0||n===!0;const f=document.createElement("span"),d=document.createElement("span"),E=ne(e),{left:y,top:v,width:$,height:l}=t.getBoundingClientRect(),k=Math.sqrt($*$+l*l),g=k/2,p=`${($-k)/2}px`,s=m?p:`${E.left-y-g}px`,b=`${(l-k)/2}px`,R=m?b:`${E.top-v-g}px`;d.className="q-ripple__inner",me(d,{height:`${k}px`,width:`${k}px`,transform:`translate3d(${s},${R},0) scale3d(.2,.2,1)`,opacity:0}),f.className=`q-ripple${u?" text-"+u:""}`,f.setAttribute("dir","ltr"),f.appendChild(d),t.appendChild(f);const P=()=>{f.remove(),clearTimeout(B)};r.abort.push(P);let B=setTimeout(()=>{d.classList.add("q-ripple__inner--enter"),d.style.transform=`translate3d(${p},${b},0) scale3d(1,1,1)`,d.style.opacity=.2,B=setTimeout(()=>{d.classList.remove("q-ripple__inner--enter"),d.classList.add("q-ripple__inner--leave"),d.style.opacity=0,B=setTimeout(()=>{f.remove(),r.abort.splice(r.abort.indexOf(P),1)},275)},250)},50)}function H(e,{modifiers:t,value:r,arg:n}){const u=Object.assign({},e.cfg.ripple,t,r);e.modifiers={early:u.early===!0,stop:u.stop===!0,center:u.center===!0,color:u.color||n,keyCodes:[].concat(u.keyCodes||13)}}var he=se({name:"ripple",beforeMount(e,t){const r=t.instance.$.appContext.config.globalProperties.$q.config||{};if(r.ripple===!1)return;const n={cfg:r,enabled:t.value!==!1,modifiers:{},abort:[],start(u){n.enabled===!0&&u.qSkipRipple!==!0&&u.type===(n.modifiers.early===!0?"pointerdown":"click")&&V(u,e,n,u.qKeyEvent===!0)},keystart:be(u=>{n.enabled===!0&&u.qSkipRipple!==!0&&I(u,n.modifiers.keyCodes)===!0&&u.type===`key${n.modifiers.early===!0?"down":"up"}`&&V(u,e,n,!0)},300)};H(n,t),e.__qripple=n,ee(n,"main",[[e,"pointerdown","start","passive"],[e,"click","start","passive"],[e,"keydown","keystart","passive"],[e,"keyup","keystart","passive"]])},updated(e,t){if(t.oldValue!==t.value){const r=e.__qripple;r!==void 0&&(r.enabled=t.value!==!1,r.enabled===!0&&Object(t.value)===t.value&&H(r,t))}},beforeUnmount(e){const t=e.__qripple;t!==void 0&&(t.abort.forEach(r=>{r()}),te(t,"main"),delete e._qripple)}});const Z={left:"start",center:"center",right:"end",between:"between",around:"around",evenly:"evenly",stretch:"stretch"},ye=Object.keys(Z),ke={align:{type:String,validator:e=>ye.includes(e)}};function pe(e){return i(()=>{const t=e.align===void 0?e.vertical===!0?"stretch":"left":e.align;return`${e.vertical===!0?"items":"justify"}-${Z[t]}`})}function qe(e){return e.appContext.config.globalProperties.$router!==void 0}function W(e){return e?e.aliasOf?e.aliasOf.path:e.path:""}function U(e,t){return(e.aliasOf||e)===(t.aliasOf||t)}function xe(e,t){for(const r in t){const n=t[r],u=e[r];if(typeof n=="string"){if(n!==u)return!1}else if(Array.isArray(u)===!1||u.length!==n.length||n.some((m,f)=>m!==u[f]))return!1}return!0}function X(e,t){return Array.isArray(t)===!0?e.length===t.length&&e.every((r,n)=>r===t[n]):e.length===1&&e[0]===t}function $e(e,t){return Array.isArray(e)===!0?X(e,t):Array.isArray(t)===!0?X(t,e):e===t}function Ce(e,t){if(Object.keys(e).length!==Object.keys(t).length)return!1;for(const r in e)if($e(e[r],t[r])===!1)return!1;return!0}const Le={to:[String,Object],replace:Boolean,exact:Boolean,activeClass:{type:String,default:"q-router-link--active"},exactActiveClass:{type:String,default:"q-router-link--exact-active"},href:String,target:String,disable:Boolean};function Se({fallbackTag:e,useDisableForRouterLinkProps:t=!0}={}){const r=G(),{props:n,proxy:u,emit:m}=r,f=qe(r),d=i(()=>n.disable!==!0&&n.href!==void 0),E=t===!0?i(()=>f===!0&&n.disable!==!0&&d.value!==!0&&n.to!==void 0&&n.to!==null&&n.to!==""):i(()=>f===!0&&d.value!==!0&&n.to!==void 0&&n.to!==null&&n.to!==""),y=i(()=>E.value===!0?R(n.to):null),v=i(()=>y.value!==null),$=i(()=>d.value===!0||v.value===!0),l=i(()=>n.type==="a"||$.value===!0?"a":n.tag||e||"div"),k=i(()=>d.value===!0?{href:n.href,target:n.target}:v.value===!0?{href:y.value.href,target:n.target}:{}),g=i(()=>{if(v.value===!1)return-1;const{matched:o}=y.value,{length:q}=o,C=o[q-1];if(C===void 0)return-1;const S=u.$route.matched;if(S.length===0)return-1;const w=S.findIndex(U.bind(null,C));if(w>-1)return w;const z=W(o[q-2]);return q>1&&W(C)===z&&S[S.length-1].path!==z?S.findIndex(U.bind(null,o[q-2])):w}),p=i(()=>v.value===!0&&g.value!==-1&&xe(u.$route.params,y.value.params)),s=i(()=>p.value===!0&&g.value===u.$route.matched.length-1&&Ce(u.$route.params,y.value.params)),b=i(()=>v.value===!0?s.value===!0?` ${n.exactActiveClass} ${n.activeClass}`:n.exact===!0?"":p.value===!0?` ${n.activeClass}`:"":"");function R(o){try{return u.$router.resolve(o)}catch{}return null}function P(o,{returnRouterError:q,to:C=n.to,replace:S=n.replace}={}){if(n.disable===!0)return o.preventDefault(),Promise.resolve(!1);if(o.metaKey||o.altKey||o.ctrlKey||o.shiftKey||o.button!==void 0&&o.button!==0||n.target==="_blank")return Promise.resolve(!1);o.preventDefault();const w=u.$router[S===!0?"replace":"push"](C);return q===!0?w:w.then(()=>{}).catch(()=>{})}function B(o){if(v.value===!0){const q=C=>P(o,C);m("click",o,q),o.defaultPrevented!==!0&&q()}else m("click",o)}return{hasRouterLink:v,hasHrefLink:d,hasLink:$,linkTag:l,resolvedLink:y,linkIsActive:p,linkIsExactActive:s,linkClass:b,linkAttrs:k,getLink:R,navigateToRouterLink:P,navigateOnClick:B}}const F={none:0,xs:4,sm:8,md:16,lg:24,xl:32},Ee={xs:8,sm:10,md:14,lg:20,xl:24},we=["button","submit","reset"],Pe=/[^\s]\/[^\s]/,Be=["flat","outline","push","unelevated"],Re=(e,t)=>e.flat===!0?"flat":e.outline===!0?"outline":e.push===!0?"push":e.unelevated===!0?"unelevated":t,Te={...oe,...Le,type:{type:String,default:"button"},label:[Number,String],icon:String,iconRight:String,...Be.reduce((e,t)=>(e[t]=Boolean)&&e,{}),square:Boolean,round:Boolean,rounded:Boolean,glossy:Boolean,size:String,fab:Boolean,fabMini:Boolean,padding:String,color:String,textColor:String,noCaps:Boolean,noWrap:Boolean,dense:Boolean,tabindex:[Number,String],ripple:{type:[Boolean,Object],default:!0},align:{...ke.align,default:"center"},stack:Boolean,stretch:Boolean,loading:{type:Boolean,default:null},disable:Boolean};function _e(e){const t=ce(e,Ee),r=pe(e),{hasRouterLink:n,hasLink:u,linkTag:m,linkAttrs:f,navigateOnClick:d}=Se({fallbackTag:"button"}),E=i(()=>{const s=e.fab===!1&&e.fabMini===!1?t.value:{};return e.padding!==void 0?Object.assign({},s,{padding:e.padding.split(/\s+/).map(b=>b in F?F[b]+"px":b).join(" "),minWidth:"0",minHeight:"0"}):s}),y=i(()=>e.rounded===!0||e.fab===!0||e.fabMini===!0),v=i(()=>e.disable!==!0&&e.loading!==!0),$=i(()=>v.value===!0?e.tabindex||0:-1),l=i(()=>Re(e,"standard")),k=i(()=>{const s={tabindex:$.value};return u.value===!0?Object.assign(s,f.value):we.includes(e.type)===!0&&(s.type=e.type),m.value==="a"?(e.disable===!0?s["aria-disabled"]="true":s.href===void 0&&(s.role="button"),n.value!==!0&&Pe.test(e.type)===!0&&(s.type=e.type)):e.disable===!0&&(s.disabled="",s["aria-disabled"]="true"),e.loading===!0&&e.percentage!==void 0&&Object.assign(s,{role:"progressbar","aria-valuemin":0,"aria-valuemax":100,"aria-valuenow":e.percentage}),s}),g=i(()=>{let s;e.color!==void 0?e.flat===!0||e.outline===!0?s=`text-${e.textColor||e.color}`:s=`bg-${e.color} text-${e.textColor||"white"}`:e.textColor&&(s=`text-${e.textColor}`);const b=e.round===!0?"round":`rectangle${y.value===!0?" q-btn--rounded":e.square===!0?" q-btn--square":""}`;return`q-btn--${l.value} q-btn--${b}`+(s!==void 0?" "+s:"")+(v.value===!0?" q-btn--actionable q-focusable q-hoverable":e.disable===!0?" disabled":"")+(e.fab===!0?" q-btn--fab":e.fabMini===!0?" q-btn--fab-mini":"")+(e.noCaps===!0?" q-btn--no-uppercase":"")+(e.dense===!0?" q-btn--dense":"")+(e.stretch===!0?" no-border-radius self-stretch":"")+(e.glossy===!0?" glossy":"")+(e.square?" q-btn--square":"")}),p=i(()=>r.value+(e.stack===!0?" column":" row")+(e.noWrap===!0?" no-wrap text-no-wrap":"")+(e.loading===!0?" q-btn__content--hidden":""));return{classes:g,style:E,innerClasses:p,attributes:k,hasLink:u,linkTag:m,navigateOnClick:d,isActionable:v}}const{passiveCapture:x}=ue;let _=null,A=null,O=null;var Me=J({name:"QBtn",props:{...Te,percentage:Number,darkPercentage:Boolean,onTouchstart:[Function,Array]},emits:["click","keydown","mousedown","keyup"],setup(e,{slots:t,emit:r}){const{proxy:n}=G(),{classes:u,style:m,innerClasses:f,attributes:d,hasLink:E,linkTag:y,navigateOnClick:v,isActionable:$}=_e(e),l=N(null),k=N(null);let g=null,p,s;const b=i(()=>e.label!==void 0&&e.label!==null&&e.label!==""),R=i(()=>e.disable===!0||e.ripple===!1?!1:{keyCodes:E.value===!0?[13,32]:[13],...e.ripple===!0?{}:e.ripple}),P=i(()=>({center:e.round})),B=i(()=>{const a=Math.max(0,Math.min(100,e.percentage));return a>0?{transition:"transform 0.6s",transform:`translateX(${a-100}%)`}:{}}),o=i(()=>{if(e.loading===!0)return{onMousedown:j,onTouchstart:j,onClick:j,onKeydown:j,onKeyup:j};if($.value===!0){const a={onClick:C,onKeydown:S,onMousedown:z};if(n.$q.platform.has.touch===!0){const c=e.onTouchstart!==void 0?"":"Passive";a[`onTouchstart${c}`]=w}return a}return{onClick:T}}),q=i(()=>({ref:l,class:"q-btn q-btn-item non-selectable no-outline "+u.value,style:m.value,...d.value,...o.value}));function C(a){if(l.value!==null){if(a!==void 0){if(a.defaultPrevented===!0)return;const c=document.activeElement;if(e.type==="submit"&&c!==document.body&&l.value.contains(c)===!1&&c.contains(l.value)===!1){l.value.focus();const K=()=>{document.removeEventListener("keydown",T,!0),document.removeEventListener("keyup",K,x),l.value!==null&&l.value.removeEventListener("blur",K,x)};document.addEventListener("keydown",T,!0),document.addEventListener("keyup",K,x),l.value.addEventListener("blur",K,x)}}v(a)}}function S(a){l.value!==null&&(r("keydown",a),I(a,[13,32])===!0&&A!==l.value&&(A!==null&&M(),a.defaultPrevented!==!0&&(l.value.focus(),A=l.value,l.value.classList.add("q-btn--active"),document.addEventListener("keyup",L,!0),l.value.addEventListener("blur",L,x)),T(a)))}function w(a){l.value!==null&&(r("touchstart",a),a.defaultPrevented!==!0&&(_!==l.value&&(_!==null&&M(),_=l.value,g=a.target,g.addEventListener("touchcancel",L,x),g.addEventListener("touchend",L,x)),p=!0,clearTimeout(s),s=setTimeout(()=>{p=!1},200)))}function z(a){l.value!==null&&(a.qSkipRipple=p===!0,r("mousedown",a),a.defaultPrevented!==!0&&O!==l.value&&(O!==null&&M(),O=l.value,l.value.classList.add("q-btn--active"),document.addEventListener("mouseup",L,x)))}function L(a){if(l.value!==null&&!(a!==void 0&&a.type==="blur"&&document.activeElement===l.value)){if(a!==void 0&&a.type==="keyup"){if(A===l.value&&I(a,[13,32])===!0){const c=new MouseEvent("click",a);c.qKeyEvent=!0,a.defaultPrevented===!0&&ie(c),a.cancelBubble===!0&&Y(c),l.value.dispatchEvent(c),T(a),a.qKeyEvent=!0}r("keyup",a)}M()}}function M(a){const c=k.value;a!==!0&&(_===l.value||O===l.value)&&c!==null&&c!==document.activeElement&&(c.setAttribute("tabindex",-1),c.focus()),_===l.value&&(g!==null&&(g.removeEventListener("touchcancel",L,x),g.removeEventListener("touchend",L,x)),_=g=null),O===l.value&&(document.removeEventListener("mouseup",L,x),O=null),A===l.value&&(document.removeEventListener("keyup",L,!0),l.value!==null&&l.value.removeEventListener("blur",L,x),A=null),l.value!==null&&l.value.classList.remove("q-btn--active")}function j(a){T(a),a.qSkipRipple=!0}return ae(()=>{M(!0)}),Object.assign(n,{click:C}),()=>{let a=[];e.icon!==void 0&&a.push(h(Q,{name:e.icon,left:e.stack===!1&&b.value===!0,role:"img","aria-hidden":"true"})),b.value===!0&&a.push(h("span",{class:"block"},[e.label])),a=de(t.default,a),e.iconRight!==void 0&&e.round===!1&&a.push(h(Q,{name:e.iconRight,right:e.stack===!1&&b.value===!0,role:"img","aria-hidden":"true"}));const c=[h("span",{class:"q-focus-helper",ref:k})];return e.loading===!0&&e.percentage!==void 0&&c.push(h("span",{class:"q-btn__progress absolute-full overflow-hidden"+(e.darkPercentage===!0?" q-btn__progress--dark":"")},[h("span",{class:"q-btn__progress-indicator fit block",style:B.value})])),c.push(h("span",{class:"q-btn__content text-center col items-center q-anchor--skip "+f.value},a)),e.loading!==null&&c.push(h(le,{name:"q-transition--fade"},()=>e.loading===!0?[h("span",{key:"loading",class:"absolute-full flex flex-center"},t.loading!==void 0?t.loading():[h(ge)])]:null)),re(h(y.value,q.value,c),[[he,R.value,void 0,P.value]])}}});export{ge as Q,Me as a,Be as b,F as c,Re as g};
