<template>
  <div id="app">
    <el-container>
<!--      <el-aside>-->
<!--      </el-aside>-->
      <el-header>aaa</el-header>
      <el-aside>bbb</el-aside>
      <el-main>
        <QuestionView/>
      </el-main>
      <el-aside>
        <TestElementUI/>
      </el-aside>
      <el-footer>
        <TestElementUI/>
      </el-footer>
    </el-container>
     <router-view></router-view>
  </div>
</template>

<script>
import QuestionView from "@/views/QuestionView";
import TestElementUI from "@/views/TestElementUI";

export default {
    components: {
      TestElementUI,
      QuestionView,
    },
    name: 'App'
  }
</script>
