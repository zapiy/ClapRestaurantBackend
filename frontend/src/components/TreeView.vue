<script lang="ts" setup>
import { defineProps, ref, useSlots, defineEmits } from "vue";

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  image: {
    type: String,
    required: false,
  },
});
const expanded = ref(false);
const slots = useSlots();
const emit = defineEmits(["click"]);

function onClick() {
  if (slots.default) {
    expanded.value = !expanded.value;
  }
  emit("click");
}
</script>

<template>
  <div class="tree-view" :class="{ 'has-child': $slots.default, expanded }">
    <div class="header" @:click="onClick">
      <div class="side">
        <img class="image" v-bind:src="props.image" />

        <span class="title">{{ props.title }}</span>
      </div>
      <div class="actions" v-if="$slots.actions">
        <slot name="actions"></slot>
      </div>
      <mdicon v-if="$slots.default" class="switch" name="chevron-left" />
    </div>
    <div class="child" v-if="expanded && $slots.default">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import "@/globals/mixins.scss";
.tree-view {
  margin: 10rem;

  & > .header {
    font-size: 20rem;
    min-width: 400rem;
    user-select: none;
    width: fit-content;
    @include d-flex(h sb);

    .image {
      height: 50rem;
      max-width: 100rem;
      padding: 4rem;
      border-radius: 10rem;
    }

    & > .side {
      @include d-flex(h);
    }

    & > .actions {
      @include d-flex(h);

      margin: 0 50rem;
    }
  }
  & > .child {
    padding-left: 10rem;
  }

  &.has-child {
    & > .header {
      border-bottom: 2rem solid var(--foreground);
      & > .switch {
        transition: transform 0.2s;
        width: 40rem;
        height: 40rem;
      }
    }
  }

  &.expanded {
    .header .switch {
      transform: rotate(-90deg);
    }
  }
}
</style>
