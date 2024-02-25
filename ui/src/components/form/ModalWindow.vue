<script setup lang="ts">
defineEmits(["close"]);

const props = defineProps({
  visible: {
    type: Boolean,
    required: false,
    default: false,
  },
  title: {
    type: String,
    required: false,
  },
});
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div class="modal-overflow" v-if="props.visible" @:click="$emit('close')">
        <div class="modal" @:click.stop>
          <div class="modal-header" v-if="props.title">
            <h1 class="title">{{ props.title }}</h1>
          </div>

          <div class="modal-body">
            <slot></slot>
          </div>

          <div class="modal-actions" v-if="$slots.actions">
            <slot name="actions"></slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style lang="scss" scoped>
@import "@/globals/mixins.scss";

.modal {
  min-width: 30%;
  max-width: 80%;
  min-height: 200rem;
  max-height: 90%;
  width: fit-content;
  overflow-y: auto;

  margin: 0 auto;
  padding: 20rem 30rem;
  background-color: var(--background);
  border-radius: 5rem;
  box-shadow: 0 2rem 8rem rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;

  .title {
    margin-right: 100rem;
  }

  &-actions {
    @include d-flex(h end);
    margin-top: 15rem;
  }

  &-overflow {
    position: fixed;
    z-index: 90;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    transition: opacity 0.3s ease;

    @include d-flex(v c);
  }
}

.modal-enter-active {
  opacity: 0;
  & > .modal {
    transform: scale(1.1);
  }
}
.modal-leave-active {
  opacity: 0;
  & > .modal {
    transform: scale(0.9);
  }
}
</style>
