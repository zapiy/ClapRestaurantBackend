<script setup lang="ts">
import { userActions } from "@/defines";
import { ref, onMounted, onUnmounted } from "vue";

const actionsVisible = ref(false);

function onWindowClick() {
  if (actionsVisible.value) {
    actionsVisible.value = false;
  }
}
onMounted(() => window.addEventListener("click", onWindowClick));
onUnmounted(() => window.removeEventListener("click", onWindowClick));
</script>

<template>
  <header>
    <div class="inner">
      <div class="side">
        <div
          class="burger hoverable-icon"
          :class="{ expanded: $store.sidebarShown }"
          @:click="$store.switchSidebar()"
        >
          <div class="line"></div>
        </div>

        <div class="mark">
          <img class="logo" src="/res/logo.svg" />
          <span class="name">Restaurant</span>
        </div>
      </div>
      <div class="side" v-if="userActions">
        <mdicon
          @:click.stop="actionsVisible = !actionsVisible"
          class="hoverable-icon"
          name="dots-vertical"
          size="35"
        />

        <div
          class="actions"
          :class="{ visible: actionsVisible }"
          @:click.stop="actionsVisible = false"
        >
          <div
            v-for="action in userActions"
            :key="action.text"
            @:click="action.handle()"
            class="item"
          >
            {{ action.text }}
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style lang="scss">
header .mdi {
  position: relative;
  svg {
    fill: var(--background) !important;
  }
}
</style>

<style scoped lang="scss">
@import "@/globals/mixins.scss";

.hoverable-icon {
  position: relative;
  &:hover::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 150%;
    height: 150%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background-color: rgba(0, 0, 0, 0.2);
  }
}

header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  z-index: 50;
  height: var(--header-height);

  box-shadow: var(--shadow);

  padding: 5rem 10rem;

  background-color: var(--primary-color);
  color: var(--background);

  & > .inner {
    @include d-flex(h sb);

    .side {
      @include d-flex(h, $gap: 15rem);
    }

    .mark {
      @include d-flex(h c, $gap: 5rem);
      user-select: none;

      .logo {
        width: 35rem;
        height: 35rem;
      }

      .name {
        font-size: 20rem;
      }
    }

    .actions {
      z-index: 5;
      position: absolute;
      top: calc(100% + 5rem);
      right: 5rem;
      min-width: 200rem;
      min-height: 20rem;
      border: 2rem solid var(--primary-color);
      border-radius: 5rem;
      display: block;

      @include d-flex(v w);

      background-color: var(--background);
      color: var(--foreground);

      box-shadow: var(--shadow);

      &:not(.visible) {
        display: none;
      }

      .item {
        display: block;
        padding: 5rem;
        width: 100%;
        user-select: none;

        @include adaptive(
          (
            font-size: (
              _ 14rem,
              wide tablet 20rem,
              small middle 22rem,
            ),
          )
        );

        &:hover {
          background-color: var(--secondary);
        }
      }
    }

    .burger {
      cursor: pointer;
      position: relative;
      width: 30rem;
      height: 30rem;
      @include d-flex(c);

      transition: transform 0.3s;

      &.expanded {
        transform: rotate(180deg);

        .line {
          &::before {
            top: -10rem;
          }
          &::after {
            bottom: -10rem;
          }
        }
      }

      .line {
        display: block;
        position: relative;

        &::before {
          top: -7rem;
        }
        &::after {
          bottom: -7rem;
        }
        &::before,
        &::after {
          content: "";
          transition:
            top 0.2s,
            bottom 0.2s,
            transform 0.2s;
          transform-origin: center;

          position: absolute;
          left: 0;
        }
      }
      .line,
      .line::before,
      .line::after {
        border-radius: 4rem;
        background-color: var(--background) !important;

        @include adaptive(
          (
            width: (
              _ 25rem,
              every 35rem,
            ),
            height: (
              _ 2rem,
              every 4rem,
            ),
          )
        );
      }
    }
  }
}
</style>
