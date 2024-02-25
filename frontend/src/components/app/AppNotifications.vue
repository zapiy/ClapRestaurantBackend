<template>
  <div class="notification-list">
    <div
      v-for="notif in $store.notifications"
      :key="notif.id"
      class="notification"
      @click.stop="notif.stop()"
    >
      <span>{{ notif.text }}</span>
      <div class="progress" :style="{ width: notif.progress + '%' }"></div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import "@/globals/mixins.scss";

.notification-list {
  position: fixed;
  z-index: 95;
  bottom: 20rem;
  right: 20rem;

  width: fit-content;
  max-height: 70%;
  @include d-flex(v wp e, $gap: 10rem);
  @include adaptive(
    (
      max-width: (
        small middle 80%,
        tablet wide 70%,
        every-x 45%,
      ),
    )
  );

  .notification {
    position: relative;
    font-size: 18rem;
    padding: 5rem 15rem;
    background-color: var(--background);
    box-shadow: var(--shadow);
    border-radius: 10rem;
    user-select: none;
    overflow: hidden;
    min-width: 200rem;

    .progress {
      background-color: var(--primary-color);
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 2rem;
    }
  }
}
</style>
