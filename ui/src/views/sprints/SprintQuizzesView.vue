<script setup lang="ts">
import {
	AccentBox,
	TableView,
	TableViewLine,
	PaginatorControl,
	LoadingPreview,
} from "@/components";
import { fetcher } from "@/defines";
import { ref, watch } from "vue";
import useSWRV from "swrv";

const paginate = ref(1);
const { data, mutate: reload } = useSWRV("/sprints/quizzes", (url) =>
	fetcher(url, { p: paginate.value })
);
watch(paginate, () => reload());
</script>

<template>
	<div class="inner">
		<template v-if="data != null">
			<span>Count workers: {{ data.users_count }}</span>
			<AccentBox title="Sprints">
				<TableView
					:header="[
						'Quiz',
						'Pending Count',
						'Passed Count',
						'Currently Processing Count',
					]"
				>
					<TableViewLine
						v-for="item in data.view"
						:key="item.uuid"
						:rows="[
							item.name,
							item.pending_count,
							item.passed_count,
							item.processing_count,
						]"
						@click="$router.push(`/sprint/quiz/${item.uuid}`)"
					/>
				</TableView>
			</AccentBox>
			<PaginatorControl
				v-model:current="paginate"
				:max="data?.paginator?.max ?? 1"
			/>
		</template>
		<LoadingPreview v-else />
	</div>
</template>
