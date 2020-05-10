<template>
    <b-card header="Settings">
        <div v-if="this.isAuthorized">
            <b-form-group
                    :label='"Max Thumbnail Width: "+maxWidth+"px"'
            >
                <b-form-input v-model="maxWidth" type="range" min="70" max="150"></b-form-input>
            </b-form-group>
            <hr>
            <b-form-group
                    :label='"Max Thumbnail Height: "+maxHeight+"px"'
            >
                <b-form-input id="range-1" v-model="maxHeight" type="range" min="70" max="150"></b-form-input>
            </b-form-group>
            <hr>
            <b-form-group
                    :label='"Images per page: "+perPage'
            >
                <b-form-input id="range-1" v-model="perPage" type="range" min="1" max="100"></b-form-input>
            </b-form-group>
            <hr>
            <b-button type="button" @click="updateSettings" variant="secondary">Update</b-button>
        </div>
        <p v-else>Feature is not available without authorization.</p>
    </b-card>
</template>

<script>
  import axios from 'axios';

  export default {
    name: "Settings",
    data() {
      return {
        maxWidth: this.$globals.imageMeta['maxImageWidth'],
        maxHeight: this.$globals.imageMeta['maxImageHeight'],
        perPage: this.$globals.imageMeta['itemsPerPage']
      }
    },
    computed: {
      isAuthorized: function () {
        return this.$globals.flockEventToken && this.$globals.flockEvent
      }
    },
    methods: {
      updateSettings() {
        if (this.isAuthorized) {
          const headers = {'Authorization': `Bearer ${this.$globals.flockEventToken}`};
          const data = {
            'imageMeta': {
              'maxImageWidth': this.maxWidth,
              'maxImageHeight': this.maxHeight,
              'itemsPerPage': this.perPage
            }
          };
          axios
            .post(`${this.$globals.backend}/api/meta/update/`, data, {headers: headers})
            .then(response => {
              console.log(response);
              this.$root.$emit('addToast', 'Good evening', `Settings updated`, 'success', 3000);
            })
            .catch(error => {
              console.log(error);
              this.$root.$emit('addToast', 'Good evening', `Settings update failed: ${error}`, 'danger', 4000);
            })
        } else {
          console.error('Received no authorization data');
          this.$router.push('error');
        }
      }
    }
  }
</script>

<style scoped>

</style>