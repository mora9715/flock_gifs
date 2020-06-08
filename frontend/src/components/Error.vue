<template>
    <div class="body">
        <h1 class="neg title"><span class="bg">Error - 403/404/5**/whatever</span></h1>
        <h1 style="text-align:center;">Welcome to limbo.</h1>
        <div class="text-holder">
            <p>
                A region on the border of purdeg RAM and oblivion,<br/>
                serving as the abode after death of crashed pages<br/>
                and of the righteous visitors who died trying to access the content.
            </p>
            <p>Try reinstalling app <b-button style="background-color:#aaaaaa;" @click="openBrowser">here</b-button> if you see this page.</p>
        </div>

    </div>
</template>

<script>
  export default {
    name: 'Error',
    data() {
      return {}
    },
    created() {
      this.$loadScript('https://apps-static.flock.co/js-sdk/1.8.6/flock.js')
    },
    methods: {
      openBrowser: function() {
        console.log('clicked');
        /* eslint-disable */
        flock.openBrowser('https://apps.flock.com/manage')
        /* eslint-enable */
      }
    }
  }
</script>

<style scoped>
    @import 'https://fonts.googleapis.com/css?family=VT323';

    h1 {
        font: normal 2.75rem/1.05em 'VT323', monospace;
        color: #e0e2f4;
    }

    p {
        font: normal 20px/1.25rem 'VT323', monospace;
        color: #e0e2f4;
    }

    .body {
        background: #0414a7;
        position: fixed;
        padding: 0;
        margin: 0;
        width: 100%;
        height: 100%;
    }

    .neg {
        text-align: center;
        color: #0414a7;
    }

    .bg {
        background: #aaaaaa;
        padding: 0 15px 2px 13px;
    }

    .text-holder {
        display: table;
        margin: 0 auto;
    }
</style>