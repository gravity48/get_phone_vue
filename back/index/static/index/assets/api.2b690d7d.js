import{a as n}from"./index.2cf0d985.js";import{T as t,u as a}from"./TokenService.69fb936b.js";const s=n.create({baseURL:"/api/",headers:{"Content-Type":"application/json"}});s.interceptors.request.use(e=>{const r=t.getLocalAccessToken();return r&&(e.headers.Authorization="Bearer "+r),e},e=>Promise.reject(e));s.interceptors.response.use(e=>e,async e=>{const r=e.config;return r.url!=="token/"&&e.response&&e.response.status===401&&!r._retry?(r._retry=!0,await n.post("/api/token/refresh/",{refresh:t.getLocalRefreshToken()}).then(o=>{t.updateLocalAccessToken(o.data.access)}).catch(o=>{t.removeUser(),a().redirect_to_login()}),s(r)):Promise.reject(e)});export{s as i};
