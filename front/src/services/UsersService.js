import api from "src/services/api";

class UsersService{
  getAllUsers(){
    return api.get('users/');
  }
  createUser(data){
    return api.post('users/', data)
  }
  deleteUser(user_id){
    return api.delete('users/' + user_id + '/')
  }
}

export default  new UsersService();
