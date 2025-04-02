<template>
  <div id="app">
    <header>
      <h1>Kariya</h1>
      <p>Write something for Kariya to analyse your handwriting</p>
    </header>
    <main>
      <HandwritingCanvas @analyze="handleAnalyzeRequest" />
      <HandwritingAnalyzer 
        :handwritingData="handwritingData"
        @analysis-complete="handleAnalysisComplete" 
      />
      <SocialSharing v-if="analysisResults" :results="analysisResults" />
    </main>
    <footer>
      <p>© 2025 Kariya - Made with ❤️ by <a href="https://github.com/gongahkia/">Gabriel Ong.</a></p>
      <p>Source code <a href="https://github.com/gongahkia/kariya">here.</a></p>
    </footer>
  </div>
</template>

<script>
import HandwritingCanvas from './components/HandwritingCanvas.vue';
import HandwritingAnalyzer from './components/HandwritingAnalyzer.vue';
import SocialSharing from './components/SocialSharing.vue';

export default {
  name: 'App',
  components: {
    HandwritingCanvas,
    HandwritingAnalyzer,
    SocialSharing
  },
  data() {
    return {
      handwritingData: null,
      analysisResults: null
    }
  },
  methods: {
    handleAnalyzeRequest(data) {
      this.handwritingData = data;
    },
    handleAnalysisComplete(results) {
      this.analysisResults = results;
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

header {
  margin-bottom: 30px;
}

main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

footer {
  margin-top: 50px;
  font-size: 14px;
  color: #666;
}
</style>