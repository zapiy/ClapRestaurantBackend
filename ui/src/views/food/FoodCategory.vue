<script setup lang="ts">
import { useRoute } from "vue-router";
import { AccentBox, ClickableContainer, PaginatorControl } from "@/components";
import useSWRV from "swrv";
import { ref, watch } from "vue";
import { fetcher, router } from "@/defines";
import { ActionButton } from "@/components/form";

const route = useRoute();

const paginate = ref(1);
const {
  data,
  error,
  mutate: reload,
} = useSWRV(`/food/of/${route.params.uuid}`, (url) =>
  fetcher(url, { p: paginate.value })
);
watch(error, (err) => {
  if (err?.code == 404) {
    router.push({ path: "/foods" });
  }
});
watch(paginate, () => reload());
</script>

<template>
  <div class="inner">
    <h1 v-if="error">Fail to receive data!</h1>
    <template v-else-if="data != null">
      <AccentBox :title="data.category.name" grid>
        <template #actions>
          <ActionButton
            text="Add Food"
            @click="
              $router.push({
                path: `/food/new`,
                query: { category: data.category.uuid },
              })
            "
          />
        </template>

        <ClickableContainer
          v-for="item in data.view"
          :key="item.uuid"
          :title="item.name"
          :image="item.image"
          @click="$router.push(`/food/${item.uuid}`)"
        />
      </AccentBox>

      <PaginatorControl
        v-model:current="paginate"
        :max="data?.paginator?.max ?? 1"
      />
    </template>
    <LoadingPreview v-else />
  </div>
</template>
