<template>
  <div class="projects-list">
    <div class="custom-wrap"></div>
    <p>Список обработчиков</p>
    <div class="custom-wrap"></div>
    <button type="button" @click.stop.prevent="proj_create_modal_window = !proj_create_modal_window">
      <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-file-plus"
           viewBox="0 0 16 16">
        <path d="M8.5 6a.5.5 0 0 0-1 0v1.5H6a.5.5 0 0 0 0 1h1.5V10a.5.5 0 0 0 1 0V8.5H10a.5.5 0 0 0 0-1H8.5V6z"/>
        <path
          d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm10-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1z"/>
      </svg>
    </button>
    <transition appear
                enter-active-class="animated fadeInLeft"
                leave-active-class="animated fadeOutLeft">
      <div class="popup-form" v-show="proj_create_modal_window">
        <ul>
          <li @click="addProject('extract_entity_proj')">Извлечение именованных сущеностей</li>
          <li @click="addProject('retrain_proj')">Переобучение выборки</li>
        </ul>
      </div>
    </transition>
  </div>
  <ul id="project-list-ul">
    <li v-for="(project, index) in projects" :key="project.id">
      <NamedEntities v-if="project.proj_type === 'extract_entity_proj'" :proj_id="project.id"
                     @remove:proj="this.deleteProj(index)"></NamedEntities>
      <RetrainEntities v-if="project.proj_type === 'retrain_proj'" :proj_id="project.id"
                     @remove:proj="this.deleteProj(index)"></RetrainEntities>
    </li>
  </ul>
</template>

<script>
import TrainingService from "src/services/TrainingService";
import NamedEntities from "components/NamedEntities.vue";
import RetrainEntities from "components/RetrainEntities.vue";

var handle_timeout;

export default {
  name: "TrainingPage",
  components: {
    NamedEntities,
    RetrainEntities,
  },
  data() {
    return {
      projects: [],
      proj_create_modal_window: false,
      extract_proj: {
        options: {}
      },
      doc_extensions: [],
      doc_status: [],
      retrain_proj: {
        options: {}
      },
      field_translation: {
        'all': 'Соединение к базе данных',
        'extract_entity_proj': 'Извлечение именнованных сущностей',
      },
    }
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
    addProject(proj_type){
      TrainingService.addProject({proj_type: proj_type}).then(response =>{
        this.projects.push(response.data);
      })
    },
    getInitData() {
      TrainingService.getProjects().then(response => {
        this.projects = response.data;
      })
    },
    deleteProj(index) {
      TrainingService.removeProj(this.projects[index].id).then((response) => {
        this.projects.splice(index, 1);
      })
    },
  },
  mounted() {
    this.getInitData();
    document.body.addEventListener('click', () => {
      this.proj_create_modal_window = false
    }, true);
  },
  computed: {
  },
}
</script>

<style scoped>


.popup-form {
  text-align: center;
  z-index: 10000;
  background-color: white;
  position: absolute;
  top: 26px;
  left: calc(100% - 291px);
}

.popup-form > ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.popup-form > ul > li {
  padding: 10px;
}

.popup-form > ul > li:hover {
  background-color: #eee;
  cursor: pointer;
}

.custom-wrap {
  flex-grow: 2;
}

.projects-list button {
  width: 30px;
  height: 30px;
  background-color: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
}

.projects-list button svg {
  width: 100%;
  height: 100%;
  padding: 0;
}

#project-list-ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

#project-list-ul li {
}

#project-list-ul .panel {
  margin: 5px 0;
}


.projects-list {
  height: 50px;
  width: 100%;
  background-color: #eee;
  margin: 5px 0;
  padding: 5px;
  display: flex;
  align-items: center;
  position: relative;
  user-select: none;
}





</style>
