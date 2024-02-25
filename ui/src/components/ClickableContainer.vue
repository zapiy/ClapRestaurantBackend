<script setup lang="ts">
defineEmits(["click"]);
const props = defineProps({
  image: {
    type: String,
    required: false,
  },
  title: {
    type: String,
    required: false,
  },
  mdi: {
    type: Boolean,
    required: false,
    default: false,
  },
  checked: {
    type: Boolean,
    required: false,
  },
});
</script>

<template>
  <button
    class="titled-image"
    @click.prevent="$emit('click')"
    :class="{ checked }"
  >
    <template v-if="props.image">
      <mdicon v-if="mdi" class="img" :name="props.image" />
      <img v-else class="img" :src="props.image" />
    </template>
    <span class="title" v-if="props.title">{{ props.title }}</span>
  </button>
</template>

<style lang="scss" scoped>
@import "@/globals/mixins.scss";
.titled-image {
  @include d-flex(v);
  max-width: 200rem;
  width: fit-content;
  overflow: hidden;

  box-shadow: var(--shadow);
  transition: box-shadow 0.5s;
  padding: 10rem;
  border-radius: 10rem;
  margin: 10rem;

  &:active,
  &.checked {
    box-shadow: var(--rev-shadow);
  }

  .img {
    min-width: 150rem;
    max-width: 100%;
    min-height: 150rem;
    max-height: 250rem;
    border-radius: 10rem;
    object-fit: cover;
  }
  .title {
    max-width: 100%;
  }
}
</style>
