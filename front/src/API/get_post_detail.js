import Server from "../utils/require"

function get_post_detail(post_id){
    return  Server.post('api/post/detail',{post_id})
}



export {
    get_post_detail,
}