<script lang="ts" setup>
import { ref } from "vue";

defineEmits(["click"]);
const props = defineProps({
	text: {
		type: String,
		required: true,
	},
	size: {
		type: String,
		default: "normal",
		validator: (value: string) =>
			["normal", "fw", "mw", "sm", "md", "ex"].includes(value),
	},
	color: {
		type: String,
		default: "primary",
		validator: (value: string) =>
			["primary", "confirm", "cancel", "flat", "blue", "gold"].includes(value),
	},
	subactions: {
		type: Object,
		required: false,
	},
	disabled: {
		type: Boolean,
		default: false,
	},
});

const expanded = ref(false);
</script>

<template>
	<button
		type="button"
		class="action-button"
		@:click.stop.prevent="subactions ? (expanded = !expanded) : $emit('click')"
		:class="[
			'size-' + props.size,
			'color-' + props.color,
			{ subactions: subactions, expanded },
		]"
		:disabled="props.disabled"
	>
		{{ props.text }}

		<div v-if="props.subactions" class="subactions">
			<button
				v-for="[key, val] in Object.entries(props.subactions)"
				:key="key"
				@click.stop.prevent="
					if (!props.disabled) {
						expanded = false;
						$emit('click', { type: key });
					}
				"
				class="item"
			>
				{{ val }}
			</button>
		</div>
	</button>
</template>

<style scoped lang="scss">
@import "@/globals/mixins.scss";

.action-button {
	position: relative;
	background: var(--primary-color);
	border-radius: 10rem;
	box-sizing: border-box;
	color: var(--background);
	cursor: pointer;
	font-size: 18rem;
	font-weight: 500;
	padding: 5rem 20rem;
	margin: 5rem 0;
	text-align: center;
	text-decoration: none;
	text-decoration-skip-ink: auto;
	text-shadow: rgba(0, 0, 0, 0.3) 1px 1px 1px;
	transition: all 0.2s ease-in-out;
	user-select: none;
	touch-action: manipulation;
	border: 0;
	margin: 5rem;
	white-space: nowrap;

	&.subactions {
		&.expanded {
			border-bottom-left-radius: 0;
			border-bottom-right-radius: 0;
			& > .subactions {
				visibility: visible;
			}
		}

		&:active {
			background: transparent;
			outline: 0;
		}

		& > .subactions {
			position: absolute;
			@include d-flex(v);
			width: 100%;
			top: calc(100% - 5rem);
			left: 0;

			background-color: var(--primary-color);
			border-top: 2rem;
			padding-top: 5rem;
			border-bottom-left-radius: 10rem;
			border-bottom-right-radius: 10rem;

			visibility: collapse;

			& > .item {
				padding: 2rem 8rem;
				color: var(--background);
			}
		}
	}

	&.color- {
		&confirm {
			background: var(--confirm-color);
		}
		&cancel {
			background: var(--cancel-color);
		}
		&blue {
			background: var(--blue-color);
		}
		&gold {
			background: var(--gold-color);
		}
		&flat {
			background: var(--background);
		}
	}

	&:not(:disabled) {
		&:not(.subactions):active {
			border-bottom-style: none;
			border-color: var(--secondary);
			box-shadow: var(--rev-shadow);
			background: transparent;
			outline: 0;
		}
		&:hover {
			border-bottom-style: none;
			border-color: var(--secondary);
		}
	}

	&.size- {
		&fw {
			width: 100%;
			font-size: 22rem;
		}
		&mw {
			width: 50%;
			font-size: 20rem;
		}
		&sm {
			font-size: 16rem;
		}
		&md {
			font-size: 20rem;
		}
		&ex {
			font-size: 24rem;
		}
	}
}
</style>
