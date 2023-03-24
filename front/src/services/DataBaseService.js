import api from 'src/services/api'

class  DataBaseService{
  updateDataBase(data){
    return api.put('database/', data)
  }
  getDatabaseData(){
    return api.get('database/')
  }
}

export  default new DataBaseService();
