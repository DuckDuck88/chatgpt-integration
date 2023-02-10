import {createApp} from 'vue'
import installElementPlus from './plugins/element'
// import Chat from 'jwchat';
import router from './router'
import App from './App'
import axios from 'axios'

// axios.defaults.baseURL = 'http://localhost:8081'
axios.defaults.baseURL = process.env.VUE_APP_SERVER

const app = createApp(App)
// app.use(Chat)
app.use(router)
installElementPlus(app)
app.config.globalProperties.$axios = axios
app.mount('#app')
