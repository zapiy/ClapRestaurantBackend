<script lang="ts" setup>
const props = defineProps({
  header: {
    type: Array<string>,
    required: true,
  },
});
</script>

<template>
  <table>
    <thead>
      <tr>
        <th v-for="title in props.header" :key="title">{{ title }}</th>
      </tr>
    </thead>
    <tbody>
      <slot></slot>
    </tbody>
  </table>
</template>

<style scoped lang="scss">
table {
  border-spacing: 1;
  border-collapse: collapse;
  background: var(--background);
  position: relative;
  user-select: none;
  z-index: 0;

  width: fit-content;
  border-radius: 10rem;
  overflow: hidden;

  thead {
    background-color: var(--primary-color);
    th {
      padding: 4rem 20rem;
      color: var(--background);
      text-align: center;
      white-space: nowrap;
    }
  }
}
</style>
