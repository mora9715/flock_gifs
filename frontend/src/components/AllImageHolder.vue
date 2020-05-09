<template>
<div @mouseover="isHovered=true" @mouseleave="isHovered=false" class="holder holder-focus">
  <div v-if="isHovered" class="holder-top-right">
    <b-icon-star-fill @click="processFeatured()" class="holder-icon-focus" font-scale="1.3" variant="warning"/>
  </div>
  <div v-if="isHovered" class="holder-bottom-right">
    <b-icon-clipboard-data  @click="copyImage()" class="holder-icon-focus" font-scale="1.3" variant="primary"/>
  </div>
  <img
    :src='source'
    alt=""
    :style="{maxWidth: $globals.imageMeta['maxImageWidth']+'px', maxHeight: $globals.imageMeta['maxImageHeight']+'px'}"
    style="z-index: -1;"
  >
</div>
</template>

<script>

import axios from 'axios';

export default {
  name: 'FeaturedImageHolder',
  components: {
  },
  data() {
    return {
      isHovered: false,
    }
  },
  props: {
    img: {
      type: Object,
      required: false
    }
  },
  methods: {
    processFeatured: function() {
      const headers = {'Authorization': `Bearer ${this.$globals.flockEventToken}`};
      const data = {'add': [this.img.id]};
      axios
        .post(`${this.$globals.backend}/api/featured/${this.$globals.flockEvent['userId']}/update/`, data, {headers: headers})
        .then(response => {
          console.log(response);
          this.$root.$emit('addToast','Good evening',`Added ${this.img.name} to featured`, 'success', 3000);
        })
        .catch(error => {
          this.$root.$emit('addToast', 'Good evening',`Image ${this.img.name} has not been added: ${error}`, 'danger', 2000);
        })
        .finally(() => {this.loading = false; this.alreadyLoaded = true})
    },
    copyImage: function() {
      this.$copyText(`${this.$globals.slashCommand} ${this.img.name}`);
      this.$root.$emit('addToast', 'Good evening',`Image ${this.img.name} copied`, 'info', 1000);
    }
  },
  computed: {
    source: function() {
      return `${this.$globals.backend}/${this.img.image}`;
    }
  },
}
</script>

<style>
.holder {
  position: relative;
}

.holder-top-right {
  position: absolute;
  top: 5px;
  right: 5px;
}

.holder-bottom-right {
  position: absolute;
  top: 35px;
  right: 5px;
}

.holder-icon-focus {
  transition: .2s;
}

.holder-icon-focus:hover {
  cursor: pointer;
  transform: scale(1.2);
}

.holder-focus {
  transition: transform .5s, box-shadow .5s; /* Animation */
}

.holder-focus:hover {
  transform: scale(1.04); /* (150% zoom - Note: if the zoom is too large, it will go outside of the viewport) */
  box-shadow: 0px 0px 10px 5px rgba(84,84,84,1);
}
</style>