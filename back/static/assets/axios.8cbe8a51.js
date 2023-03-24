import {R as i} from "./index.d72547a9.js";
import {a} from "./index.2cf0d985.js";

const e = a.create({baseURL: "https://api.example.com"});
var t = i(({app: o}) => {
    o.config.globalProperties.$axios = a, o.config.globalProperties.$api = e
});
export {e as api, t as default};
