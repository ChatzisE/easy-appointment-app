import axios from 'axios';
const ajax = {
    async get(url, args) {
        let _args = {};
        if (args) {
            _args = { params: args };
        }
        var s = await axios.get(url, _args)
        return s.data;
    },
    async post(url, args) {
        let _args =args|| {};
        var s = await axios.post(url, _args)
        return s.data;
    },
    async delete(url, args) {
        let _args = {};
        if (args) {
            _args = { data: args };
        }
        var s = await axios.delete(url, _args)
        return s.data;
    }
}
export default ajax;