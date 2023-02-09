<template>
  <div id="app">
    <div class="container">
      <el-input type="textarea" :autosize="{ minRows: 2}" v-model="question" placeholder="请输入问题"/>
      <el-button @click="submitQuestion" type="primary">提交</el-button>
    </div>

    <div style="display: flex;">
      <div style="flex: 1; margin-right: 20px;">
        <h3>最新问题与回答</h3>
        <p>Human：{{ question }}</p>
        <p> Ai： {{ answer }}</p>
      </div>
      <div style="flex: 1;">
        <h3>历史请求与回答</h3>
        <ul>
          <li v-for="item in history" :key="item.question">
            Human:{{ item[2] }}<br>Ai:{{ item[3] }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'app',
  data() {
    return {
      question: '',
      answer: '',
      history: [],
    }
  },

  mounted() {
    this.$axios.get('/chathistory', {headers: {'Content-Type': 'application/json'}}).then(response => {
      this.history = response.data.reply;
      console.log('历史记录', response.data.reply);
    }).catch(error => {
      console.log(error);
    });
  },
  methods: {
    sendQuestion() {
      const response = axios.post('http://127.0.0.1:8081/chat2', {
        question: this.question,
      })
      const {data} = response
      this.answer = data.answer
      this.history.unshift({
        question: this.question,
        answer: this.answer,
      })
    },
    submitQuestion() {
      const data = {
        "question": this.question
      }
      const jsonData = JSON.stringify(data)
      console.log(jsonData)
      this.$axios.post('/chat2', jsonData, {headers: {'Content-Type': 'application/json'}}).then(response => {
        this.answer = response.data.reply;
        console.log(response.data);
      }).catch(error => {
        console.log(error);
      });
    }
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.container {
  text-align: left;
  margin: 0 auto;
  width: 400px;
  padding: 20px;
}

.history {
  text-align: left;
  margin: 0 auto;
  width: 400px;
  padding: 20px;
}
</style>
