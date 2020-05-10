<template>
<b-card header="All images">
  <div class="image-holder">
    <loading :active.sync="loading" 
        :can-cancel="false" 
        :is-full-page="true"></loading>
    <div v-if="imageList.length != 0">
      <div v-masonry="" transition-duration="0.3s" item-selector=".item" gutter="5">
        <div v-for="image in imageList.slice(startNumber,endNumber)" :key="image.id" v-masonry-tile class="item">
          <AllImageHolder :img="image" style="margin-top: 5px;"/>
        </div>
      </div>
      <br>
      <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      align="fill"
      pills
      size="sm"
    ></b-pagination>
    </div>
    <h2 v-else-if="loading"></h2>
    <h2 v-else>No images yet</h2>
  </div>
  </b-card>
</template>

<script>
// Import component
import Loading from 'vue-loading-overlay';
// Import stylesheet
import 'vue-loading-overlay/dist/vue-loading.css';
import AllImageHolder from './AllImageHolder.vue';
import axios from 'axios';

export default {
  name: 'All',
  data() {
    return {
      imageList: [],
      loading: true,
      currentPage: 1,
      perPage: 6,
    }
  },
  components: {
    AllImageHolder,
    Loading
  },
  created() {
    if ( this.$globals.flockEventToken && this.$globals.flockEvent ) {
      const headers = {'Authorization': `Bearer ${this.$globals.flockEventToken}`};
      axios
        .get(`${this.$globals.backend}/api/images/`, {headers: headers})
        .then(response => {
          this.imageList = response.data['images'];
          this.$globals.imageMeta = response.data['imageMeta'];
        })
        .catch(error => {
          console.log(error)
          this.$router.push('error');
        })
        .finally(() => {this.loading = false; this.alreadyLoaded = true})
    } else {
      console.error('Received no authorization data');
      this.$router.push('error');
    }
    console.log(this.$globals);
  },
  computed: {
    rows()  {
      return this.imageList.length
    },
    startNumber() {
      return (this.currentPage - 1) * this.perPage
    },
    endNumber() {
      return this.currentPage * this.perPage
    }
  }
}
</script>

<style lang="scss">

@import '../assets/theme.scss';

.image-holder {
  margin-left: 5px;
}
h5 {
  text-align: center;
}



</style>