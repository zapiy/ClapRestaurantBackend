<script lang="ts" module>
export interface Cell {
	text: String;
	span?: Number;
}
</script>

<script lang="ts" setup>
defineEmits(["click"]);

const props = defineProps({
	rows: {
		type: Array<String | Cell>,
		required: true,
	},
});
</script>

<template>
	<tr @:click="$emit('click')">
		<td
			v-for="cell in props.rows"
			:key="typeof cell == 'object' ? cell.text : cell"
			:colspan="typeof cell == 'object' ? cell.span : null"
			:class="['color-' + (cell?.color ?? 'none')]"
		>
			{{ typeof cell == "object" ? cell.text : cell }}
		</td>
		<td v-if="$slots.default">
			<slot></slot>
		</td>
	</tr>
</template>

<style scoped lang="scss">
tr {
	border-bottom: 1px solid var(--primary-color);
	background-color: var(--background);
	transition: background-color 0.2s;

	&:last-child {
		border-bottom-left-radius: 10rem;
		border-bottom-right-radius: 10rem;
	}

	&:hover {
		background-color: var(--secondary);
	}

	td,
	th {
		min-width: 100rem;
		padding: 4rem;

		text-align: center;
	}

	& > td.color- {
		&confirm {
			color: var(--confirm-color);
		}
		&cancel {
			color: var(--cancel-color);
		}
		&blue {
			color: var(--blue-color);
		}
		&gold {
			color: var(--gold-color);
		}
		&none {
			color: var(--foreground);
		}
	}
}
</style>
