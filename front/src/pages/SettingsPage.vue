<template>
  <div class="panel">
    <div class="panel-header" @click.prevent="toggle_panel">
      <p>Подключение к базе данных</p>
      <button class="panel-ico" @click.stop="toggle_panel">
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-chevron-down" viewBox="0 0 16 16">
          <path fill-rule="evenodd"
                d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
        </svg>
      </button>
    </div>
    <div class="panel-content">
      <div class="column">
        <div class="input-group">
          <label for="db_ip">Сервер базы данных</label>
          <p>Указывается в формате IP:port</p>
          <div class="custom-input">
            <input type="text" id="db_ip" v-model="db_settings.db_ip">
            <span class="input-border"> </span>
          </div>
          <div class="input-error"></div>
        </div>
        <div class="input-group">
          <label for="db_login">Логин</label>
          <p>Пользователь базы данных</p>
          <div class="custom-input">
            <input type="text" id="db_login" v-model="db_settings.db_login">
            <span class="input-border"> </span>
          </div>
          <div class="input-error"></div>
        </div>
      </div>
      <div class="column">
        <div class="input-group">
          <label for="db_path">Путь к базе данных</label>
          <p>Укажите полный путь к БД на удаленном севере </p>
          <div class="custom-input">
            <input type="text" id="db_path" v-model="db_settings.db_path">
            <span class="input-border"> </span>
          </div>
          <div class="input-error"></div>
        </div>
        <div class="input-group">
          <label for="db_password">Пароль</label>
          <p>Пароль пользователя БД на удаленном севере</p>
          <div class="custom-input">
            <input type="password" id="db_password" v-model="db_settings.db_password">
            <span class="input-border"></span>
          </div>
          <div class="input-error"></div>
        </div>
      </div>
      <div class="column-fill">
        <button type="button" @click="updateDataBaseSettings">Обновить</button>
      </div>
    </div>
  </div>
  <div class="panel">
    <div class="panel-header" @click.prevent="toggle_panel">
      <p>Пользователи</p>
      <button class="panel-ico" @click.stop="toggle_panel">
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-chevron-down" viewBox="0 0 16 16">
          <path fill-rule="evenodd"
                d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
        </svg>
      </button>
    </div>
    <div class="panel-content">
      <ul id="userspace-control">
        <li><p>#</p>
          <p>Имя пользователя</p>
          <p>Email</p>
          <p>Административные полномочия</p>
          <p>Дата создания</p>
          <p @click.prevent="modal_show = !modal_show">
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-person-add" viewBox="0 0 16 16">
              <path
                d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Zm.5-5v1h1a.5.5 0 0 1 0 1h-1v1a.5.5 0 0 1-1 0v-1h-1a.5.5 0 0 1 0-1h1v-1a.5.5 0 0 1 1 0Zm-2-6a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"/>
              <path
                d="M8.256 14a4.474 4.474 0 0 1-.229-1.004H3c.001-.246.154-.986.832-1.664C4.484 10.68 5.711 10 8 10c.26 0 .507.009.74.025.226-.341.496-.65.804-.918C9.077 9.038 8.564 9 8 9c-5 0-6 3-6 4s1 1 1 1h5.256Z"/>
            </svg>
          </p>
        </li>
        <li v-for="(user, index) in users_list" :key="user.id"><p>{{ index + 1 }}</p>
          <p>{{ user.username }}</p>
          <p>{{ user.email }}</p>
          <p>{{ user.is_staff }}</p>
          <p>{{ filtered_date(user.date_joined) }}</p>
          <p @click="deleteUser(index, user.id)">
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-person-x"
                 viewBox="0 0 16 16">
              <path
                d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm.256 7a4.474 4.474 0 0 1-.229-1.004H3c.001-.246.154-.986.832-1.664C4.484 10.68 5.711 10 8 10c.26 0 .507.009.74.025.226-.341.496-.65.804-.918C9.077 9.038 8.564 9 8 9c-5 0-6 3-6 4s1 1 1 1h5.256Z"/>
              <path
                d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Zm-.646-4.854.646.647.646-.647a.5.5 0 0 1 .708.708l-.647.646.647.646a.5.5 0 0 1-.708.708l-.646-.647-.646.647a.5.5 0 0 1-.708-.708l.647-.646-.647-.646a.5.5 0 0 1 .708-.708Z"/>
            </svg>
          </p>
        </li>
      </ul>
    </div>
  </div>
  <transition
    appear
    enter-active-class="animated fadeIn"
    leave-active-class="animated fadeOut"
  >
    <div id="modal-window" v-show="modal_show">
      <button class="modal-close-btn" @click="modal_show = !modal_show">
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
          <path
            d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
        </svg>
      </button>
      <div class="add_user">
        <div class="column">
          <div class="input-group">
            <label for="dest_pholder">Имя пользователя</label>
            <p>Введите username пользователя</p>
            <div class="custom-input">
              <input type="text" id="username" v-model="user_.username">
              <span class="input-border"> </span>
            </div>
            <div class="input-error"></div>
          </div>
          <div class="input-group">
            <label for="dest_pholder">Пароль</label>
            <p>Введите пароль пользователя</p>
            <div class="custom-input">
              <input type="password" id="password" v-model="user_.password">
              <span class="input-border"> </span>
            </div>
            <div class="input-error"></div>
          </div>
        </div>
        <div class="column">
          <div class="input-group">
            <label for="dest_pholder">Почта</label>
            <p>Введите почтовый ящик пользователя</p>
            <div class="custom-input">
              <input type="text" id="email" v-model="user_.email">
              <span class="input-border"> </span>
            </div>
            <div class="input-error"></div>
          </div>
          <div class="additional-options">
            <div class="additional-header">Дополнительные опции</div>
            <div class="checkbox-group">
              <input class="check-box-input" id="check_is_staff" type="checkbox" v-model="user_.is_staff">
              <label for="check_is_staff">Администратор</label>
            </div>
          </div>
        </div>
        <div class="column-fill">
          <button type="button" @click="createUser">Добавить</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import {notify} from "@kyvg/vue3-notification";
import moment from 'moment'
import UsersService from "src/services/UsersService";
import DataBaseService from 'src/services/DataBaseService'

export default {
  name: "SettingsPage",
  data() {
    return {
      users_list: [],
      modal_show: false,
      user_: {},
      db_settings: {},
      field_translation: {
        'db_path': 'Путь к базе данных',
        'all': 'Соединение к базе данных',
      }
    }
  },
  mounted() {
    this.getUsers();
    this.getDataBaseSettings();
  },
  methods: {
    toggle_panel(event) {
      let button_ico = event.target.closest('.panel').querySelector('.panel-ico');
      let panel_content = event.target.closest('.panel').querySelector('.panel-content');
      if (button_ico.classList.contains("rotate-180")) {
        button_ico.classList.remove("rotate-180");
        panel_content.classList.add("hide");
        setTimeout(() => {
          panel_content.classList.remove("visible");
        }, 100);

      } else {
        panel_content.classList.remove("hide");
        button_ico.classList.add("rotate-180");
        panel_content.classList.add("visible");
      }
    },
    getDataBaseSettings() {
      DataBaseService.getDatabaseData().then(response => {
        this.db_settings = response.data;
      }).catch(error => {
          console.log(error);
        }
      )
    },
    updateDataBaseSettings() {
      DataBaseService.updateDataBase(this.db_settings).then(response => {
        this.$notify({
          type: 'success',
          title: 'Подключение к базе данных',
          text: 'Сведения о базе данных успешно обновлены',
          duration: 5000,
        });
      }).catch(errors => {
        console.log(errors);
        for (const [key, value] of Object.entries(errors.response.data)) {
          notify({
            type: 'error',
            title: this.field_translation[key],
            text: value,
            duration: 5000
          });
        }
      })
    },
    getUsers() {
      UsersService.getAllUsers().then(response => {
        this.users_list = response.data;
      }).catch(errors => {
        console.log(errors);
      })
    },
    createUser() {
      UsersService.createUser(this.user_).then(response => {
        this.users_list.push(response.data);
        this.modal_show = false;
      }).catch(error => {

      })
    },
    deleteUser(index, user_id) {
      UsersService.deleteUser(user_id).then(response => {
        this.getUsers();
      });
    },
    filtered_date(value) {
      if (value) {
        return moment(String(value)).format('DD/MM/YYYY hh:mm')
      }
    },
  },
}
</script>

<style scoped>
.modal-close-btn {
  position: absolute;
  top: 10px;
  left: calc(100% - 35px);
  width: 35px;
  height: 35px;
  background-color: transparent;
  border: none;
}

.modal-close-btn > svg {
  width: 100%;
  height: 100%;
  color: red;
}

.modal-close-btn:hover {
  cursor: pointer;

}


.additional-options {
  margin: 10px 0;
}


#modal-window .add_user {
  display: flex;
  flex-wrap: wrap;
}

.column-fill {
  flex: 100%;
  padding: 10px 10px;
}

.column-fill > button {
  height: 30px;
  width: 100px;
}

#modal-window .add_user .column {
  flex: 50%;
  padding: 10px 10px;
}

#modal-window {
  width: 100%;
  height: calc(100% - 70px);
  background-color: white;
  position: absolute;
  padding: 10px 0;
  top: 70px;
  left: 0;
}


#userspace-control li:not(:first-child) p:last-child > svg {
  opacity: 0;
}

#userspace-control li p:last-child > svg {
  cursor: pointer;
}

#userspace-control li:not(:first-child):hover svg {
  opacity: 1 !important;
  transition: opacity ease-out 0.3s;
}

#userspace-control {
  list-style-type: none;
  width: 100%;
  padding: 0;
}

#userspace-control li {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 5px;
}

#userspace-control li:first-child {
  border-bottom: 1px solid black;
}

#userspace-control li p:first-child {
  flex: 5%;
}

#userspace-control li p:last-child {
  flex: 5%;
  display: flex;
  align-items: center;
  justify-content: center;
}

#userspace-control li p:last-child > svg {
  height: 30px;
}


#userspace-control li p {
  flex: 22.5%;
  text-align: center;
  min-height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>
