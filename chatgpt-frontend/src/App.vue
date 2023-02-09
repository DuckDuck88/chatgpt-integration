<template>
  <div id="app">
     <router-view><QuestionView/></router-view>
<!--     <router-link to="">test</router-link>-->
  </div>
</template>

<script>
import QuestionView from "@/views/QuestionView";

export default {
    components: {
      // TestElementUI,
      // TestElementUI,
      QuestionView,
    },
    name: 'App'
  }
</script>
