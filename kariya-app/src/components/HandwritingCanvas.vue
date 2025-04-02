<template>
  <div class="handwriting-canvas">
    <h3>Write something below</h3>
    <canvas 
      ref="canvas" 
      @mousedown="startDrawing" 
      @mousemove="draw" 
      @mouseup="stopDrawing"
      @touchstart="startDrawingTouch"
      @touchmove="drawTouch"
      @touchend="stopDrawing"
      width="500" 
      height="300">
    </canvas>
    <div class="controls">
      <button @click="clearCanvas">Clear</button>
      <button @click="analyzeHandwriting">Analyze</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HandwritingCanvas',
  data() {
    return {
      isDrawing: false,
      context: null,
      strokes: []
    }
  },
  mounted() {
    const canvas = this.$refs.canvas;
    this.context = canvas.getContext('2d');
    this.context.lineWidth = 3;
    this.context.lineCap = 'round';
    this.context.strokeStyle = 'black';
  },
  methods: {
    startDrawing(event) {
      this.isDrawing = true;
      this.context.beginPath();
      this.context.moveTo(
        event.clientX - this.$refs.canvas.getBoundingClientRect().left,
        event.clientY - this.$refs.canvas.getBoundingClientRect().top
      );
      
      // Start a new stroke
      this.currentStroke = [{
        x: event.clientX - this.$refs.canvas.getBoundingClientRect().left,
        y: event.clientY - this.$refs.canvas.getBoundingClientRect().top,
        time: Date.now()
      }];
    },
    
    draw(event) {
      if (!this.isDrawing) return;
      
      const x = event.clientX - this.$refs.canvas.getBoundingClientRect().left;
      const y = event.clientY - this.$refs.canvas.getBoundingClientRect().top;
      
      this.context.lineTo(x, y);
      this.context.stroke();
      
      // Add point to current stroke
      this.currentStroke.push({
        x: x,
        y: y,
        time: Date.now()
      });
    },
    
    startDrawingTouch(event) {
      event.preventDefault();
      const touch = event.touches[0];
      this.startDrawing({
        clientX: touch.clientX,
        clientY: touch.clientY
      });
    },
    
    drawTouch(event) {
      event.preventDefault();
      const touch = event.touches[0];
      this.draw({
        clientX: touch.clientX,
        clientY: touch.clientY
      });
    },
    
    stopDrawing() {
      this.isDrawing = false;
      if (this.currentStroke && this.currentStroke.length > 0) {
        this.strokes.push(this.currentStroke);
        this.currentStroke = null;
      }
    },
    
    clearCanvas() {
      this.context.clearRect(0, 0, this.$refs.canvas.width, this.$refs.canvas.height);
      this.strokes = [];
    },
    
    analyzeHandwriting() {
      // Convert canvas to image data
      const imageData = this.$refs.canvas.toDataURL('image/png');
      
      // Emit event with image data and strokes for analysis
      this.$emit('analyze', {
        imageData: imageData,
        strokes: this.strokes
      });
    }
  }
}
</script>

<style scoped>
.handwriting-canvas {
  display: flex;
  flex-direction: column;
  align-items: center;
}

canvas {
  border: 1px solid #ccc;
  background-color: #fff;
  margin-bottom: 15px;
}

.controls {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>