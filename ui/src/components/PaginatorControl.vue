<script setup lang="ts">
import { nextTick, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { routerSetQuery } from "@/defines";

const emit = defineEmits(["update:current"]);
const route = useRoute();

const props = defineProps({
  current: {
    type: Number,
    required: false,
    default: null,
  },
  max: {
    type: Number,
    required: false,
    default: 1,
  },
});

const current = ref(1);
if (props.current == null || props.current == undefined) {
  nextTick(() => {
    const queryParam: number = route.query.p ?? 1;
    current.value = queryParam < 1 && queryParam > props.max ? 1 : queryParam;
    routerSetQuery("p", current.value);
    emit("update:current", current.value);
  });
}

watch(current, () => {
  routerSetQuery("p", current.value);
  emit("update:current", current.value);
});
</script>

<template>
  <div class="paginator">
    <button v-if="current > 1" class="switch arrow" @click="current--">
      <mdicon class="icon" name="chevron-left" />
    </button>
    <div class="switch numbers">
      <template v-if="max < 8">
        <button
          v-for="i in max"
          :key="i"
          class="item"
          :class="{ current: current == i }"
          @click="current = i"
        >
          {{ i }}
        </button>
      </template>
      <template v-else>
        <button
          class="item"
          v-for="i in current <= 2 ? 3 : 1"
          :key="i"
          :class="{ current: current == i }"
          @click="current = i"
        >
          {{ i }}
        </button>

        <template v-if="2 < current && current < max - 1">
          <button v-if="current > 3" class="item" disabled>…</button>
          <button class="item" @click="current--">
            {{ current - 1 }}
          </button>
          <button class="item current">
            {{ current }}
          </button>
          <button class="item" @click="current++">
            {{ current + 1 }}
          </button>
          <button v-if="current < max - 2" class="item" disabled>…</button>
        </template>
        <button v-else class="item" disabled>…</button>

        <button
          class="item"
          v-for="i in max - 2 < current ? 3 : 1"
          :key="i"
          :class="{ current: max - 2 < current && current == max - 3 + i }"
          @click="current = max - 2 < current ? max - 3 + i : max"
        >
          {{ max - 2 < current ? max - 3 + i : max }}
        </button>
      </template>
    </div>
    <button v-if="current < props.max" class="switch arrow" @click="current++">
      <mdicon class="icon" name="chevron-right" />
    </button>
  </div>
</template>

<style scoped lang="scss">
@import "@/globals/mixins.scss";
.paginator {
  @include d-flex(h);
  margin-left: auto;
  width: fit-content;
  margin: 10rem auto;

  & > .switch {
    box-shadow: var(--shadow);
    user-select: none;

    &.numbers {
      @include d-flex(h);
      border-radius: 18rem;
      margin: 0 10rem;
      overflow: hidden;

      & > .item {
        padding: 8rem 20rem;
        font-weight: 500;

        &:not(.current):not(:disabled):active {
          box-shadow: var(--rev-shadow);
        }
        &.current {
          background-color: var(--primary-color);
          color: var(--background);
        }
      }
    }
    &.arrow {
      width: 40rem;
      height: 40rem;
      border-radius: 50%;

      &:active {
        box-shadow: var(--rev-shadow);
      }
    }

    @include respond-to(small middle) {
      &.numbers > .item {
        padding: 4rem 15rem;
        font-size: 14rem;
      }
      &.arrow {
        width: 30rem;
        height: 30rem;
      }
    }
  }
}
</style>
