// authAxios.js

import axiosApi from "axios";

let axios = null;
let baseURL = process.env.VUE_APP_BASEURL;

axios = axiosApi.create({
    baseURL: baseURL,
});

if (localStorage.getItem('token')) {
    axios = axiosApi.create({
        baseURL: baseURL,
        headers: {
            'Content-Type': 'application/json',
            Authorization: 'Token ' + localStorage.getItem('token')
        }
    });
}

module.exports = axios
export default axios;

