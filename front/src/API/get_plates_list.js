import Server from "../utils/require"

function get_plates_list(){
    return  Server.post('api/plate/list')
}



export {
    get_plates_list,
}