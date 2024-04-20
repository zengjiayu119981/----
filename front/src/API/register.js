import Server from "../utils/require"

function user_register(username,password){
    return  Server.post('api/register/user',{username,password})
}



export {
    user_register,
}