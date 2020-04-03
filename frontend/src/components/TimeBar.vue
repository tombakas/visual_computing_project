<template>
  <div class="timebar">
    <div class="playback">
      <div class="playback__icon" v-on:click="playbackCalls()">
        <svg
          data-v-fb1278fc
          xmlns="http://www.w3.org/2000/svg"
          width="24px"
          height="24px"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="icon-svg feather feather-play-circle"
          v-if="!playbackRunning"
        >
          <circle data-v-fb1278fc cx="12" cy="12" r="10" />
          <polygon data-v-fb1278fc points="10 8 16 12 10 16 10 8" />
        </svg>
        <svg
          data-v-fb1278fc
          xmlns="http://www.w3.org/2000/svg"
          width="24px"
          height="24px"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="icon-svg feather feather-stop-circle"
          v-if="playbackRunning"
        >
          <circle data-v-fb1278fc cx="12" cy="12" r="10" />
          <rect data-v-fb1278fc x="9" y="9" width="6" height="6" />
        </svg>
      </div>
      <div class="playback__progress">
        <div class="playback__progress-inner"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    playbackRunning() {
      return this.$store.getters.getPlaybackDate !== "";
    }
  },
  methods: {
    playbackCalls() {
      if (!this.playbackRunning) {
        this.$store.dispatch("getPlaybackCalls", this.$store.getters.getCalls);
      } else  {
        this.$store.dispatch('setPlayback', true);
        this.aborting = true;
      }
    }
  }
};
</script>

<style lang="scss">
@import "../scss/variables";

.timebar {
  width: calc(100% - 410px);
  position: absolute;
  right: 0;
  bottom: 0;
  height: 100px;
  background: rgba(
    $color: (
      map-get($map: $colors, $key: "black")
    ),
    $alpha: 0.4
  );
  z-index: 2;
}

.playback {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 100%;

  &__icon {
    margin-left: 30px;

    svg {
      height: 50px;
      width: 50px;
      stroke: map-get($map: $colors, $key: "black");
      transition-duration: 0.25s;

      &:hover {
        stroke: map-get($map: $colors, $key: "white");
      }
    }
  }
  &__progress {
    margin: auto 40px;
    width: 100%;
    height: 20px;
    border: 4px solid (map-get($map: $colors, $key: "black"));
    border-radius: 8px;
    overflow: hidden;

    &-inner {
      position: relative;
      width: 10px;
      height: 100%;
      background-color: map-get($map: $colors, $key: "black");
      left: -10px;
    }
  }
}
</style>