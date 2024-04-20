import Server from "../utils/require"

function user_login(username,password){
    return  Server.post('api/login/user',{username,password})
}



export {
    user_login,
}