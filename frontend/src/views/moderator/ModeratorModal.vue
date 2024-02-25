<script setup lang="ts">
import {
	ActionButton,
	InputField,
	ModalWindow,
	InfoView,
} from "@/components/form";
import { store, pusher } from "@/defines";
import { reactiveForm, prettyDate, copyToClipboard } from "@/utils";
const emit = defineEmits(["close", "reload"]);
const props = defineProps({
	item: {
		type: Object,
		required: true,
	},
});

const {
	form,
	formValid,
	formEditing,
	formNewest,
	submitForm,
	generatePostForm,
} = reactiveForm({
	isNew: props.item?.uuid == "new",
	fields: {
		key_name: {
			required: true,
			validate: (val) => val.length <= 50,
		},
	},
	defaults: props.item,
});

async function submit() {
	const generated: FormData = generatePostForm();

	const resp = await pusher(`/moderator/${props.item.uuid}`, {
		data: generated,
	});
	if (resp.status != 200) {
		store.notify("Error on server side, try later!!!");
		return;
	}
	emit("reload");
	const value = await resp.json();
	Object.assign(props.item, value);
	submitForm(value);
}

async function remove() {
	const resp = await pusher(`/moderator/${props.item.uuid}`, {
		method: "DELETE",
		data: {
			uuid: props.item.uuid,
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

const generateLink = () =>
	location.origin + "/admin/@/" + props.item.auth_token;

async function copyLink() {
	await copyToClipboard(generateLink());
	store.notify("Link was copied to clipboard!");
}
async function shareLink() {
	navigator
		.share({
			title: "Clap Academy Authorization",
			url: generateLink(),
		})
		.then(() => console.log("Successful share!"))
		.catch((err) => console.error(err));
}
</script>

<template>
	<ModalWindow :title="form?.key_name" @close="$emit('close')" visible>
		<template v-if="formEditing">
			<InputField
				placeholder="Key identifier"
				v-model:value="form.key_name"
				size="fw"
			/>
		</template>
		<template v-else>
			<InfoView
				:items="{
					'Created at': prettyDate(item?.created_at),
				}"
			/>
			<ActionButton text="Copy auth link" color="confirm" @click="copyLink" />
			<ActionButton text="Share auth link" color="blue" @click="shareLink" />
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
			<template v-else-if="!formEditing">
				<ActionButton text="Delete" color="cancel" @click="remove" />
				<ActionButton text="Edit" color="gold" @click="formEditing = true" />
			</template>
		</template>
	</ModalWindow>
</template>
