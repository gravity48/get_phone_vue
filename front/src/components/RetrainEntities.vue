<template>
  <div class="panel">
    <div class="panel-header" @click.prevent="toggle_panel">
      <p>Переобучение выборки</p>
      <button class="panel-ico" @click.stop="toggle_panel">
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-chevron-down" viewBox="0 0 16 16">
          <path fill-rule="evenodd"
                d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z"/>
        </svg>
      </button>
      <p>{{proj_id }}</p>
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
          <label for="doc_status">Статус документов</label>
          <p>Выбрать в случае необходимости документы по их статусу</p>
          <v-select multiple label="status_name" :options="doc_status"
                    v-model="retrain_proj.options.status"></v-select>
          <div class="input-error"></div>
        </div>
        <div class="input-group">
          <label for="record_id">ID документа в БД</label>
          <p>Используйте id документа чтобы продолжить в случае сбоя</p>
          <div class="custom-input">
            <input type="number" id="record_id" v-model="retrain_proj.options.record_id">
            <span class="input-border"></span>
          </div>
          <div class="input-error"></div>
        </div>
      </div>
      <div class="column">
        <div class="input-group">
          <label for="alias-retrain">Имя обработчика</label>
          <p>Используется для хранения лог файлов</p>
          <div class="custom-input">
            <input type="text" id="alias-retrain" v-model="retrain_proj.options.alias">
            <span class="input-border"> </span>
          </div>
          <div class="input-error"></div>
        </div>
        <div class="input-group">
          <label for="process_count">Количество процессов</label>
          <p>Укажите число процессов которые будут использоваться при обработке</p>
          <div class="custom-input">
            <input type="number" id="process_count" v-model="retrain_proj.options.process_count">
            <span class="input-border"></span>
          </div>
          <div class="input-error"></div>
        </div>
      </div>
      <div class="column-fill">
        <div class="additional-options">
          <div class="additional-header">Дополнительные опции</div>
          <div class="checkbox-group">
            <input class="check-box-input" id="delete-old-files" type="checkbox"
                   v-model="retrain_proj.options.delete_not_found">
            <label for="delete-old-files">Удалять не найденные файлы</label>
          </div>
        </div>
        <div class="program-control">
          <button class="play-btn" :disabled="retrain_proj.is_start" @click.stop="StartProject(retrain_proj)">Старт
          </button>
          <button class="stop-btn" :disabled="!retrain_proj.is_start" @click.stop="StopProject(retrain_proj)">Стоп</button>
        </div>
        <div class="wrapper" @click="StatusProject">
          <p>{{ retrain_proj.status }} </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TrainingService from "src/services/TrainingService";

export default {
  name: "RetrainEntities",
  data(){
    return{
      doc_status: [],
      retrain_proj: {
        options: {}
      },
      field_translation: {
        'all': 'Соединение к базе данных',
        'extract_entity_proj': 'Извлечение именнованных сущностей',
        'retrain_proj': 'Переобучение выборки',
      },
    }
  },
  props:{
    proj_id: Number,
  },
  emits: ['remove:proj'],
  mounted() {
    this.getInitData();
    setInterval(this.StatusProject, 2000);
  },
  methods:{
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
      if(this.retrain_proj.is_start) {
        TrainingService.statusProject(this.retrain_proj).then(response => {
          this.retrain_proj.status = response.data.status;
        });
      }
    },
    StopProject(data) {
      TrainingService.stopProject(data).then(response => {
        data.is_start = false;
        data.status = response.data.status;
      })
    },
    getInitData(){
      TrainingService.getRetrieveProj(this.proj_id).then(response => {
        this.retrain_proj = response.data;
      })
      TrainingService.getDocStatus().then(response => {
        this.doc_status = response.data;
      })
    },
    updateRetrainProj(data){
      TrainingService.partialUpdateProj(this.proj_id, data);
    }
  },
  watch:{
    'retrain_proj.options': {
      handler(newValue, oldValue) {
        this.updateRetrainProj(newValue);
      },
      deep: true
    }
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
