<script setup lang="ts">
const props = defineProps({
  items: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <div class="info-view">
    <div
      class="line"
      v-for="[key, value] in Object.entries(props.items)"
      :key="key"
    >
      <div class="key">{{ key }}</div>
      <div class="value">{{ value }}</div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/globals/mixins.scss";

.info-view {
  @include d-flex(v w, $gap: 10rem);
  & > .line {
    @include d-flex(h, $gap: 10rem);

    & > .key {
      user-select: none;
      box-shadow: var(--rev-shadow);
      font-weight: 500;
      border-radius: 5rem;
      padding: 2rem 5rem;
    }
  }
}
</style>
