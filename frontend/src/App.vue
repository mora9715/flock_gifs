<template>
  <div id="app">
    <b-navbar type="dark" variant="dark">
      <b-navbar-nav>
        <router-link :to="{name: 'home'}" v-slot="{ navigate, href }">
          <b-nav-item :disabled="isActive(href, $route.path)" :href="href" @click="navigate"><b-icon-collection/></b-nav-item>
        </router-link>
        <router-link :to="{name: 'featured'}" v-slot="{ navigate, href }">
          <b-nav-item :disabled="isActive(href, $route.path)" :href="href" @click="navigate"><b-icon-bookmarks/></b-nav-item>
        </router-link>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto">
        <router-link :to="{name: 'upload'}" v-slot="{ navigate, href }">
          <b-nav-item :disabled="isActive(href, $route.path)" :href="href" @click="navigate"><b-icon-upload/></b-nav-item>
        </router-link>
        <router-link :to="{name: 'info'}" v-slot="{ navigate, href }">
          <b-nav-item :disabled="isActive(href, $route.path)" :href="href" @click="navigate"><b-icon-info-circle/></b-nav-item>
        </router-link>
      </b-navbar-nav>
    </b-navbar>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
    }
  },
  methods: {
    isActive: function(currentRoute, desiredRoute) {
      return (currentRoute === '#'+desiredRoute);
    },
    makeToast(title, contents, variant='info', timeout) {
      console.log(timeout);
      this.$bvToast.toast(contents, {
        title: title,
        autoHideDelay: timeout,
        variant: variant,
        toaster: 'b-toaster-bottom-left'
      })
    }
  },
  components: {
  },
  created() {
    this.$root.$on('addToast', (title, contents, variant='info', timeout=4000) => {
      this.makeToast(title, contents, variant, timeout);
    });
    // Gettings data from Flock:
    const _this = this;
    let uri = window.location.href.split('#').shift().split('?');
    if (uri.length == 2)
    {
      let vars = uri[1].split('&');
      let tmp = '';
      try {
        vars.forEach(function(v){
          tmp = v.split('=');
          if(tmp.length == 2) {
            if (tmp[0] === 'flockEventToken'){
              _this.$globals.flockEventToken = tmp[1];
              
            }
            else if(tmp[0] === 'flockEvent'){
              _this.$globals.flockEvent = JSON.parse(decodeURIComponent(tmp[1]));
            }
            else if(tmp[0] === 'flockTheme'){
              _this.$globals.flockTheme = JSON.parse(decodeURIComponent(tmp[1]));
            }
          }
        });
      }
      catch(error) {
        console.log('Incorrect JSON payload from Flock! Not all features will be available\n', error);
      }
    }
  }
}
</script>