import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';

createApp(App).mount('#app');

const apiUrl = 'http://127.0.0.1:8000';

axios.get(`${apiUrl}/api/data`)
    .then(response => {
        console.log(response.data);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });