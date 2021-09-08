<template>
  <div>
    <p>{{ name }}</p>
    <Counter :initial-count="episodes_seen" label="Episodes seen: "/>
  </div>
</template>

<script>
import Counter from "./Counter";

export default {
  components: {
    Counter,
  },
  props: ['id', 'name', 'episodes_seen']
};
</script>

<style>
</style>
