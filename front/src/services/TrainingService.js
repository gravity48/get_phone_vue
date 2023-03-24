import api from 'src/services/api'

let EntityProj = 'extract_entity_proj'
let RetrainProj = 'retrain_proj'

class TrainingService{
  addProject(data){
    return api.post('proj_settings_list/', data);
  }
  getProjects(){
    return api.get('proj_settings_list/');
  }

  getRetrieveProj(proj_id){
    return api.get('proj_settings_list/' + proj_id + '/');
  }

  partialUpdateProj(proj_id, data){
    return api.patch('proj_settings_list/' + proj_id + '/', {'options': data});
  }

  getDocExtensions(){
    return api.get('extensions/')
  }

  removeProj(proj_id){
    return api.delete('proj_settings_list/' + proj_id+'/');
  }

  getDocStatus(){
    return api.get('doc_status/')
  }

  updateExtractEntity(data){
    return api.patch('proj_settings/', {'options': data}, {params: {proj: EntityProj}})
  }

  updateRetrainProj(data){
    return api.patch('proj_settings/', {'options': data}, {params: {proj: RetrainProj}})
  }

  startProject(data){
    data['action'] = 'start_proj'
    return api.post('proj_control/', data)
  }

  statusProject(data){
    data['action'] = 'status_proj';
    return api.post('proj_control/', data)
  }

  stopProject(data) {
    data['action'] = 'stop_proj'
    return api.post('proj_control/', data)
  }
}

export default new TrainingService();


