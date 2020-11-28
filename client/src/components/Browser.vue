<template>
  <div class="input-group mb-3">
    <input
      type="text"
      class="form-control"
      placeholder="Recipient's username"
      aria-label="Recipient's username"
      aria-describedby="button-addon2"
    />
    <div class="input-group-append">
      <button
        class="btn btn-outline-secondary"
        type="button"
        id="button-addon2"
        @click="search_query()"
      >
        Search
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Browser',
  data() {
    return {
      query: ''
    }
  },
  methods: {
    async search_query() {
      const body = {
        query: this.query
      }
      axios.post('http://127.0.0.1:8081/query', body).then((response) => {
        console.log(response);
      })
    }
  }
};
</script>

<style></style>
