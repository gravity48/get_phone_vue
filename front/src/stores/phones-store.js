import { defineStore } from 'pinia';

export const usePhoneStore = defineStore('phone', {
  state: () => ({
    request_id: null,
    query_params: {},
  }),
  actions: {
    set_request_id(request_id){
      this.request_id = request_id;
      this.query_params = {}
      this.query_params['request_id'] = request_id;
      this.router.push({query: this.query_params});
      this.saveParamsInLocalStorage();
    },
    set_pagination_phone(phone, page_id){
      if (this.query_params.request_id){
        this.query_params[phone] = page_id
        this.router.push({query: this.query_params});
        this.saveParamsInLocalStorage();
      }
    },
    set_query_params(query_params){
      for (const [key, value] of Object.entries(query_params)) {
        this.query_params[key] = parseInt(value);
      }
      this.request_id = query_params.request_id;
    },
    readParamsFromLocalStorage(){
      let search = JSON.parse(localStorage.getItem("search"));
      this.request_id = parseInt(search['request_id']);
      for (const [key, value] of Object.entries(search['query_params'])){
        this.query_params[key] = parseInt(value);
      }
    },
    saveParamsInLocalStorage(){
      if (localStorage.getItem("search")) {
        localStorage.removeItem("search");
      }
      let data = {
        'request_id': this.request_id,
        'query_params': this.query_params,
        'action': 'search_phone',
      }
      localStorage.setItem("search", JSON.stringify(data));
    },
  },
  getters:{
    get_previous_response:() => {
      return localStorage.getItem("search");
    }
  }
});
