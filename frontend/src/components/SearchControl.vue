<script setup lang="ts">
import { ref, watch, nextTick } from "vue";
import { useRoute } from "vue-router";
import { routerSetQuery } from "@/defines";

const emit = defineEmits(["update:query"]);
const route = useRoute();

const props = defineProps({
	query: {
		type: String,
		required: true,
	},
});

const current = ref(props.query);
if (props.query == null || props.query == undefined) {
	nextTick(() => {
		const queryParam: string = route.query.q;
		current.value = queryParam ?? null;
		routerSetQuery("q", current.value);
		emit("update:query", current.value);
	});
}

watch(current, (val) => {
	if (val === "") {
		current.value = null;
		return;
	}
	routerSetQuery("q", current.value);
	emit("update:query", current.value);
});
</script>

<template>
	<div class="search-field">
		<mdicon class="search-icon" name="magnify" />
		<input
			class="field"
			:value="current"
			@input.stop.prevent="(ev) => (current = ev.target.value.trim())"
			autocomplete="off"
		/>
		<mdicon
			v-if="current != null"
			@click="() => (current = null)"
			class="search-close-icon"
			name="close"
		/>
	</div>
</template>

<style lang="scss">
.search-icon .search-close-icon {
	width: 35rem;
	height: 35rem;
}

.search-icon svg {
	fill: var(--primary-color);
}
</style>

<style lang="scss" scoped>
@import "@/globals/mixins.scss";
.search-field {
	@include d-flex(h);

	position: relative;
	font-size: 18rem;
	margin: 10rem;
	border: 2rem solid var(--primary-color);
	background-color: var(--background);
	border-radius: 8rem;
	width: 40vw;

	& > .field {
		width: 100%;
		height: 100%;
		padding: 5rem;
	}
}
</style>
