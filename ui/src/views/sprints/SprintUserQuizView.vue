<script setup lang="ts">
import {
	AccentBox,
	TableView,
	TableViewLine,
	PaginatorControl,
	LoadingPreview,
	ClickableContainer,
} from "@/components";
import { fetcher, router } from "@/defines";
import { ref, watch } from "vue";
import useSWRV from "swrv";
import { useRoute } from "vue-router";
import { prettyDate } from "@/utils";

const route = useRoute();

const paginate = ref(1);
const {
	data,
	error,
	mutate: reload,
} = useSWRV(`/sprints/quiz/${route.params.quiz}/${route.params.user}`, (url) =>
	fetcher(url, { p: paginate.value })
);
watch(paginate, () => reload());

watch(error, (err) => {
	if (err?.code == 404) {
		router.push({ path: "/sprints" });
	}
});
</script>

<template>
	<div class="inner">
		<template v-if="data != null">
			<div d-flex="h">
				<ClickableContainer :image="data.quiz.image" />
				<ClickableContainer :image="data.user.avatar" />
			</div>
			<AccentBox
				:title="
					'Sprints quiz - ' +
					data.quiz.name +
					' (by ' +
					data.user.full_name +
					')'
				"
			>
				<TableView :header="['Status', 'Started At', 'Finished At']">
					<TableViewLine
						v-for="item in data.view"
						:key="item.uuid"
						:rows="[
							{
								text: item.status,
								color:
									item.status === 'correct'
										? 'confirm'
										: item.status === 'incorrect'
										  ? 'cancel'
										  : 'blue',
							},
							prettyDate(item.created_at),
							prettyDate(item.finished_at),
						]"
						@click="$router.push(`/sprint/${item.uuid}`)"
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
