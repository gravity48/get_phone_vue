import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    is_staff: 0,
    login: false,
  }),
  actions: {
    set_user(is_staff) {
      this.is_staff = is_staff;
      this.login = true;
    },
    redirect_to_login(){
      this.router.push({name: 'Login'});
    }
  },
});
