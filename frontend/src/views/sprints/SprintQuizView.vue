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

const route = useRoute();

const paginate = ref(1);
const {
	data,
	error,
	mutate: reload,
} = useSWRV(`/sprints/quiz/${route.params.uuid}/users`, (url) =>
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
			<ClickableContainer :image="data.quiz.image" />
			<AccentBox :title="data.quiz.name">
				<TableView
					:header="['User Name', 'Current Status', 'Incorrect Attempts']"
				>
					<TableViewLine
						v-for="item in data.view"
						:key="item.uuid"
						:rows="[
							item.full_name,
							{
								text: item.current_status,
								color:
									item.current_status === 'correct'
										? 'confirm'
										: item.current_status === 'incorrect'
										  ? 'cancel'
										  : 'blue',
							},
							item.incorrect_attempts,
						]"
						@click="
							$router.push(`/sprint/quiz/${$route.params.uuid}/${item.uuid}`)
						"
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
