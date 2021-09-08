<template>
  <div>
    <Instructions
      :complete="true"
    />
    <h5>Add a show</h5>
    <label for="newShowNameInput">Name:</label>
    <input id="newShowNameInput"
           type="text"
           placeholder="e.g. Breaking Bad"
           v-model="showNameInput"
    />
    <button type="button"
            @click="addShow(showNameInput); showNameInput = '';"
    >
      Create
    </button>
    <Show
      v-for="show in shows"
      :key="show.id"
      :id="show.id"
      :name="show.name"
      :episodes_seen="show.episodes_seen"
    />
  </div>
</template>

<script>
import Instructions from "./Instructions.vue";
import Show from "./Show.vue";

export default {
  components: {
    Instructions,
    Show
  },
  data() {
    return {
      showNameInput: '',
      shows: [
        { id: 1, name: "Game of Thrones", episodes_seen: 0 },
        { id: 2, name: "Naruto", episodes_seen: 220 },
        { id: 3, name: "Black Mirror", episodes_seen: 3 }
      ]
    };
  },
  methods: {
    addShow: function (showName) {
      const nextId = Math.max(...this.shows.map(s => s.id)) + 1;
      this.shows.push({
        id: nextId,
        name: showName,
        episodes_seen: 0,
      })
    }
  }
};
</script>

<style>
</style>


