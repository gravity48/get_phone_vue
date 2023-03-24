import axios from "axios";
import TokenService from "src/services/TokenService";
import {useAuthStore} from "stores/auth-store";

const instance = axios.create({
  baseURL: "/api/",
  headers: {
    "Content-Type": "application/json",
  },
});

instance.interceptors.request.use(
  (config) => {
    const token = TokenService.getLocalAccessToken();
    if (token) {
      config.headers["Authorization"] = 'Bearer ' + token;  // for Spring Boot back-end
      //config.headers["x-access-token"] = token; // for Node.js Express back-end
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
instance.interceptors.response.use(
  (res) => {
    return res;
  },
  async (err) => {
    const originalConfig = err.config;
    if (originalConfig.url !== "token/" && err.response) {
      // Access Token was expired
      if (err.response.status === 401 && !originalConfig._retry) {
        originalConfig._retry = true;
        await axios.post("/api/token/refresh/", {
          refresh: TokenService.getLocalRefreshToken(),
        }).then(response => {
          TokenService.updateLocalAccessToken(response.data.access);
        }).catch(error => {
          TokenService.removeUser();
          const user = useAuthStore();
          user.redirect_to_login();
        });
        return instance(originalConfig);
      }
    }
    return Promise.reject(err);
  }
);
export default instance
