<template>
    <div>
        <b-card header="Featured images">
            <div class="image-holder">
                <loading :active.sync="loading"
                         :can-cancel="false"
                         :is-full-page="true"></loading>
                <div v-if="imageList && imageList != 0">
                    <div v-masonry="" transition-duration="0.3s" item-selector=".item" gutter="5">
                        <div v-for="image in imageList.slice(startNumber,endNumber)" :key="image.id" v-masonry-tile class="item">
                            <FeaturedImageHolder :img="image" style="margin-top: 5px;"/>
                        </div>
                    </div>

                </div>
                <h2 v-else-if="loading"></h2>
                <h2 v-else>No featured images yet</h2>
            </div>
        </b-card>
        <b-pagination
                v-model="currentPage"
                :total-rows="rows"
                :per-page="perPage"
                align="center"
                pills
                class="bottom"
        ></b-pagination>
    </div>
</template>

<script>
  // Import component
  import Loading from 'vue-loading-overlay';
  // Import stylesheet
  import 'vue-loading-overlay/dist/vue-loading.css';
  import FeaturedImageHolder from './FeaturedImageHolder.vue';
  import axios from 'axios';

  export default {
    name: 'Featured',
    data() {
      return {
        imageList: [],
        loading: true,
        currentPage: 1,
      }
    },
    components: {
      FeaturedImageHolder,
      Loading
    },
    created() {
      this.$root.$on('removeImage', (id) => {
        var removeIndex = this.imageList.map(function (item) {
          return item.id;
        })
          .indexOf(id);
        ~removeIndex && this.imageList.splice(removeIndex, 1);
      });
      if (this.$globals.flockEventToken && this.$globals.flockEvent) {
        const headers = {'Authorization': `Bearer ${this.$globals.flockEventToken}`};
        axios
          .get(`${this.$globals.backend}/api/featured/${this.$globals.flockEvent['userId']}/`, {headers: headers})
          .then(response => {
            this.imageList = response.data['featured'];
            this.$globals.imageMeta = response.data['imageMeta'];
          })
          .catch(error => {
            console.log(error)
            this.$router.push('error');
          })
          .finally(() => {
            this.loading = false;
            this.alreadyLoaded = true
          })
      } else {
        console.error('Received no authorization data');
        this.$router.push('error');
      }
    },
    computed: {
      perPage() {
        if (this.$globals.imageMeta !== null) {
          return this.$globals.imageMeta['itemsPerPage']
        } else {
          return 10
        }
      },
      rows() {
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

<style scoped>

    .image-holder {
        margin-left: 5px;
    }

    h5 {
        text-align: center;
    }

    .bottom {
        position: fixed;
        bottom: 0;
        width: 100%;
    }
</style>