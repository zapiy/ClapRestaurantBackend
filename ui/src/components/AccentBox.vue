<script setup lang="ts">
const props = defineProps({
  title: {
    type: String,
    required: false,
  },
  grid: {
    type: Boolean,
    required: false,
    default: false,
  },
});
</script>

<template>
  <div class="accent-box" :class="{ grid }">
    <div class="header" v-if="props.title || $slots.actions">
      <h1 v-if="props.title">{{ props.title }}</h1>
      <div class="actions" v-if="$slots.center">
        <slot name="center"></slot>
      </div>
      <div class="actions" v-if="$slots.actions">
        <slot name="actions"></slot>
      </div>
    </div>

    <div class="content" v-if="$slots.default">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import "@/globals/mixins.scss";
.accent-box {
  margin: 5rem 0;
  overflow: visible;

  & > .header {
    margin: 5rem;
    user-select: none;
    width: 100%;
    @include d-flex(h sb);

    .actions {
      @include d-flex(h c, $gap: 5rem);
      justify-self: flex-end;
    }
  }
  & > .content {
    padding: 10rem;
    margin: 5rem auto;
    min-width: 100rem;
    min-height: 100rem;
    width: fit-content;
    max-width: 100%;
    overflow-x: auto;
    overflow-y: visible;

    background-color: var(--background);
    box-shadow: var(--shadow);

    border-radius: 10rem;
  }

  &.grid > .content {
    @include d-flex(h wp);
  }
}
</style>
