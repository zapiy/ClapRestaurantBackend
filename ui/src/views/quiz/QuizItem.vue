<script setup lang="ts">
import { AccentBox, ClickableContainer, LoadingPreview } from "@/components";
import { RichTextEditor, InputField } from "@/components/form";
import { ActionButton } from "@/components/form";
import { fetcher, pusher, router } from "@/defines";
import { store } from "@/defines";
import { selectFile, reactiveForm } from "@/utils";
import useSWRV from "swrv";
import { watch } from "vue";
import { useRoute } from "vue-router";
import QuizQuestions from "./QuizQuestions.vue";

const route = useRoute();

const { data: item, error } = useSWRV(`/quiz/${route.params.uuid}`, fetcher);
const {
	form,
	formValid,
	formEditing,
	formNewest,
	submitForm,
	generatePostForm,
} = reactiveForm({
	isNew: route.params.uuid === "new",
	fields: {
		image: {
			preview: (val) => URL.createObjectURL(val),
		},
		name: {
			required: true,
			validate: (val) => val.length <= 100,
		},
		newbie_required: {
			required: false,
			default: false,
			submit: (val) => (val ? "true" : "false"),
		},
		passing_percentage: {
			required: true,
			validate: (val) => 0 <= val && val <= 100,
		},
		content: {
			required: false,
			preview: (val) => val.ops,
			submit: (val: any, form: FormData) => {
				Object.values(val.attachments).forEach((file) =>
					form.append("attachments", file)
				);
				return val.ops;
			},
		},
	},
	defaults: item,
});
watch(error, (err) => {
	if (err?.code == 404) {
		router.push({ path: "/quizzes" });
	}
});

const selectImage = async () => {
	if (!formEditing.value) return;
	const image = await selectFile(["jpg", "jpeg", "png"]);
	form.image = image;
};

async function submit() {
	const generated: FormData = generatePostForm();
	if (!generated) {
		store.notify("Form is not valid");
		return;
	}

	store.isProcessing = true;
	try {
		const resp = await pusher(`/quiz/${route.params.uuid}`, {
			data: generated,
		});
		if (resp.status != 200) {
			store.notify("Error on server side, try later!!!");
			return;
		}
		item.value = await resp.json();
		if (route.params.uuid == "new") {
			router.push(`/quiz/${item.value.uuid}`);
		}
		submitForm(item.value);
	} finally {
		store.isProcessing = false;
	}
}

const remove = () =>
	store.showDialog({
		title: "Delete",
		text: "Are you sure you want to delete?",
		handle: async function () {
			const resp = await pusher(`/quiz/${route.params.uuid}`, {
				method: "DELETE",
				data: {
					uuid: route.params.uuid,
				},
			});
			if (resp.status != 200) {
				store.notify("Error on server side, try later!!!");
				return false;
			}
			router.push({ path: "/quizzes" });
			return true;
		},
	});
</script>

<template>
	<div class="inner">
		<h1 v-if="error">Fail to receive data!</h1>
		<template v-else-if="form != null">
			<ClickableContainer :image="form.image" @click="selectImage" />
			<div v-if="formEditing" d-flex="h">
				<InputField
					placeholder="Required for newbies"
					v-model:value="form.newbie_required"
					type="checkbox"
				/>
				<InputField
					placeholder="Quiz passing percentage"
					type="number"
					v-model:value="form.passing_percentage"
				/>
			</div>
			<template v-else>
				<div v-if="form.newbie_required" d-flex="h">
					<mdicon name="check" />
					<span>Required for newbies</span>
				</div>
				<span>Quiz passing percentage: {{ form.passing_percentage }}%</span>
			</template>
			<AccentBox :title="formEditing ? null : form.name">
				<template #actions>
					<InputField
						v-if="formEditing"
						placeholder="Name"
						v-model:value="form.name"
					/>

					<ActionButton
						@click="() => (formEditing ? submit() : (formEditing = true))"
						:text="formNewest ? 'Add' : formEditing ? 'Save' : 'Edit'"
						:disabled="formEditing && !formValid"
					/>
					<ActionButton
						text="Cancel"
						v-if="formEditing && !formNewest"
						color="cancel"
						@click="formEditing = false"
					/>
					<ActionButton
						text="Delete"
						v-else-if="!formNewest"
						color="cancel"
						@click="remove"
					/>
				</template>

				<RichTextEditor
					v-model:content="form.content"
					:placeholder="formEditing ? 'Write something...' : 'Content is empty'"
					:readOnly="!formEditing"
				/>
			</AccentBox>
			<template v-if="!formEditing && item">
				<QuizQuestions :uuid="item.uuid" />
			</template>
		</template>
		<LoadingPreview v-else />
	</div>
</template>
