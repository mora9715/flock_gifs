<template>
  <b-card header="Upload an Image">
    <b-form @submit="uploadImage" v-if="this.isAuthorized">
      <b-form-group id="input-group-1" label-for="input-1">
        <b-form-input
          id="input-2"
          v-model="name"
          required
          :state="name ? true : false"
          placeholder="Enter image name"
        ></b-form-input>
      </b-form-group>
      <b-form-group id="input-group-2" label-for="input-2">
      <b-form-file
        v-model="file"
        accept="image/*"
        required
        :state="file ? true : false"
        placeholder="Choose a file or drop it here..."
        drop-placeholder="Drop file here..."
      ></b-form-file>
      </b-form-group>
      <b-button type="button" @click="uploadImage" variant="secondary">Submit</b-button>
    </b-form>
      <p v-else>Feature is not available without authorization.</p>
  </b-card>
</template>

<script>

import axios from 'axios';

export default {
  name: 'UploadForm',
  components: {
  },
  data() {
    return {
      file: null,
      imageSrc: null,
      name: null
    }
  },
  computed: {
    isAuthorized: function() {
      if(this.$globals.flockEventToken && this.$globals.flockEvent) {
        return true;
      } else {
        return false;
      }
    }
  },
  methods: {
    uploadImage: function(){
      let _this = this;
      if (!_this.name || !_this.file) {
        _this.$root.$emit('addToast', 'Good evening',`Fill all fields to proceed!`, 'danger', 2000);
        return;
      }
      var reader = new FileReader();
      reader.onload = function(e) {
        _this.imageSrc = e.target.result.replace(/^data:.+;base64,/, '');
        const headers = {'Authorization': `Bearer ${_this.$globals.flockEventToken}`};
        const data = {'image': `${_this.imageSrc}==`, 'name': _this.name};
        axios
          .post(`${this.$globals.backend}/api/images/upload/`, data, {headers: headers})
          .then(response => {
            console.log(response);
            _this.$root.$emit('addToast','Good evening',`Uploaded ${_this.name}`, 'success', 3000);
          })
          .catch(error => {
            let errorBody = JSON.parse(error.request.response);
            let errorText = '';
            for (let [, value] of Object.entries(errorBody)) {
              errorText = value;
            }
            _this.$root.$emit('addToast', 'Good evening',`Upload failed: ${errorText}`, 'danger', 4000);
        })

      };
      reader.onerror = function(error) {
        this.$root.$emit('addToast', 'Good evening',`Upload failed: ${error}`, 'danger', 4000);
      };
      reader.readAsDataURL(this.file);
    }
  },
}
</script>

<style>
</style>