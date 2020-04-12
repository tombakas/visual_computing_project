<template>
  <div class="chartHolder">
    <div id="goBack" v-on:click="handleGoBack">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 483.96021">
        <path d="m 241.48011,482.75312 v -110.352 h 202.91158 v -258.328 H 241.48011 V 1.2071167 L 0.70710995,241.98412 Z" id="arrowPolygon" />
      </svg>
    </div>
    <canvas id="barChart">
    </canvas>
  </div>
</template>

<script>
import { getCounts, handleGoBack, prevStack} from './graphDefinitions.js'

export default {
  mounted () {
    getCounts("http://localhost:5000/api/calls/count?interval=year", "Yearly all data point breakdown")
  },
  methods: {
    handleGoBack: () => {
      handleGoBack()
    }
  }
}
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";

.chartHolder {
  display: flex;
  flex-direction: column;
  align-self: center;
  width: 100%;
  height: 800px;
  justify-content: space-around;
  margin: 0 50px;
}

#goBack {
  position: absolute;
  left: 440px;
  top: 28px;
  height: 60px;
  width: 60px;

  #arrowPolygon {
    fill: #bfd9f0;
    stroke: #97b5ee;
    stroke-width: 12px;
    opacity: 0.5;
    &:hover {
      opacity: 0.8;
      cursor: pointer;
    }
  }
}

#barChart {
  align-self: center;
  border: 3px solid #999;
  padding: 25px;
  max-width: 80%;
}
</style>
