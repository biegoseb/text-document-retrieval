<template>
  <div>
    <h1 style="color: #2d2d2d; font-family: 'Teko', sans-serif">
      Inverted Index Text Retrieval Search Engine
    </h1>
    <br />
    <img
      alt="Vue logo"
      src="./assets/twitter-logo.png"
      height="125"
      width="220"
      class="mb-5"
    />
    <div class="container">
      <Browser />
    </div>
  </div>
</template>

<script>
import Browser from "./components/Browser.vue";
export default {
  name: "App",
  components: {
    Browser,
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Teko:wght@500&display=swap");
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>