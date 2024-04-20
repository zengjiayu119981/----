import Server from "../utils/require"

function get_posts_list(title){
    return  Server.post('api/posts/list',{title})
}



export {
    get_posts_list,
}