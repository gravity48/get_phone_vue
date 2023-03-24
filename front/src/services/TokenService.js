import axios from "axios";
import {useAuthStore} from "stores/auth-store";
import {createPinia} from "pinia";

let URL = '/api/'

class TokenService {
  sendAuth(data) {
    return axios.post(URL + 'token/', data).then(response => {
      let data = {
        'token': response.data.access,
        'refresh': response.data.refresh,
        'is_staff': response.data.is_staff,
      }
      localStorage.setItem("tokens", JSON.stringify(data));
      const user = useAuthStore();
      user.set_user(data['is_staff']);
      return response;
    });
  }

  getLocalAccessToken() {
    let user = JSON.parse(localStorage.getItem("tokens"));
    return user?.token;
  }

  getLocalRefreshToken() {
    let user = JSON.parse(localStorage.getItem("tokens"));
    return user?.refresh;
  }

  updateLocalAccessToken(token) {
    let user = JSON.parse(localStorage.getItem("tokens"));
    user.token = token;
    localStorage.setItem("tokens", JSON.stringify(user));
  }

  removeUser() {
    localStorage.removeItem("tokens");
  }
}

export default new TokenService();
