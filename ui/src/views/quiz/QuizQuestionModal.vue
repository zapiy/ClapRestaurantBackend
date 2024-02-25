<script setup lang="ts">
import { ClickableContainer } from "@/components";
import { ActionButton, InputField, ModalWindow } from "@/components/form";
import { store, pusher } from "@/defines";
import { reactiveForm, selectFile } from "@/utils";
const emit = defineEmits(["close", "reload"]);
const props = defineProps({
	question: {
		type: Object,
		required: true,
	},
});

const formFields = {
	image: {
		preview: (val) => URL.createObjectURL(val),
	},
	name: {
		required: true,
		validate: (val) => val.length <= 100,
	},
	description: {
		validate: (val) => val.length <= 1000,
	},
};

if (props.question?.type === "option") {
	Object.assign(formFields, {
		answers: {
			required: true,
			prepare: (val) => {
				if (!val || val.length == 0) {
					form.correct_answer = null;
					return null;
				}

				const values = Array.from(val.values()).map((ans) => ans.toTitleCase());
				if (form.correct_answer && !values.includes(form.correct_answer)) {
					form.correct_answer = null;
				}
				return values;
			},
			validate: (val) => val.length <= 100,
		},
		correct_answer: {
			required: true,
		},
	});
}

const { form, formValid, formEditing, formNewest, generatePostForm } =
	reactiveForm({
		isNew: props.question?.uuid == "new",
		fields: formFields,
		defaults: props.question,
	});

async function submit() {
	const generated: FormData = generatePostForm();
	if (!generated) {
		store.notify("Form is not valid");
		return;
	}
	if (formNewest) {
		generated.set("type", props.question?.type);
		generated.set("quiz", props.question?.quiz);
	}

	const resp = await pusher(`/quiz/question/${props.question.uuid}`, {
		data: generated,
	});
	if (resp.status != 200) {
		store.notify("Error on server side, try later!!!");
		return;
	}
	emit("reload");
	emit("close");
}

async function selectImage() {
	if (!formEditing.value) return;
	const image = await selectFile(["jpg", "jpeg", "png"]);
	form.image = image;
}

async function remove() {
	const resp = await pusher(`/quiz/question/${props.question.uuid}`, {
		method: "DELETE",
		data: {
			uuid: props.question.uuid,
		},
	});
	if (resp.status != 200) {
		store.notify("Error on server side validation! Check and try later.");
		return;
	}
	emit("close");
	emit("reload");
	store.notify("Success remove!");
}
</script>

<template>
	<ModalWindow :title="form?.name" @close="$emit('close')" visible>
		<ClickableContainer
			:image="form.image"
			:title="form.image ? null : 'Image'"
			@click="() => (formEditing ? selectImage() : null)"
		/>
		<template v-if="formEditing">
			<InputField placeholder="Name" v-model:value="form.name" size="fw" />

			<InputField
				placeholder="Description"
				type="multiline"
				v-model:value="form.description"
				size="fw"
			/>

			<template v-if="form.type == 'option'">
				<InputField
					placeholder="Answers"
					type="tags"
					v-model:value="form.answers"
					size="fw"
				/>
				<template v-if="form.answers">
					<h2>Correct answer</h2>
					<div d-flex="h wp">
						<ClickableContainer
							v-for="ans in form.answers"
							:key="ans"
							:title="ans"
							:checked="form.correct_answer == ans"
							@click="form.correct_answer = ans"
						/>
					</div>
				</template>
			</template>
		</template>
		<template v-else>
			<template v-if="form.description">
				<h2>Description</h2>
				<span>{{ form.description }}</span>
			</template>
			<template
				v-if="form.type == 'option' && form.answers && form.answers.length > 0"
			>
				<h2>Options</h2>
				<div d-flex="h wp">
					<ClickableContainer
						v-for="ans in form.answers"
						:key="ans.uuid"
						:title="ans.name"
					/>
				</div>
				<h2>Correct Answer</h2>
				<ClickableContainer :title="form?.correct_answer?.name" />
			</template>
		</template>

		<template #actions>
			<ActionButton
				text="Cancel"
				@click="
					formEditing && !formNewest ? (formEditing = false) : $emit('close')
				"
			/>
			<ActionButton
				v-if="formNewest || formEditing"
				text="Save"
				color="confirm"
				@click="submit"
				:disabled="!formValid"
			/>
			<ActionButton
				v-else-if="!formEditing"
				text="Delete"
				color="cancel"
				@click="remove"
			/>
			<!-- <ActionButton
        v-if="!formNewest && !formEditing"
        text="Edit"
        color="gold"
        @click="formEditing = true"
      /> -->
		</template>
	</ModalWindow>
</template>
