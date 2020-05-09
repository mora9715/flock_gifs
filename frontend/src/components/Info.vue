<template>
  <b-card-group deck>
    <b-card header="Project info">
      <p>Flock Gifs is an <i>open-source</i> project. </p>
      <p>Source code is available <a href="https://github.com/mora9715/flock_gifs">here</a> and <a href="https://github.com/mora9715/flock_frontend">here</a>.</p>
    </b-card>
      <b-card header="Software stack">
      <p>Frontend:</p>
      <ul>
      <li>VueJS for logic</li>
      <li>Bootsrap for HTML/CSS</li>
      </ul>
      <p>Backend:</p>
      <ul>
      <li>Django</li>
      <li>Django Rest Framework</li>
      </ul>
    </b-card>
    <b-card header="Contribute">
      <p>Should you have any suggestions, feature requests, bugs, report them to <strong>@Eugene Prodan</strong>.</p>
    </b-card>
  </b-card-group>
</template>

<script>
export default {
  name: 'Info',
  data() {
    return {
    }
  }
}
</script>

<style scoped>
.info-holder {
  padding: 10px;
  display: table;
  margin: 0 auto;
}
</style>