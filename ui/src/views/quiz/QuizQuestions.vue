<script setup lang="ts">
import { fetcher } from "@/defines";
import { prettyDate } from "@/utils";
import useSWRV from "swrv";
import { ref, watch } from "vue";
import QuizQuestionModal from "./QuizQuestionModal.vue";
import {
	AccentBox,
	LoadingPreview,
	PaginatorControl,
	TableView,
} from "@/components";
import TableViewLine from "@/components/TableViewLine.vue";
import { ActionButton } from "@/components/form";

const props = defineProps({
	uuid: {
		type: String,
		required: true,
	},
});

const paginate = ref(1);
const {
	data,
	error,
	mutate: reload,
} = useSWRV(`/quiz/${props.uuid}/questions`, (url) =>
	fetcher(url, { p: paginate.value })
);
watch(paginate, () => reload());

const selected = ref();
const add = (type) =>
	(selected.value = {
		uuid: "new",
		quiz: props.uuid,
		type: type,
	});
</script>

<template>
	<h1 v-if="error">Fail to receive question list!</h1>
	<template v-else-if="data">
		<AccentBox title="Questions">
			<template #actions>
				<ActionButton
					text="Add Question"
					:subactions="{
						text: 'Text variant',
						option: 'Option variant',
					}"
					@click="(ev) => add(ev.type)"
				/>
			</template>

			<TableView :header="['Name', 'Type', 'Created at']">
				<TableViewLine
					v-for="item in data.view"
					@click="selected = item"
					:key="item.uuid"
					:rows="[item.name, item?.type, prettyDate({ date: item.created_at })]"
				/>
			</TableView>
		</AccentBox>
		<PaginatorControl
			v-model:current="paginate"
			:max="data?.paginator?.max ?? 1"
		/>

		<template v-if="selected">
			<QuizQuestionModal
				:question="selected"
				@reload="reload"
				@close="selected = null"
			/>
		</template>
	</template>
	<LoadingPreview v-else />
</template>
