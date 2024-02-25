<template>
  <div class="loading-view">
    <div class="spinner">
      <div class="circle"></div>
      <div class="circle"></div>
    </div>

    <h1 class="info-text">Loading please wait...</h1>
  </div>
</template>

<style scoped lang="scss">
@import "@/globals/mixins.scss";

.loading-view {
  width: 100%;
  @include d-flex(v c);
  padding: 50rem;

  .info-text {
    margin: 20rem 0;
    font-size: 30rem;
  }
}

.spinner {
  width: 100rem;
  height: 100rem;
  border-radius: 100%;
  position: relative;

  * {
    box-sizing: border-box;
  }
  .circle {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 100%;
    border: calc(100rem / 10) solid transparent;

    &:nth-child(1) {
      border-top-color: var(--primary-color);
      animation: spinner-animation 1s infinite;
    }
    &:nth-child(2) {
      border-bottom-color: var(--primary-color);
      animation: spinner-animation 1s infinite alternate;
    }
  }
}

@keyframes spinner-animation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
