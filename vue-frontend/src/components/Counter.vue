<template>
  <div>
    <p>{{ label }}{{ count }}</p>
    <button class="btn" @click="count > 0 ? --count : count">🔽</button>
    <button class="btn" @click="++count">🔼</button>
  </div>
</template>

<script>
export default {
  props: {
    initialCount: {
      default: 0
    },
    label: {
      default: "I'm a Counter! "
    }
  },
  data() {
    return {
      count: this.initialCount
    }
  }
};
</script>

<style>
</style>

