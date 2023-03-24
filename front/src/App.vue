<template>
  <notifications position="bottom right" />
  <router-view />
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<style>
#q-app{
  height: 100%;
  min-height: 100%;

}

html, body{
  height: 100%;
  min-height: 100%;
}

.vue-notification-wrapper{
  height: 100px;
  font-size: 14px;
  margin: 0 0 2px 0 !important;
}

.vue-notification-template{
  height: 100%;
}

.notification-title{
  padding: 5px 0;
}


</style>
