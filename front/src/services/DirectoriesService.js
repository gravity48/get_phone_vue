import api from "src/services/api";

class DirectoriesService{

  getSubdir(data){
    return api.post('directories/',data, {params: {'action': 'get_sub_dir' }})
  }

  getRootDirectory(){
    return api.post('directories/',{}, {params: {'action': 'get_root_dir'}})
  }

}
export default new DirectoriesService();
