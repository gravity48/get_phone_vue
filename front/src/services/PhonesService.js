import api from "src/services/api";


class PhonesService {

  sendSearchString(search_string, validation_data) {
    let data = {
      'search_string': search_string,
      'validate_data': validation_data,
    }
    return api.post('phones/', data, {
      params: {
        'action': 'new_question',
      }
    });
  }
  sendPagination(page_id, phone){
    let data = {
      'page_id': page_id,
      'phone': phone,
    }
    return api.post('phones/', data, {
      params: {
        'action': 'pagination'
      }
    })
  }

  sendPreviousRequest(data){
    return api.post('phones/', data, {
      params: {
        'action': 'previous_request',
      }
    })
  }

}

export default new PhonesService();
