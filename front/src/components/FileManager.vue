<template>
  <div class="popup-overlay" id="folder-pickup" @click.stop="closePopup">
    <div class="popup-content" @click.stop="">
      <div>
        <div class="popup-content--header">
          <p>Выберите папку</p>
          <button type="button" class="close-button" title="Закрыть" @click="closePopup"></button>
        </div>
        <div class="folder-tree">
          <div class="loader hidden">
            <div></div>
          </div>
          <div class="folder-tree--panel">
            <ul>
              <recursive-component v-for="(item, index) in this.root_dirs" :item="item" :key="index"
                                   @update:select-value="(value) => recursiveEmit(value)"></recursive-component>
            </ul>
          </div>
        </div>
        <div class="popup-content--buttons">

          <button type="button" @click="updateModelValue">OK</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DirectoriesService from "src/services/DirectoriesService";
import recursiveComponent from "components/recursiveComponent.vue";

export default {
  name: "FileManager",
  emits: ['close:popup', 'update:value'],
  components: {
    recursiveComponent,
  },
  data() {
    return {
      root_dirs: [],
      selected_item: {},
    }
  },
  mounted() {
    this.getRootDir();
  },
  methods: {
    closePopup() {
      this.$emit('close:popup');
    },
    getRootDir() {
      DirectoriesService.getRootDirectory().then((response) => {
        this.root_dirs = response.data;
      })
    },
    recursiveEmit(value) {
      this.selected_item.selected = false;
      this.selected_item = value;
      this.selected_item.selected = true;
    },
    updateModelValue(){
      if (this.selected_item.path) {
        this.$emit('update:value', this.selected_item.path);
        this.closePopup();
      }
    }
  },
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

body > div {
  align-items: center;
  display: flex;
  flex-direction: row;
  height: 100%;
  justify-content: center;
}

p {
  margin: 0;
}

ul {
  padding-left: 0;
  list-style-type: none;
  margin: 0;
}

.popup-content--buttons > button {
  background-color: rgba(76, 175, 80, 1);
  border: 2px solid rgb(72, 169, 75);
  border-radius: 6px;
  color: white;
  cursor: pointer;
  display: block;
  outline: none;
  padding: 15px 25px;
  transition: background .2s, box-shadow .2s;
}

.popup-content--buttons > button:hover {
  background-color: rgba(76, 175, 80, 1);
}

.popup-content--buttons > button.pressed {
  box-shadow: -2px 2px 6px inset rgb(72, 169, 75, .6);
}

.close-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  height: 35px;
  outline: none;
  padding: 0;
  position: relative;
  width: 35px;
}

.close-button:before, .close-button:after {
  background-color: rgba(76, 175, 80, 1);
  content: '';
  display: block;
  height: 2px;
  left: 0;
  position: absolute;
  top: calc(50% - 1px);
  transform: rotate(45deg);
  transition: background .2s;
  width: 100%;
}

.close-button:after {
  transform: rotate(-45deg);
}

.close-button:hover:before, .close-button:hover:after {
  background-color: red;
}

.popup-overlay {
  align-items: center;
  background-color: rgba(31, 31, 31, 0.9);
  display: flex;
  height: 100%;
  justify-content: stretch;
  left: 0;
  position: fixed;
  top: 0;
  transition: opacity .2s;
  width: 100%;
  z-index: 10000;
}

.popup-overlay.hidden {
  opacity: 0;
  pointer-events: none;
}

.popup-content--header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px;
  margin-bottom: 10px;
  background: linear-gradient(90deg, rgba(76, 175, 80, 1) 0%, rgba(76, 175, 80, .7) 50%, rgba(76, 175, 80, 0) 85%);
}

.popup-content--header > p {
  font-size: 1.2em;
  color: white;
  font-weight: 900;
}

.popup-overlay > .popup-content {
  background-color: #FFFFFF;
  border-radius: 5px;
  box-shadow: 0 0 25px rgba(0, 0, 0, 0.4);
  height: 90%;
  margin: 0 auto;
  max-height: 800px;
  max-width: 600px;
  position: relative;
  width: 98%;
  overflow: hidden;
}

.popup-content > div {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.popup-content > div > * {
  flex-grow: 0;
  padding-left: 10px;
  padding-right: 10px;
}

.popup-content > div > *:first-child {
  padding-top: 10px;
}

.popup-content > div > *:last-child {
  padding-bottom: 10px;
}

.popup-content > div > .folder-tree {
  flex-grow: 2;
  position: relative;
  overflow: auto;
  margin-bottom: 10px;
}

.folder-tree > .loader {
  background-color: rgba(76, 175, 80, 0.9);
  height: 100%;
  left: 0;
  position: absolute;
  top: 0;
  transition: opacity .2s;
  width: 100%;
  z-index: 1;
}

.folder-tree > .loader.hidden {
  opacity: 0;
  pointer-events: none;
}

.loader > div {
  animation: loading .5s linear infinite;
  border: 2px solid rgba(76, 175, 80, 1);
  border-radius: 50%;
  border-top: none;
  height: 50px;
  margin: 0 auto;
  position: relative;
  top: calc(50% - 25px);
  width: 50px;
}

@keyframes loading {
  to {
    transform: rotate(360deg);
  }
}

.folder-tree--panel {
  height: 100%;
}

.folder-tree--panel ul li.root-drive > span {
  font-weight: 900;
}

.popup-content--buttons > button {
  text-transform: uppercase;
  padding: 10px 25px;
  min-width: 200px;
  margin-right: 0;
  margin-left: auto;
  height: auto;
  width: auto;
}

</style>
