import Server from "../utils/require"

function get_plate_pic(){
    return  Server.post('api/palte/pic')
}



export {
    get_plate_pic,
}