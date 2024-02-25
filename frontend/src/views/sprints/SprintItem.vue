<script setup lang="ts">
import {
	AccentBox,
	TableView,
	TableViewLine,
	PaginatorControl,
	LoadingPreview,
	ClickableContainer,
} from "@/components";
import { fetcher, pusher, store } from "@/defines";
import { ref, watch } from "vue";
import useSWRV from "swrv";
import { useRoute } from "vue-router";
import { ActionButton, InfoView, ModalWindow } from "@/components/form";

const route = useRoute();
const selectedAnswer = ref(null);

const verifyCheck = async (valid: boolean) => {
	const resp = await pusher(
		`/sprint/answer/${selectedAnswer.value?.uuid}/verify`,
		{
			data: {
				valid: valid,
			},
		}
	);
	if (resp.status != 200) {
		store.notify("Error on server side, try later!!!");
		return;
	}
	selectedAnswer.value = null;
	await reload();
};

const paginate = ref(1);
const { data, mutate: reload } = useSWRV(
	`/sprint/${route.params.uuid}/answers`,
	(url) => fetcher(url, { p: paginate.value })
);
watch(paginate, () => reload());
</script>

<template>
	<div class="inner">
		<template v-if="data != null">
			<div d-flex="h">
				<ClickableContainer :image="data.sprint.quiz_image" />
				<ClickableContainer :image="data.sprint.user_image" />
			</div>
			<div d-flex="h" v-if="data.sprint.status == 'while_taking'">
				<mdicon name="progress-clock" />
				<span
					>Sprint is currently closed because the user has not finished testing
					yet</span
				>
			</div>
			<div d-flex="h" v-else-if="data.sprint.status == 'incorrect'">
				<mdicon name="close" />
				<span>Sprint closed as unsolved.</span>
			</div>
			<div d-flex="h" v-else-if="data.sprint.status == 'correct'">
				<mdicon name="check" />
				<span>Sprint closed as solved</span>
			</div>
			<AccentBox :title="data.sprint.quiz + ' (by ' + data.sprint.user + ')'">
				<TableView :header="['Name', 'Type', 'Status']">
					<TableViewLine
						v-for="item in data.view"
						@click="selectedAnswer = item"
						:key="item.uuid"
						:rows="[
							item.question.name,
							item.question.type,
							{
								text: item.status,
								color:
									item.status === 'correct'
										? 'confirm'
										: item.status === 'incorrect'
										  ? 'cancel'
										  : 'blue',
							},
						]"
					/>
				</TableView>
			</AccentBox>
			<PaginatorControl
				v-model:current="paginate"
				:max="data?.paginator?.max ?? 1"
			/>

			<ModalWindow
				:visible="selectedAnswer != null"
				@close="selectedAnswer = null"
				:title="selectedAnswer?.question?.name"
			>
				<ClickableContainer
					v-if="selectedAnswer?.question.image"
					:image="selectedAnswer?.question.image"
				/>

				<InfoView
					:items="{
						Status: selectedAnswer?.status,
					}"
				/>

				<template v-if="selectedAnswer?.question.description">
					<h1>Description</h1>
					<span>{{ selectedAnswer?.question.description }}</span>
				</template>

				<template v-if="selectedAnswer?.question.type == 'text'">
					<h1>User Answer</h1>
					<span>{{ selectedAnswer?.text_answer }}</span>
				</template>
				<template v-else>
					<h1>Answers</h1>
					<div d-flex="h wp">
						<ClickableContainer
							v-for="ans in selectedAnswer.question.answers"
							:key="ans.uuid"
							:title="ans.name"
						/>
					</div>
					<h1>Correct Answer</h1>
					<ClickableContainer
						:title="selectedAnswer.question.correct_answer.name"
					/>
					<h1>User Answer</h1>
					<ClickableContainer :title="selectedAnswer.option_answer.name" />
				</template>

				<template #actions>
					<template
						v-if="
							data.sprint.status == 'on_verification' &&
							selectedAnswer.status == 'on_verification'
						"
					>
						<ActionButton
							text="Cancel"
							size="ex"
							color="cancel"
							@click="selectedAnswer = null"
						/>
						<ActionButton
							text="Incorrect"
							size="ex"
							color="cancel"
							@click="verifyCheck(false)"
						/>
						<ActionButton
							text="Correct"
							size="ex"
							color="confirm"
							@click="verifyCheck(true)"
						/>
					</template>
					<ActionButton
						v-else
						text="Close"
						size="ex"
						color="cancel"
						@click="selectedAnswer = null"
					/>
				</template>
			</ModalWindow>
		</template>
		<LoadingPreview v-else />
	</div>
</template>
