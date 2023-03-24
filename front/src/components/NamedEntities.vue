<template>
  <div class="panel">
    <div class="panel-header" @click.prevent="toggle_panel">
      <p>Извлечение именнованных сущностей</p>
      <button class="panel-ico" @click.stop="toggle_panel">
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-chevron-down" viewBox="0 0 16 16">
          <path fill-rule="evenodd"
                d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
        </svg>
      </button>
      <p>{{ this.proj_id }}</p>
    </div>
    <div class="panel-content">
      <div class="delete-projects-div">
        <button type="button" @click="this.$emit('remove:proj')">
          <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-x-lg"
               viewBox="0 0 16 16">
            <path
              d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
          </svg>
        </button>
      </div>
      <div class="column">
        <div class="input-group">
          <label for="dest_folder">Папка для обработки</label>
          <p>Обязательно начинается с /mnt/</p>
          <div class="custom-input">
            <FileManager v-if="file_manager_show" @close:popup="()=> {this.file_manager_show = false}"
                         @update:value="(value) =>{extract_proj.options.folder = value}"></FileManager>
            <input type="text" id="dest_folder" v-model="extract_proj.options.folder"
                   @click="file_manager_show = !file_manager_show" readonly>
            <span class="input-border"> </span>
          </div>
          <div class="input-error"></div>
        </div>
        <div class="input-group">
          <label for="doc_extension">Расширение документов</label>
          <p>Выберите расширения документов из списка доступных</p>
          <v-select multiple label='extension' :options="doc_extensions"
                    v-model="extract_proj.options.doc_extension"></v-select>
          <div class="input-error"></div>
        </div>
      </div>
      <div class="column">
        <div class="input-group">
          <label for="proj-alias">Имя обработчика</label>
          <p>Используется для создания лог-файла</p>
          <div class="custom-input">
            <input type="text" id="proj-alias" v-model="extract_proj.options.alias">
            <span class="input-border"> </span>
          </div>
          <div class="input-error"></div>
        </div>
        <div class="input-group">
          <label for="extract_process_count">Количество процессов</label>
          <p>Укажите число процессов которые будут использоваться при обработке</p>
          <div class="custom-input">
            <input type="number" id="extract_process_count" v-model="extract_proj.options.process_count"
                   :disabled="extract_proj.options.raw_data">
            <span class="input-border"></span>
          </div>
          <div class="input-error"></div>
        </div>
      </div>
      <div class="column-fill">
        <div class="additional-options">
          <div class="additional-header">Дополнительные опции</div>
          <div class="checkbox-group">
            <input class="check-box-input" id="check-only-new" type="checkbox"
                   v-model="extract_proj.options.only_new_files">
            <label for="check-only-new">Добавлять только новые файлы</label>
          </div>
          <div class="checkbox-group">
            <input class="check-box-input" id="check-raw-data" type="checkbox"
                   v-model="extract_proj.options.raw_data">
            <label for="check-raw-data">Заносить сведения базу данных без обработки</label>
          </div>
        </div>
        <div class="program-control">
          <button class="play-btn" :disabled="extract_proj.is_start" @click="StartProject(extract_proj)">Старт
          </button>
          <button class="stop-btn" :disabled="!extract_proj.is_start" @click="StopProject(extract_proj)">Стоп
          </button>
        </div>
        <div class="wrapper" @click="StatusProject">
          <p>{{ extract_proj.status }} </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TrainingService from "src/services/TrainingService";
import FileManager from "./FileManager.vue";

export default {
  name: "NamedEntities",
  components: {
    FileManager,
  },
  props: {
    proj_id: Number,
  },
  emits: ['remove:proj'],
  data() {
    return {
      file_manager_show: false,
      doc_extensions: [],
      extract_proj: {
        options: {}
      },
      field_translation: {
        'all': 'Соединение к базе данных',
        'extract_entity_proj': 'Извлечение именнованных сущностей',
      },
    }
  },
  mounted() {
    this.getInitData();
    setInterval(this.StatusProject, 2000);
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
    StartProject(data) {
      TrainingService.startProject(data).then(response => {
        data.is_start = true;
        this.$notify({
          type: 'success',
          title: this.field_translation[data['proj_type']],
          text: 'Запущен',
          duration: 5000,
        });
      });
    },
    StatusProject() {
      if (this.extract_proj.is_start) {
        TrainingService.statusProject(this.extract_proj).then(response => {
          this.extract_proj.status = response.data.status
        });
      }
    },
    StopProject(data) {
      TrainingService.stopProject(data).then(response => {
        data.is_start = false;
        data.status = response.data.status;
      })
    },
    getInitData() {
      TrainingService.getRetrieveProj(this.proj_id).then(response => {
        this.extract_proj = response.data;
      })
      TrainingService.getDocExtensions().then(response => {
        this.doc_extensions = response.data;
      })
    },
    updateExtractEntity(data) {
      TrainingService.partialUpdateProj(this.proj_id, data);
    },
  },
  watch: {
    'extract_proj.options': {
      handler(newValue, oldValue) {
        this.updateExtractEntity(newValue);
      },
      deep: true,
    },
  }
}
</script>

<style scoped>


.panel-header p:last-child {
  position: absolute;
  top: 14px;
  left: 10px;
}

.wrapper {
  border: 1px solid blue;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.program-control {
  display: flex;
  align-items: center;
  min-width: 300px;
  justify-content: center;
  border: 1px solid #4CAF50;
  margin: 0 10px;
  border-radius: 10px;
}

.panel .panel-header {
  background-color: transparent;
  border: 2px solid rgba(128, 128, 128, 0.78);
  border-radius: 20px;
  margin: 0;
}

.panel-content {
  border: 2px solid rgba(128, 128, 128, 0.78);
  border-top: none;
  border-radius: 20px;
  padding: 5px 5px;
}

.program-control button {
  margin: 0 10px;
}
</style>
