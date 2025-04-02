<template>
  <div class="analyzer">
    <div v-if="isAnalyzing" class="loading">
      <p>Analyzing your handwriting...</p>
    </div>
    <div v-else-if="results" class="results">
      <h3>Analysis Results</h3>
      <div class="score-container">
        <div class="score" :class="{ 'good-score': results.totalScore > 70, 'bad-score': results.totalScore < 50 }">
          {{ results.totalScore }}/100
        </div>
        <p class="verdict">Your handwriting is {{ results.isCooked ? 'COOKED 🔥' : 'NOT COOKED ✅' }}</p>
      </div>
      
      <div class="details">
        <h4>Details:</h4>
        <p><strong>Legibility Score:</strong> {{ results.legibilityScore }}/100</p>
        <p><strong>Consistency Score:</strong> {{ results.consistencyScore }}/100</p>
        <p><strong>Classification:</strong> {{ results.classification }}</p>
        <p><strong>Confidence:</strong> {{ (results.confidence * 100).toFixed(2) }}%</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HandwritingAnalyzer',
  props: {
    handwritingData: Object
  },
  data() {
    return {
      isAnalyzing: false,
      results: null
    }
  },
  watch: {
    handwritingData(newData) {
      if (newData) {
        this.analyzeHandwriting(newData);
      }
    }
  },
  methods: {
    async analyzeHandwriting(data) {
      this.isAnalyzing = true;
      this.results = null;
      
      try {
        // Send data to backend for analysis
        const response = await axios.post('/api/analyze', {
          imageData: data.imageData,
          strokes: data.strokes
        });
        
        this.results = response.data;
        this.$emit('analysis-complete', this.results);
      } catch (error) {
        console.error('Error analyzing handwriting:', error);
        // For demo purposes, generate mock results if backend is not available
        this.generateMockResults();
      } finally {
        this.isAnalyzing = false;
      }
    },
    
    generateMockResults() {
      // Mock results for demonstration
      const legibilityScore = Math.floor(Math.random() * 100);
      const consistencyScore = Math.floor(Math.random() * 100);
      const totalScore = Math.floor((legibilityScore + consistencyScore) / 2);
      
      this.results = {
        legibilityScore: legibilityScore,
        consistencyScore: consistencyScore,
        totalScore: totalScore,
        isCooked: totalScore < 60,
        classification: totalScore < 40 ? 'Illegible Scribble' : 
                       totalScore < 60 ? 'Poor Handwriting' : 
                       totalScore < 80 ? 'Average Handwriting' : 'Excellent Handwriting',
        confidence: 0.85 + (Math.random() * 0.15)
      };
      
      this.$emit('analysis-complete', this.results);
    }
  }
}
</script>

<style scoped>
.analyzer {
  margin: 20px 0;
  padding: 15px;
  border-radius: 8px;
  background-color: #f5f5f5;
  max-width: 500px;
}

.loading {
  text-align: center;
  padding: 20px;
}

.score-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.score {
  font-size: 48px;
  font-weight: bold;
  padding: 10px 20px;
  border-radius: 50%;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  background-color: #f0f0f0;
}

.good-score {
  background-color: #4CAF50;
  color: white;
}

.bad-score {
  background-color: #f44336;
  color: white;
}

.verdict {
  font-size: 18px;
  font-weight: bold;
}

.details {
  background-color: white;
  padding: 15px;
  border-radius: 8px;
}
</style>