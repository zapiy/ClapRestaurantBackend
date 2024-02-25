<template>
  <div
    class="sidebar-overflow"
    :class="{ minimized: !$store.sidebarShown }"
    @:click="$store.switchSidebar()"
  >
    <aside
      class="sidebar"
      @:click="
        (ev) => ($window.screen.width >= 960 ? ev.stopPropagation() : null)
      "
    >
      <RouterLink
        v-for="route in $router.options.routes.filter(
          (el) => el.name && el.icon
        )"
        :key="route.path"
        :to="route.path"
        class="item"
      >
        <mdicon class="icon" :name="route.icon || 'view-dashboard'" />
        <span class="text">{{ route.name }}</span>
      </RouterLink>
    </aside>
  </div>
</template>

<style scoped lang="scss">
@import "@/globals/mixins.scss";

.sidebar {
  display: block;
  overflow-y: auto;
  width: 100%;
  height: 100%;
  @include d-flex(v);

  &-overflow {
    width: 15%;
    height: 100%;
    transition: width 0.3s;
    z-index: 49;
    &.minimized {
      width: 50rem;
      .item {
        align-items: center;
        justify-content: center;

        .text {
          opacity: 0;
          display: none;
        }
      }
    }
    &:not(.minimized) {
      @include respond-to(small middle tablet) {
        position: absolute;
        top: 0;
        left: 0;
        display: block;
        width: 100%;
        background-color: rgba($color: #000000, $alpha: 0.2);

        .sidebar {
          @include line-anim(0.3s forwards, "width", (0 45%));
          background-color: var(--background);
        }
      }
    }

    @include respond-to(small middle tablet) {
      display: none;
      width: 100%;
    }
  }
  @include respond-to(small middle tablet) {
    width: 0%;
  }

  .item {
    @include d-flex(h, $gap: 10rem);
    width: 100%;
    height: fit-content;
    user-select: none;
    text-wrap: nowrap;
    padding: 10rem 15rem;

    &:hover {
      background-color: var(--secondary);
    }

    &.router-link-active {
      .mdi.icon {
        width: 20rem;
      }
      .text {
        font-weight: bold;
      }
    }

    .icon {
      width: 16rem;
      transition: width 0.1s;
    }
    .text {
      @include adaptive(
        (
          font-size: (
            _ 14rem,
            small middle tablet 20rem,
          ),
        )
      );
      font-weight: 500;

      transition:
        opacity 0.3,
        0.3 display 0.3;
    }
  }
}
</style>
