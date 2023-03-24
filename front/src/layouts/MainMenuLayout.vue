<template>
    <nav>
      <ul>
        <li>
          <div class="osa-menu-icons">
            <svg viewBox="0 0 133 145" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
              <!-- Created with SVG-edit - https://github.com/SVG-Edit/svgedit-->
              <g class="layer">
                <title>Layer 1</title>
                <ellipse cx="174" cy="18" fill="none" id="svg_1" rx="42.5" ry="43.5" stroke="#000000" stroke-width="5"
                         transform="rotate(176.829 120 57.166)"/>
                <ellipse cx="69.5" cy="40.5" fill="none" id="svg_3" rx="15" ry="15" stroke="#000000" stroke-width="5"/>
                <line fill="none" id="svg_5" stroke="#000000" stroke-dasharray="null" stroke-linecap="null"
                      stroke-linejoin="null" stroke-width="5" x1="28.5" x2="106.16595" y1="83.5" y2="83.5"/>
                <line fill="none" id="svg_7" stroke="#000000" stroke-dasharray="null" stroke-linecap="null"
                      stroke-linejoin="null" stroke-width="5" x1="25.5" x2="108.71658" y1="104.5" y2="104.5"/>
                <line fill="none" id="svg_8" stroke="#000000" stroke-dasharray="null" stroke-linecap="null"
                      stroke-linejoin="null" stroke-width="5" x1="32.5" x2="101.52898" y1="125.5" y2="125.5"/>
                <line fill="none" id="svg_10" stroke="#000000" stroke-dasharray="null" stroke-linecap="null"
                      stroke-linejoin="null" stroke-width="5" x1="79.5" x2="98.53943" y1="25.5" y2="6.46057"/>
                <line fill="none" id="svg_13" stroke="#000000" stroke-dasharray="null" stroke-linecap="null"
                      stroke-linejoin="null" stroke-width="5" transform="rotate(-88.3397 51 16.5)" x1="41.48029"
                      x2="60.51972" y1="26.01972" y2="6.98029"/>
                <line fill="none" id="svg_14" stroke="#000000" stroke-dasharray="null" stroke-linecap="null"
                      stroke-linejoin="null" stroke-width="5" x1="105.48029" x2="122.51972" y1="85.01972"
                      y2="70.98029"/>
                <line fill="none" id="svg_15" stroke="#000000" stroke-dasharray="null" stroke-linecap="null"
                      stroke-linejoin="null" stroke-width="5" transform="rotate(39.2072 120.333 104.5)" x1="111.81362"
                      x2="128.85305" y1="111.51972" y2="97.48029"/>
                <line fill="none" id="svg_16" stroke="#000000" stroke-dasharray="null" stroke-linecap="null"
                      stroke-linejoin="null" stroke-width="5" transform="rotate(80.4069 111.333 134.5)" x1="102.81362"
                      x2="119.85305" y1="141.51972" y2="127.48029"/>
                <line fill="none" id="svg_17" stroke="#000000" stroke-dasharray="null" stroke-linecap="null"
                      stroke-linejoin="null" stroke-width="5" transform="rotate(71.8473 19.3333 77.5)" x1="10.81362"
                      x2="27.85305" y1="84.51972" y2="70.48029"/>
                <line fill="none" id="svg_18" stroke="#000000" stroke-dasharray="null" stroke-linecap="null"
                      stroke-linejoin="null" stroke-width="5" transform="rotate(39.2072 13.333 104.5)" x1="4.81369"
                      x2="21.85312" y1="111.5195" y2="97.48007"/>
                <line fill="none" id="svg_20" stroke="#000000" stroke-dasharray="null" stroke-linecap="null"
                      stroke-linejoin="null" stroke-width="5" transform="rotate(167.561 28.5 134.5)" x1="19.98055"
                      x2="37.01999" y1="141.5194" y2="127.47997"/>
                <ellipse cx="40.5" cy="5" fill="none" id="svg_21" rx="1.5" ry="1.5" stroke="#000000" stroke-width="5"/>
                <ellipse cx="99" cy="5.5" fill="none" id="svg_22" rx="1.5" ry="1.5" stroke="#000000" stroke-width="5"/>
              </g>
            </svg>
          </div>
        </li>
        <li class="router-li">
          <router-link :to="{name: 'Description'}"><span id="logotype-name">OSA</span>
            <span id="logotype-proj-name">extra</span></router-link>
        </li>
        <li class="router-li">
          <router-link id='logotype-main' :to="{name: 'Phones'}">Поиск</router-link>
        </li>
        <li class="router-li">
          <router-link id='logotype-main' :to="{name: 'Training'}"> Обучение</router-link>
        </li>
        <li class="router-li">
          <router-link id='logotype-main' :to="{name: 'Settings'}"> Настройки</router-link>
        </li>
        <li id="filler"></li>
        <li class="router-li"><a href="#" @click=logout>Выйти</a></li>
        <li class="mobile-menu-btn">
          <button @click="mobile_menu_show = !mobile_menu_show">
            <q-icon
              name="fa-solid fa-bars"
            />
          </button>
        </li>
      </ul>
    </nav>
    <transition appear
                enter-active-class="animated fadeIn"
                leave-active-class="animated fadeOut">
      <div id="mobile-menu" v-show="mobile_menu_show">
        <ul>
          <li class="router-li">
            <router-link id='logotype-main' :to="{name: 'Phones'}">Поиск номеров</router-link>
          </li>
          <li class="router-li"><a href="#">Выйти</a></li>
        </ul>
      </div>
    </transition>
    <div class="page-content">
        <router-view></router-view>
    </div>

</template>

<script>
import TokenService from "src/services/TokenService";

export default {
  name: "MainMenuLayout",
  data() {
    return {
      mobile_menu_show: false,
    }
  },
  methods: {
    logout(){
      TokenService.removeUser();
      this.$router.push({name: 'Login'});
    }

  }
}
</script>

<style scoped>

.page-content {
  display: flex;
  flex-direction: column;
  height: calc(100% - 70px);
  min-height: calc(100% - 70px);
}


nav {
  position: sticky;
  top: 0;
}

nav ul li > p, li a {
  display: block;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

li a {
  color: black;
  text-align: center;
  text-decoration: none;
}

nav ul {
  display: flex;
  list-style-type: none;
  margin: 0;
  padding: 0;
  background-color: #eee;

}

nav ul li {
  display: flex;
  height: 70px;
  width: 100px;
  align-items: center;
  justify-content: center;
}


#filler {
  display: block;
  flex-grow: 1;
}

nav ul li:first-child {
  width: 50px;
}

nav ul li:first-child svg, nav ul li:first-child div {
  width: 100%;
  height: 100%;
}

.router-li:hover {
  background-color: #4CAF50; /* Add a green color to the "active/current" link */
  color: white;
}

#mobile-menu {
  position: absolute;
  top: 50px;
  background-color: #eee;
  width: 100%;
}

#mobile-menu ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

nav ul li:last-child {
  display: none;
}

nav ul li button {
  border: none;
  background-color: transparent;
}

#logotype-main {
  text-align: center;
  padding: 15px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

#logotype-name {
  display: block;
  font-size: 32px;
  line-height: 31px;
}

#logotype-proj-name {
  display: block;
  font-size: 10px;
  line-height: 10px;
  margin-top: -2px;
  letter-spacing: 3px;
}


@media screen and (max-width: 500px) {
  nav ul li:not(:first-child) {
    display: none;
  }

  nav ul li:last-child {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .mobile-menu-btn {

  }
}


</style>
