import { boot} from 'quasar/wrappers'

import {h} from 'vue';


import Notification from '@kyvg/vue3-notification';

import Datepicker from '@vuepic/vue-datepicker';
import './datepicker.css'

import vSelect from "vue-select";
import 'vue-select/dist/vue-select.css';

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.component('DatepickerVue', Datepicker);
  app.component('v-select', vSelect);
  app.use(Notification);

  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

