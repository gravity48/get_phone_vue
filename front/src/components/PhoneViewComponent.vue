<template>
  <div class="panel">
    <div class="panel-header" @click.prevent="toggle_panel">
      <p>{{ phone }}</p>
      <button class="panel-ico" @click.stop="toggle_panel">
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-chevron-down" viewBox="0 0 16 16">
          <path fill-rule="evenodd"
                d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
        </svg>
      </button>
    </div>
    <div class="panel-content">
      <ul>
        <li><p>#</p>
          <p>Результат</p>
          <p class="p-filepath">Документ</p>
          <p>Дата</p>
          <p>Параграф</p></li>
        <li class="preloader-page" v-if="data.preloader">
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p class="p-filepath">
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
        </li>
        <li class="preloader-page" v-if="data.preloader">
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p class="p-filepath">
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
        </li>
        <li class="preloader-page" v-if="data.preloader">
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p class="p-filepath">
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
        </li>
        <li class="preloader-page" v-if="data.preloader">
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p class="p-filepath">
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
        </li>
        <li class="preloader-page" v-if="data.preloader">
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p class="p-filepath">
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
          <p>
            <q-skeleton :type="rect"/>
          </p>
        </li>
        <li v-for="(item, index) in data.data" :key="index" class="li-result" v-else>
          <p>{{ index + 1 }}</p>
          <p>{{ item.number }}</p>
          <p class="p-filepath"><a :href="item.filepath"> {{ item.filename }}</a></p>
          <p>{{ filtered_date(item.doc_date) }}</p>
          <p><span v-for="(paragraph, p_index) in item.paragraph" :key="p_index">
            <span class="p-before">{{ paragraph.p_before }}</span><span
            class="p-target">{{ paragraph.target }}</span><span class="p-after">{{ paragraph.p_after }}</span> ...
          </span></p>
        </li>
      </ul>
      <div class="pagination">
        <q-pagination
          :model-value="data.current_page"
          :max="data.max_page"
          :max-pages="6"
          direction-links
          flat
          color="grey"
          active-color="primary"
          @update:model-value="(new_value) => {
                this.$emit('update:data', new_value, this.phone);
                //this.getPaginationPhone(new_value,phone);
              }"
        />
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "PhoneViewComponent",
  props: {
    phone: Number,
    data: Object,
  },
  emits: ['update:data'],
  data() {
    return {}
  },
  methods: {
    filtered_date(value) {
      if (value) {
        return moment(String(value)).format('DD/MM/YYYY')
      }
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
  }
}
</script>

<style scoped>

.p-target {
  font-style: italic;
  font-weight: bold;
}


.pagination {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}


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
  flex: 10%;
}

.result-table ul li .p-filepath{
  flex: 25% !important;
  word-break: break-word;
}

.result-table ul li p:last-child {
  flex: 55%;
  word-break: break-word;
}

</style>
