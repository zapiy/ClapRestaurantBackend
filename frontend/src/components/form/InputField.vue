<script setup lang="ts">
import { useUUID } from "@/utils";
import { onMounted, reactive, ref, watch } from "vue";

const emit = defineEmits(["update:value"]);
const props = defineProps({
	name: {
		type: String,
		required: false,
	},
	placeholder: {
		type: String,
		required: true,
	},
	required: {
		type: Boolean,
		required: false,
	},
	value: {
		type: [String, Number, Array<String>, Boolean],
		required: false,
	},
	size: {
		type: String,
		default: "normal",
		validator: (value: string) => ["normal", "fw", "mw"].includes(value),
	},
	type: {
		type: String,
		default: "text",
		validator: (value: string) =>
			[
				"text",
				"phone",
				"number",
				"email",
				"password",
				"image",
				"file",
				"multiline",
				"checkbox",
				"tags",
			].includes(value),
	},
});

const input = ref();
const tags = props.type == "tags" ? reactive([]) : null;
const uuid = useUUID("input-field");
const current = ref("");

watch(current, (value) => {
	if (props.type !== "tags") {
		if (props.type === "number") {
			value = new Number(value);
		} else if (value === "") {
			value = null;
		}
		emit("update:value", value);
	}
});

if (props.type === "tags") {
	if (props.value) {
		tags.push(...props.value);
	}

	onMounted(() => {
		input.value.tags = tags;
	});
} else if (!["file", "image"].includes(props.type)) {
	const applyExternal = () => {
		if (props.type === "checkbox") {
			current.value = props.value ?? false;
		} else {
			current.value = props.value?.toString()?.trim() ?? "";
		}
	};

	applyExternal();

	watch(() => props.value, applyExternal);
}

const handleInputEnter = (ev) => {
	const value = current.value.trim();
	if (!value) return;

	if (props.type == "tags") {
		ev.preventDefault();
		ev.stopPropagation();

		if (!tags?.includes(value)) {
			tags?.push(value);
		}

		current.value = "";
		emit("update:value", tags);
	}
};

const onPickImage = (ev) => {
	if (ev.target.files) {
		const file = ev.target.files[0];

		if (file) {
			if (file.name.match(/\.(jpg|jpeg|png)$/)) {
				const preview = ev.target.closest(".field").querySelector(".preview");
				preview.src = URL.createObjectURL(file);
				preview.classList.remove("hidden");
				emit("update:value", file);
			} else {
				ev.target.value = "";
				alert("Unsupported file");
			}
		}
	}
};
</script>

<template>
	<div class="group" :class="['size-' + props.size, props.type]">
		<template v-if="type == 'image'">
			<div
				class="field picker"
				@click.stop.prevent="
					(ev) => ev.target.closest('.field').querySelector('input').click()
				"
			>
				<img
					class="preview"
					:class="{ hidden: !props.value }"
					:src="props.value"
				/>
				<input
					type="file"
					:name="props.name"
					:required="props.required"
					:value="props.value?.toString()"
					ref="input"
					accept="image/png, image/jpeg"
					@change="onPickImage"
					@click.stop
					hidden
				/>
				<span class="placeholder">{{ props.placeholder }}</span>
			</div>
		</template>
		<template v-else-if="type == 'checkbox'">
			<input
				class="checkbox"
				ref="input"
				:id="uuid"
				type="checkbox"
				:name="props.name"
				:required="props.required"
				v-model="current"
				@click.stop
			/>
			<label :for="uuid" class="placeholder">{{ props.placeholder }}</label>
		</template>
		<template v-else>
			<textarea
				class="field multiline"
				v-if="props.type == 'multiline'"
				:id="uuid"
				:name="props.name"
				:required="props.required"
				ref="input"
				v-model.trim="current"
				@input.stop.prevent
				autocomplete="off"
			></textarea>
			<input
				v-else
				class="field"
				:type="props.type"
				:placeholder="props.placeholder"
				:id="uuid"
				ref="input"
				:name="props.name"
				v-model.trim="current"
				:required="props.required"
				@keydown.enter="handleInputEnter"
				@input.stop.prevent
				autocomplete="off"
			/>
			<label :for="uuid" class="label">
				{{ props.placeholder }}
			</label>

			<div class="tags" v-if="tags && tags.length > 0">
				<span
					@click.stop.prevent="
						tags.splice(tags.indexOf(tag), 1);
						$emit('update:value', tags);
					"
					v-for="tag in tags"
					:key="tag"
					class="item"
					>{{ tag }}</span
				>
			</div>
		</template>
	</div>
</template>

<style lang="scss" scoped>
@import "@/globals/mixins.scss";
.group {
	position: relative;
	font-size: 18rem;
	margin: 10rem;
	border: 2rem solid var(--primary-color);
	background-color: var(--background);
	border-radius: 4rem;
	width: fit-content;

	&.checkbox {
		@include d-flex(h);

		& > .checkbox {
			width: 15rem;
			height: 15rem;
			margin: 5rem;
		}
		padding-right: 5rem;
	}

	.label {
		position: absolute;
		top: -5rem;
		left: 5rem;
		padding: 0 2rem;
		transform: translateY(-25%);
		transition: 0.2s;
		font-size: 0.6em;
		font-weight: 700;
		line-height: 12rem;
		background-color: var(--background);
		color: var(--primary-color);
		user-select: none;
	}

	&.size- {
		&fw {
			width: 100%;
		}
		&mw {
			width: 50%;
		}
	}

	.field {
		width: 100%;
		min-width: 100%;
		max-width: 100%;

		outline: 0;
		color: var(--foreground);
		padding: 6rem 8rem;
		background: transparent;

		&.multiline {
			min-height: 150rem;
			max-height: 400rem;

			box-sizing: border-box;
		}

		&.picker {
			@include d-flex(v);

			.placeholder {
				width: 100%;
				height: 100%;
				background: transparent;
			}
			.preview {
				max-width: 150rem;
				max-height: 100rem;
				width: fit-content;
				margin: 0 auto;
				user-select: none;

				&:hidden {
					display: none;
				}
			}
		}

		&::placeholder {
			color: transparent;
		}

		&:placeholder-shown:not(:focus) {
			border-color: var(--foreground);
			& ~ .label {
				cursor: text;
				font-size: 1em;
				top: 14rem;
				transform: translateY(-25%);
				color: var(--secondary);
			}
		}

		&:required,
		&:invalid {
			box-shadow: none;
		}
	}

	.tags {
		margin: 5rem;
		user-select: none;
		@include d-flex(h wp, $gap: 8rem);

		& > .item {
			cursor: pointer;
			box-shadow: var(--shadow);
			border-radius: 5rem;

			padding: 4rem 6rem;
			font-size: 16rem;
			line-height: 16rem;
		}
	}
}
</style>
