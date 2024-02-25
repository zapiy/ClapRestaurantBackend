<script setup lang="ts">
import {
  AccentBox,
  PaginatorControl,
  LoadingPreview,
  ClickableContainer,
} from "@/components";
import { ActionButton } from "@/components/form";
import { fetcher } from "@/defines";
import useSWRV from "swrv";
import { ref, watch } from "vue";

const paginate = ref(1);
const {
  data,
  error,
  mutate: reload,
} = useSWRV("/quizzes", (url) => fetcher(url, { p: paginate.value }));
watch(paginate, () => reload());
</script>

<template>
  <div class="inner">
    <h1 v-if="error">Fail to receive data!</h1>

    <template v-else-if="data != null">
      <AccentBox title="Trainigs" grid>
        <template #actions>
          <ActionButton
            text="Add training"
            @click="$router.push(`/quiz/new`)"
          />
        </template>

        <ClickableContainer
          v-for="item in data.view"
          :key="item.uuid"
          :title="item.name"
          :image="item.image"
          @click="$router.push(`/quiz/${item.uuid}`)"
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
