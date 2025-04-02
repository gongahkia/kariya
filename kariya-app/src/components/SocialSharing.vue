<template>
  <div class="social-sharing">
    <h3>Share Your Results</h3>
    <div class="share-buttons">
      <button @click="shareOnFacebook" class="facebook">
        <span>Share on Facebook</span>
      </button>
      <button @click="shareOnTwitter" class="twitter">
        <span>Share on Twitter</span>
      </button>
      <button @click="shareOnWhatsApp" class="whatsapp">
        <span>Share on WhatsApp</span>
      </button>
    </div>
  </div>
</template>

<script>
import { SFacebook, STwitter, SWhatsapp } from 'vue-socials';

export default {
  name: 'SocialSharing',
  components: {
    SFacebook,
    STwitter,
    SWhatsapp
  },
  props: {
    results: Object
  },
  computed: {
    shareText() {
      if (!this.results) return '';
      
      return `I just analyzed my handwriting and scored ${this.results.totalScore}/100. My handwriting is ${this.results.isCooked ? 'COOKED 🔥' : 'NOT COOKED ✅'}. Check out this cool handwriting analyzer!`;
    },
    shareUrl() {
      return window.location.href;
    }
  },
  methods: {
    shareOnFacebook() {
      const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(this.shareUrl)}&quote=${encodeURIComponent(this.shareText)}`;
      this.openShareWindow(url);
    },
    
    shareOnTwitter() {
      const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(this.shareText)}&url=${encodeURIComponent(this.shareUrl)}`;
      this.openShareWindow(url);
    },
    
    shareOnWhatsApp() {
      const url = `https://wa.me/?text=${encodeURIComponent(this.shareText + ' ' + this.shareUrl)}`;
      this.openShareWindow(url);
    },
    
    openShareWindow(url) {
      window.open(url, '_blank', 'width=600,height=400');
    }
  }
}
</script>

<style scoped>
.social-sharing {
  margin: 20px 0;
  padding: 15px;
  border-radius: 8px;
  background-color: #f5f5f5;
  max-width: 500px;
}

.share-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 15px;
}

button {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.facebook {
  background-color: #3b5998;
}

.twitter {
  background-color: #1da1f2;
}

.whatsapp {
  background-color: #25d366;
}
</style>