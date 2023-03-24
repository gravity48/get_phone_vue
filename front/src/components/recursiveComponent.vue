<template>
  <li class="recursive-li-item" :class="{'expanded': expanded, 'loading': preloader_show, 'selected': item.selected, 'empty': empty}"
      @click.stop.prevent="getSubDir(item)" :data-path="item.path"><span>{{ item.name }}</span>
    <ul class="sublist">
      <recursiveComponent @update:select-value="(value) => recursiveEmit(value)"
                          v-for="(subitem, subindex) in item.sub_folders"
                          :key="subindex"
                          :item="subitem">
      </recursiveComponent>
    </ul>
  </li>
</template>
<script>
import DirectoriesService from "src/services/DirectoriesService";

export default {
  name: "recursiveComponent",
  props: ["item",],
  emits: ['update:select-value',],
  data() {
    return {
      expanded: false,
      preloader_show: false,
      selected: false,
      empty: false,
    }
  },
  methods: {
    async getSubDir(item) {
      this.$emit('update:select-value', item);
      this.expanded = !this.expanded;
      if (item.sub_folders === null) {
        this.preloader_show = true;
        await DirectoriesService.getSubdir({'folder': item.path}).then((response) => {
          item.sub_folders = response.data;
          if (item.sub_folders.length === 0){
            this.empty = true;
          }
        });
        this.preloader_show = false;
      }
    },
    recursiveEmit(value) {
      this.$emit('update:select-value', value);
    }
  }
}

</script>
<style>
p {
  margin: 0;
}

ul {
  padding-left: 0;
  list-style-type: none;
  margin: 0;
}


.sublist {
  display: none;
  padding-left: 20px;
}

li.recursive-li-item.expanded > .sublist {
  display: block;
}

.folder-tree--panel ul li.selected > span {
  font-weight: 900;
  background: linear-gradient(270deg, rgba(76, 175, 80, .6) 0%, rgba(76, 175, 80, .3) 50%, rgba(76, 175, 80, 0.1) 100%);
}

li.recursive-li-item.expanded:before {
  content: '-';
}

li.recursive-li-item.empty {
  padding-left: 19.5px;
}

li.recursive-li-item.empty:before {
  display: none;
}

li.recursive-li-item.loading:before {
  content: '';
  display: inline-block;
  width: 5px;
  height: 5px;
  border: 1px solid rgba(76, 175, 80);
  border-top: none;
  border-radius: 50%;
  margin-right: 12.5px;
  animation: loading .5s linear infinite;
}

li.recursive-li-item:before:hover {
  color: rgb(76, 175, 80);
}

li.recursive-li-item > span {
  vertical-align: middle;
  cursor: default;
  display: inline-block;
  width: calc(100% - 20px);
}

li.recursive-li-item:before {
  content: '+';
  vertical-align: middle;
  margin-right: 10px;
  cursor: pointer;
  color: rgb(72, 169, 75);
  display: inline-block;
  width: 9.5px;
  transition: color .2s;
}

li.recursive-li-item {
  padding: 3px 0;
  text-align: left;
}

@keyframes loading {
  to {
    transform: rotate(360deg);
  }
}

</style>
