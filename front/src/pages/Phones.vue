<template>
  <div id="search-block">
    <div class="q-pa-md">
      <q-input
        v-model="search_text"
        filled
        type="textarea" :rows="2"></q-input>
    </div>
    <div id="find-params">
      <div class="input-group">
        <div class="checkbox-group">
          <input type="checkbox" id="phones-search" v-model="search_phones_bool" :disabled="search_persons_bool">
          <label for="phones-search">Поиск абонентских номеров</label>
        </div>
        <div class="checkbox-group">
          <input type="checkbox" id="surnames-search" :disabled="search_phones_bool" v-model="search_persons_bool">
          <label for="surnames-search">Поиск установочных данных</label>
        </div>
      </div>
    </div>
    <div id="alert-messages">
      <p>{{ alert_messages }}</p>
    </div>
  </div>
  <div id="result-block">
    <div class="preloader-result">
    </div>
    <div class="result-preloader" v-if="show_preloader">
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
    </div>
    <div class="result-wait-block" v-if="!show_preloader && !Object.keys(result).length">
      <div v-if="this.get_previous_response" class="get-previous-data-block" @click.prevent="getDataFromLastQuestion">
        <p>Получить данные <br> предыдущего запроса</p>
      </div>
      <div v-else>
        <p>Начинайте вводить значение</p>
      </div>
    </div>
    <div class="result-table" v-if="Object.keys(result).length">
      <PhoneViewComponent v-for="(value, phone) in result" :phone="phone" :data="value"
                          @update:data="(page_id, phone_)=>{
                            value.preloader  = true;
                            value.current_page = page_id;
                            this.getPaginationPhone(page_id, phone_);
                          }" :key="phone"></PhoneViewComponent>
    </div>

  </div>

</template>

<script>
import PhoneViewComponent from '../components/PhoneViewComponent.vue';
import {mapActions, mapState} from 'pinia'
import {usePhoneStore} from '../stores/phones-store'
import PhonesService from "src/services/PhonesService";
import moment from "moment";

var handle_timeout;
var query_update = false;

export default {
  name: "PhonesPages",
  components: {
    PhoneViewComponent,
  },
  data() {
    return {
      search_phones_bool: true,
      search_persons_bool: false,
      alert_messages: '',
      search_text: '',
      search_timeout: null,
      result: [],
      request_id: null,
      show_preloader: 0,
    }
  },
  mounted() {
    this.initPage();
  },
  methods: {
    ...mapActions(usePhoneStore, ['set_request_id', 'set_pagination_phone', 'set_query_params', 'readParamsFromLocalStorage']),
    getPaginationPhone(page_id, phone) {
      PhonesService.sendPagination(page_id, phone).then(response => {
        this.result[phone] = response.data[phone];
        this.set_pagination_phone(phone, page_id);
      });
    },
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
    numbers_validation(number) {
      let valid_number = parseInt(number);
      let valid_str = String(valid_number);
      if (valid_str.length <= 8 || valid_str.length >= 13) {
        throw 'Validation Error'
      }
      return parseInt(number);
    },
    filtered_date(value) {
      if (value) {
        return moment(String(value)).format('DD/MM/YYYY hh:mm')
      }
    },
    async sendSearchText(search_string, search_phones) {
      let data = []
      let validation_data = []
      if (search_phones) {
        data = search_string.split('\n');
        for (const [index, item] of data.entries()) {
          try {
            validation_data.push(this.numbers_validation(item));
          } catch (e) {
            this.alert_messages = `В строке ${index + 1} выявлена ошибка`;
            return
          }
        }
      }
      if (validation_data.length) {
        this.show_preloader = true;
        await PhonesService.sendSearchString(search_string, validation_data).then(response => {
          this.result = response.data.phones;
          this.set_request_id(response.data.response_id);
        });
        this.show_preloader = false;
      }
    },
    async initPage() {
      if (Object.keys(this.$route.query).length > 0) {
        this.set_query_params({...this.$route.query});
      }
      if (Object.keys(this.query_params).length !== 0) {
        this.show_preloader = true;
        await PhonesService.sendPreviousRequest(this.query_params).then(response => {
          query_update = true;
          this.search_text = response.data['search_string'];
          this.result = response.data.phones;
          this.$router.push({query: this.query_params});
        }).catch(error => {
          this.show_preloader = false;
        }).finally(() => this.show_preloader = false);
      }
    },
    async getDataFromLastQuestion() {
      this.readParamsFromLocalStorage();
      await this.initPage();
    },
  },
  computed: {
    ...mapState(usePhoneStore, ['query_params', 'get_previous_response']),
  },
  watch: {
    search_text(NewSearchText, OldSearchText) {
      if (!query_update) {
        clearTimeout(handle_timeout);
        handle_timeout = setTimeout(() => this.sendSearchText(NewSearchText, this.search_phones_bool), 2000);
      } else {
        query_update = false;
      }
    }
  }
}
</script>

<style scoped>


.get-previous-data-block > p {
  text-align: center;
  cursor: pointer;
  animation: pulse 2s infinite;
}

.get-previous-data-block > p:hover {
  animation: none;
  transform: scale(1);
}

.pagination {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}


#alert-messages {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  flex-grow: 1;
}

#alert-messages > p {
  width: 100%;
  color: red;
}

#search-block {
  display: flex;
}

.checkbox-group > input {
  width: 30px;
  margin: 0 5px;
}

.page-content > div:last-child {
  flex-grow: 1;
}

.q-pa-md {
  min-width: 500px;

  resize: vertical;
}

/*
.result-table ul {
  width: 100%;
  list-style-type: none;
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 5px 15px;
}

.result-table ul li {
  display: flex;
  width: 100%;
  padding: 10px 0;
}

.result-table ul li:first-child {
  border-bottom: 1px solid black;
}

.result-table ul li:not(:first-child):hover {
  background-color: #ececed;
  cursor: pointer;
}

.result-table ul li p:first-child {
  flex: 1%;
  text-align: center;
}

.result-table ul li p:not(:first-child) {
  display: block;
  padding: 0 10px;
  flex: 10%
}

.result-table ul li p:last-child {
  flex: 55%
}
*/
#result-block {
}

.result-wait-block {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;

}

.result-preloader {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.osa-menu-icons {
  width: 133px;
  height: 135px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.8);
  }

  70% {
    transform: scale(1);
  }

  100% {
    transform: scale(0.8);
  }
}


</style>
