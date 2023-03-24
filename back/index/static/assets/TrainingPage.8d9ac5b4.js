import{i as a}from"./api.38b5689c.js";import{_ as g,e as f,f as y,C as t,B as u,K as l,U as d,g as h,ag as _,G as k,F as V,Y as m,V as w,W as P}from"./index.17c08fe6.js";import"./index.2cf0d985.js";import"./TokenService.d94e02eb.js";let x="extract_entity_proj",b="retrain_proj";class S{getDocExtensions(){return a.get("extensions/")}getExtractProj(){return a.get("proj_settings/",{params:{proj:x}})}getRetrainProj(){return a.get("proj_settings/",{params:{proj:b}})}getDocStatus(){return a.get("doc_status/")}updateExtractEntity(o){return a.patch("proj_settings/",{options:o},{params:{proj:x}})}updateRetrainProj(o){return a.patch("proj_settings/",{options:o},{params:{proj:b}})}startProject(o){return o.action="start_proj",a.post("proj_control/",o)}statusProject(o){return o.action="status_proj",a.post("proj_control/",o)}stopProject(o){return o.action="stop_proj",a.post("proj_control/",o)}}var p=new S;const U={name:"TrainingPage",data(){return{extract_proj:{options:{}},doc_extensions:[],doc_status:[],retrain_proj:{options:{}},field_translation:{all:"\u0421\u043E\u0435\u0434\u0438\u043D\u0435\u043D\u0438\u0435 \u043A \u0431\u0430\u0437\u0435 \u0434\u0430\u043D\u043D\u044B\u0445",extract_entity_proj:"\u0418\u0437\u0432\u043B\u0435\u0447\u0435\u043D\u0438\u0435 \u0438\u043C\u0435\u043D\u043D\u043E\u0432\u0430\u043D\u043D\u044B\u0445 \u0441\u0443\u0449\u043D\u043E\u0441\u0442\u0435\u0439"}}},methods:{toggle_panel(i){let o=i.target.closest(".panel").querySelector(".panel-ico"),c=i.target.closest(".panel").querySelector(".panel-content");o.classList.contains("rotate-180")?(o.classList.remove("rotate-180"),c.classList.add("hide"),setTimeout(()=>{c.classList.remove("visible")},100)):(c.classList.remove("hide"),o.classList.add("rotate-180"),c.classList.add("visible"))},getInitData(){p.getDocExtensions().then(i=>{this.doc_extensions=i.data}),p.getExtractProj().then(i=>{this.extract_proj=i.data}),p.getRetrainProj().then(i=>{this.retrain_proj=i.data}),p.getDocStatus().then(i=>{this.doc_status=i.data})},updateExtractEntity(i){p.updateExtractEntity(i)},updateRetrainProj(i){p.updateRetrainProj(i)},StartProject(i){p.startProject(i).then(o=>{i.is_start=!0,this.$notify({type:"success",title:this.field_translation[i.proj_type],text:"\u0417\u0430\u043F\u0443\u0449\u0435\u043D",duration:5e3})})},StatusProject(i){p.statusProject(i).then(o=>{i.status=o.data.status})},StopProject(i){p.stopProject(i).then(o=>{i.is_start=!1,i.status=o.data.status})},StatusProjectsTimeout(){for(let[i,o]of Object.entries(this.running_proj))this.StatusProject(o)}},mounted(){this.getInitData(),setInterval(this.StatusProjectsTimeout,2e3)},computed:{running_proj(){return[this.extract_proj,this.retrain_proj].filter(o=>o.is_start===!0)}},watch:{"extract_proj.options":{handler(i,o){this.updateExtractEntity(i)},deep:!0},"retrain_proj.options":{handler(i,o){this.updateRetrainProj(i)},deep:!0}}},s=i=>(w("data-v-270f2030"),i=i(),P(),i),E={class:"panel"},C=s(()=>t("p",null,"\u0418\u0437\u0432\u043B\u0435\u0447\u0435\u043D\u0438\u0435 \u0438\u043C\u0435\u043D\u043D\u043E\u0432\u0430\u043D\u043D\u044B\u0445 \u0441\u0443\u0449\u043D\u043E\u0441\u0442\u0435\u0439",-1)),D=s(()=>t("svg",{xmlns:"http://www.w3.org/2000/svg",fill:"currentColor",class:"bi bi-chevron-down",viewBox:"0 0 16 16"},[t("path",{"fill-rule":"evenodd",d:"M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"})],-1)),L=[D],M={class:"panel-content"},T={class:"column"},I={class:"input-group"},R=s(()=>t("label",{for:"dest_folder"},"\u041F\u0430\u043F\u043A\u0430 \u0434\u043B\u044F \u043E\u0431\u0440\u0430\u0431\u043E\u0442\u043A\u0438",-1)),B=s(()=>t("p",null,"\u041E\u0431\u044F\u0437\u0430\u0442\u0435\u043B\u044C\u043D\u043E \u043D\u0430\u0447\u0438\u043D\u0430\u0435\u0442\u0441\u044F \u0441 /mnt/",-1)),H={class:"custom-input"},q=s(()=>t("span",{class:"input-border"},null,-1)),z=s(()=>t("div",{class:"input-error"},null,-1)),F={class:"input-group"},N=s(()=>t("label",{for:"doc_extension"},"\u0420\u0430\u0441\u0448\u0438\u0440\u0435\u043D\u0438\u0435 \u0434\u043E\u043A\u0443\u043C\u0435\u043D\u0442\u043E\u0432",-1)),G=s(()=>t("p",null,"\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u0440\u0430\u0441\u0448\u0438\u0440\u0435\u043D\u0438\u044F \u0434\u043E\u043A\u0443\u043C\u0435\u043D\u0442\u043E\u0432 \u0438\u0437 \u0441\u043F\u0438\u0441\u043A\u0430 \u0434\u043E\u0441\u0442\u0443\u043F\u043D\u044B\u0445",-1)),K=s(()=>t("div",{class:"input-error"},null,-1)),O={class:"input-group"},W=s(()=>t("label",{for:"extract_process_count"},"\u041A\u043E\u043B\u0438\u0447\u0435\u0441\u0442\u0432\u043E \u043F\u0440\u043E\u0446\u0435\u0441\u0441\u043E\u0432",-1)),Y=s(()=>t("p",null,"\u0423\u043A\u0430\u0436\u0438\u0442\u0435 \u0447\u0438\u0441\u043B\u043E \u043F\u0440\u043E\u0446\u0435\u0441\u0441\u043E\u0432 \u043A\u043E\u0442\u043E\u0440\u044B\u0435 \u0431\u0443\u0434\u0443\u0442 \u0438\u0441\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u044C\u0441\u044F \u043F\u0440\u0438 \u043E\u0431\u0440\u0430\u0431\u043E\u0442\u043A\u0435",-1)),A={class:"custom-input"},J=["disabled"],Q=s(()=>t("span",{class:"input-border"},null,-1)),X=s(()=>t("div",{class:"input-error"},null,-1)),Z={class:"column"},$={class:"input-group"},tt=s(()=>t("label",{for:"proj-alias"},"\u0418\u043C\u044F \u043E\u0431\u0440\u0430\u0431\u043E\u0442\u0447\u0438\u043A\u0430",-1)),ot=s(()=>t("p",null,"\u0418\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0435\u0442\u0441\u044F \u0434\u043B\u044F \u0441\u043E\u0437\u0434\u0430\u043D\u0438\u044F \u043B\u043E\u0433-\u0444\u0430\u0439\u043B\u0430",-1)),st={class:"custom-input"},et=s(()=>t("span",{class:"input-border"},null,-1)),nt=s(()=>t("div",{class:"input-error"},null,-1)),it={class:"input-group"},rt=s(()=>t("label",{for:"dest_pholder"},"\u0414\u0430\u0442\u0430 \u0434\u043E\u043A\u0443\u043C\u0435\u043D\u0442\u043E\u0432",-1)),lt=s(()=>t("p",null,"\u0418\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0439\u0442\u0435 \u0433\u0430\u043B\u043E\u0447\u043A\u0443, \u0447\u0442\u043E\u0431\u044B \u0441\u0447\u0438\u0442\u044B\u0432\u0430\u0442\u044C \u0434\u0430\u0442\u0443 \u0441\u043E\u0437\u0434\u0430\u043D\u0438\u044F \u0434\u043E\u043A\u0443\u043C\u0435\u043D\u0442\u043E\u0432",-1)),at={class:"custom-input-datetime"},pt={class:"checkbox-group-datetime"},dt=s(()=>t("span",{class:"input-border"},null,-1)),ct=s(()=>t("div",{class:"input-error"},null,-1)),_t={class:"column-fill"},ut={class:"additional-options"},ht=s(()=>t("div",{class:"additional-header"},"\u0414\u043E\u043F\u043E\u043B\u043D\u0438\u0442\u0435\u043B\u044C\u043D\u044B\u0435 \u043E\u043F\u0446\u0438\u0438",-1)),jt={class:"checkbox-group"},vt=s(()=>t("label",{for:"check-only-new"},"\u0414\u043E\u0431\u0430\u0432\u043B\u044F\u0442\u044C \u0442\u043E\u043B\u044C\u043A\u043E \u043D\u043E\u0432\u044B\u0435 \u0444\u0430\u0439\u043B\u044B",-1)),mt={class:"checkbox-group"},xt=s(()=>t("label",{for:"check-raw-data"},"\u0417\u0430\u043D\u043E\u0441\u0438\u0442\u044C \u0441\u0432\u0435\u0434\u0435\u043D\u0438\u044F \u0431\u0430\u0437\u0443 \u0434\u0430\u043D\u043D\u044B\u0445 \u0431\u0435\u0437 \u043E\u0431\u0440\u0430\u0431\u043E\u0442\u043A\u0438",-1)),bt={class:"program-control"},gt=["disabled"],ft=["disabled"],yt={class:"panel"},kt=s(()=>t("p",null,"\u041F\u0435\u0440\u0435\u043E\u0431\u0443\u0447\u0435\u043D\u0438\u0435 \u0432\u044B\u0431\u043E\u0440\u043A\u0438",-1)),Vt=s(()=>t("svg",{xmlns:"http://www.w3.org/2000/svg",fill:"currentColor",class:"bi bi-chevron-down",viewBox:"0 0 16 16"},[t("path",{"fill-rule":"evenodd",d:"M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"})],-1)),wt=[Vt],Pt={class:"panel-content"},St={class:"column"},Ut={class:"input-group"},Et=s(()=>t("label",{for:"doc_status"},"\u0421\u0442\u0430\u0442\u0443\u0441 \u0434\u043E\u043A\u0443\u043C\u0435\u043D\u0442\u043E\u0432",-1)),Ct=s(()=>t("p",null,"\u0412\u044B\u0431\u0440\u0430\u0442\u044C \u0432 \u0441\u043B\u0443\u0447\u0430\u0435 \u043D\u0435\u043E\u0431\u0445\u043E\u0434\u0438\u043C\u043E\u0441\u0442\u0438 \u0434\u043E\u043A\u0443\u043C\u0435\u043D\u0442\u044B \u043F\u043E \u0438\u0445 \u0441\u0442\u0430\u0442\u0443\u0441\u0443",-1)),Dt=s(()=>t("div",{class:"input-error"},null,-1)),Lt={class:"input-group"},Mt=s(()=>t("label",{for:"record_id"},"ID \u0434\u043E\u043A\u0443\u043C\u0435\u043D\u0442\u0430 \u0432 \u0411\u0414",-1)),Tt=s(()=>t("p",null,"\u0418\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0439\u0442\u0435 id \u0434\u043E\u043A\u0443\u043C\u0435\u043D\u0442\u0430 \u0447\u0442\u043E\u0431\u044B \u043F\u0440\u043E\u0434\u043E\u043B\u0436\u0438\u0442\u044C \u0432 \u0441\u043B\u0443\u0447\u0430\u0435 \u0441\u0431\u043E\u044F",-1)),It={class:"custom-input"},Rt=s(()=>t("span",{class:"input-border"},null,-1)),Bt=s(()=>t("div",{class:"input-error"},null,-1)),Ht={class:"input-group"},qt=s(()=>t("label",{for:"process_count"},"\u041A\u043E\u043B\u0438\u0447\u0435\u0441\u0442\u0432\u043E \u043F\u0440\u043E\u0446\u0435\u0441\u0441\u043E\u0432",-1)),zt=s(()=>t("p",null,"\u0423\u043A\u0430\u0436\u0438\u0442\u0435 \u0447\u0438\u0441\u043B\u043E \u043F\u0440\u043E\u0446\u0435\u0441\u0441\u043E\u0432 \u043A\u043E\u0442\u043E\u0440\u044B\u0435 \u0431\u0443\u0434\u0443\u0442 \u0438\u0441\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u044C\u0441\u044F \u043F\u0440\u0438 \u043E\u0431\u0440\u0430\u0431\u043E\u0442\u043A\u0435",-1)),Ft={class:"custom-input"},Nt=s(()=>t("span",{class:"input-border"},null,-1)),Gt=s(()=>t("div",{class:"input-error"},null,-1)),Kt={class:"column"},Ot={class:"input-group"},Wt=s(()=>t("label",{for:"alias-retrain"},"\u0418\u043C\u044F \u043E\u0431\u0440\u0430\u0431\u043E\u0442\u0447\u0438\u043A\u0430",-1)),Yt=s(()=>t("p",null,"\u0418\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0435\u0442\u0441\u044F \u0434\u043B\u044F \u0445\u0440\u0430\u043D\u0435\u043D\u0438\u044F \u043B\u043E\u0433 \u0444\u0430\u0439\u043B\u043E\u0432",-1)),At={class:"custom-input"},Jt=s(()=>t("span",{class:"input-border"},null,-1)),Qt=s(()=>t("div",{class:"input-error"},null,-1)),Xt={class:"input-group"},Zt=s(()=>t("label",{for:"doc-date"},"\u0414\u0430\u0442\u0430 \u0434\u043E\u043A\u0443\u043C\u0435\u043D\u0442\u043E\u0432",-1)),$t=s(()=>t("p",null,"\u0418\u0441\u043F\u043E\u043B\u044C\u0437\u0443\u0439\u0442\u0435 \u0433\u0430\u043B\u043E\u0447\u043A\u0443, \u0447\u0442\u043E\u0431\u044B \u0441\u0447\u0438\u0442\u044B\u0432\u0430\u0442\u044C \u0434\u0430\u0442\u0443 \u0441\u043E\u0437\u0434\u0430\u043D\u0438\u044F \u0434\u043E\u043A\u0443\u043C\u0435\u043D\u0442\u043E\u0432",-1)),to={class:"custom-input-datetime"},oo={class:"checkbox-group-datetime"},so=s(()=>t("span",{class:"input-border"},null,-1)),eo=s(()=>t("div",{class:"input-error"},null,-1)),no={class:"column-fill"},io={class:"additional-options"},ro=s(()=>t("div",{class:"additional-header"},"\u0414\u043E\u043F\u043E\u043B\u043D\u0438\u0442\u0435\u043B\u044C\u043D\u044B\u0435 \u043E\u043F\u0446\u0438\u0438",-1)),lo={class:"checkbox-group"},ao=s(()=>t("label",{for:"delete-old-files"},"\u0423\u0434\u0430\u043B\u044F\u0442\u044C \u043D\u0435 \u043D\u0430\u0439\u0434\u0435\u043D\u043D\u044B\u0435 \u0444\u0430\u0439\u043B\u044B",-1)),po={class:"program-control"},co=["disabled"],_o=["disabled"],uo=s(()=>t("div",{class:"wrapper"},null,-1));function ho(i,o,c,jo,e,r){const j=m("v-select"),v=m("DatepickerVue");return f(),y(V,null,[t("div",E,[t("div",{class:"panel-header",onClick:o[1]||(o[1]=u((...n)=>r.toggle_panel&&r.toggle_panel(...n),["prevent"]))},[C,t("button",{class:"panel-ico",onClick:o[0]||(o[0]=u((...n)=>r.toggle_panel&&r.toggle_panel(...n),["stop"]))},L)]),t("div",M,[t("div",T,[t("div",I,[R,B,t("div",H,[l(t("input",{type:"text",id:"dest_folder","onUpdate:modelValue":o[2]||(o[2]=n=>e.extract_proj.options.folder=n)},null,512),[[d,e.extract_proj.options.folder]]),q]),z]),t("div",F,[N,G,h(j,{multiple:"",label:"extension",options:e.doc_extensions,modelValue:e.extract_proj.options.doc_extension,"onUpdate:modelValue":o[3]||(o[3]=n=>e.extract_proj.options.doc_extension=n)},null,8,["options","modelValue"]),K]),t("div",O,[W,Y,t("div",A,[l(t("input",{type:"number",id:"extract_process_count","onUpdate:modelValue":o[4]||(o[4]=n=>e.extract_proj.options.process_count=n),disabled:e.extract_proj.options.raw_data},null,8,J),[[d,e.extract_proj.options.process_count]]),Q]),X])]),t("div",Z,[t("div",$,[tt,ot,t("div",st,[l(t("input",{type:"text",id:"proj-alias","onUpdate:modelValue":o[5]||(o[5]=n=>e.extract_proj.options.alias=n)},null,512),[[d,e.extract_proj.options.alias]]),et]),nt]),t("div",it,[rt,lt,t("div",at,[t("div",pt,[l(t("input",{class:"check-box-input",id:"check_processed",type:"checkbox","onUpdate:modelValue":o[6]||(o[6]=n=>e.extract_proj.options.read_creation_date=n)},null,512),[[_,e.extract_proj.options.read_creation_date]])]),h(v,{modelValue:e.extract_proj.options.creation_date,"onUpdate:modelValue":o[7]||(o[7]=n=>e.extract_proj.options.creation_date=n),format:"dd/MM/yyyy HH:mm",disabled:e.extract_proj.options.read_creation_date},null,8,["modelValue","disabled"]),dt]),ct])]),t("div",_t,[t("div",ut,[ht,t("div",jt,[l(t("input",{class:"check-box-input",id:"check-only-new",type:"checkbox","onUpdate:modelValue":o[8]||(o[8]=n=>e.extract_proj.options.only_new_files=n)},null,512),[[_,e.extract_proj.options.only_new_files]]),vt]),t("div",mt,[l(t("input",{class:"check-box-input",id:"check-raw-data",type:"checkbox","onUpdate:modelValue":o[9]||(o[9]=n=>e.extract_proj.options.raw_data=n)},null,512),[[_,e.extract_proj.options.raw_data]]),xt])]),t("div",bt,[t("button",{class:"play-btn",disabled:e.extract_proj.is_start,onClick:o[10]||(o[10]=n=>r.StartProject(e.extract_proj))},"\u0421\u0442\u0430\u0440\u0442 ",8,gt),t("button",{class:"stop-btn",disabled:!e.extract_proj.is_start,onClick:o[11]||(o[11]=n=>r.StopProject(e.extract_proj))},"\u0421\u0442\u043E\u043F",8,ft)]),t("div",{class:"wrapper",onClick:o[12]||(o[12]=n=>r.StatusProject(e.extract_proj))},[t("p",null,k(e.extract_proj.status),1)])])])]),t("div",yt,[t("div",{class:"panel-header",onClick:o[14]||(o[14]=u((...n)=>r.toggle_panel&&r.toggle_panel(...n),["prevent"]))},[kt,t("button",{class:"panel-ico",onClick:o[13]||(o[13]=u((...n)=>r.toggle_panel&&r.toggle_panel(...n),["stop"]))},wt)]),t("div",Pt,[t("div",St,[t("div",Ut,[Et,Ct,h(j,{multiple:"",label:"status_name",options:e.doc_status,modelValue:e.retrain_proj.options.status,"onUpdate:modelValue":o[15]||(o[15]=n=>e.retrain_proj.options.status=n)},null,8,["options","modelValue"]),Dt]),t("div",Lt,[Mt,Tt,t("div",It,[l(t("input",{type:"number",id:"record_id","onUpdate:modelValue":o[16]||(o[16]=n=>e.retrain_proj.options.record_id=n)},null,512),[[d,e.retrain_proj.options.record_id]]),Rt]),Bt]),t("div",Ht,[qt,zt,t("div",Ft,[l(t("input",{type:"number",id:"process_count","onUpdate:modelValue":o[17]||(o[17]=n=>e.retrain_proj.options.process_count=n)},null,512),[[d,e.retrain_proj.options.process_count]]),Nt]),Gt])]),t("div",Kt,[t("div",Ot,[Wt,Yt,t("div",At,[l(t("input",{type:"text",id:"alias-retrain","onUpdate:modelValue":o[18]||(o[18]=n=>e.retrain_proj.options.alias=n)},null,512),[[d,e.retrain_proj.options.alias]]),Jt]),Qt]),t("div",Xt,[Zt,$t,t("div",to,[t("div",oo,[l(t("input",{class:"check-box-input",id:"doc-date",type:"checkbox","onUpdate:modelValue":o[19]||(o[19]=n=>e.retrain_proj.options.read_creation_date=n)},null,512),[[_,e.retrain_proj.options.read_creation_date]])]),h(v,{modelValue:e.retrain_proj.options.creation_date,"onUpdate:modelValue":o[20]||(o[20]=n=>e.retrain_proj.options.creation_date=n),format:"dd/MM/yyyy HH:mm",disabled:e.retrain_proj.options.read_creation_date},null,8,["modelValue","disabled"]),so]),eo])]),t("div",no,[t("div",io,[ro,t("div",lo,[l(t("input",{class:"check-box-input",id:"delete-old-files",type:"checkbox","onUpdate:modelValue":o[21]||(o[21]=n=>e.retrain_proj.options.delete_old=n)},null,512),[[_,e.retrain_proj.options.delete_old]]),ao])]),t("div",po,[t("button",{class:"play-btn",disabled:e.retrain_proj.is_start},"\u0421\u0442\u0430\u0440\u0442 ",8,co),t("button",{class:"stop-btn",disabled:!e.retrain_proj.is_start},"\u0421\u0442\u043E\u043F",8,_o)]),uo])])])],64)}var go=g(U,[["render",ho],["__scopeId","data-v-270f2030"]]);export{go as default};
