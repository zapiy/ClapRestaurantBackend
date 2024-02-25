<script setup lang="ts">
import {
	AccentBox,
	TableView,
	TableViewLine,
	PaginatorControl,
	LoadingPreview,
} from "@/components";
import { ActionButton } from "@/components/form";
import { fetcher } from "@/defines";
import { prettyDate } from "@/utils";
import { ref, watch } from "vue";
import useSWRV from "swrv";
import SearchControl from "@/components/SearchControl.vue";
import ModeratorModal from "./ModeratorModal.vue";

const selected = ref(null);

const paginate = ref(1);
const searchQuery = ref();
const { data, mutate: reload } = useSWRV("/moderators", (url) => {
	const params = { p: paginate.value };
	if (searchQuery.value) {
		params.q = searchQuery.value;
	}
	return fetcher(url, params);
});
watch(paginate, () => reload());
watch(searchQuery, () => reload());
</script>

<template>
	<div class="inner">
		<template v-if="data != null">
			<AccentBox title="Managers">
				<template #center>
					<SearchControl v-model:query="searchQuery" />
				</template>
				<template #actions>
					<ActionButton
						text="Add manager"
						@click="selected = { uuid: 'new' }"
					/>
				</template>

				<TableView :header="['Key identifier', 'Created at']">
					<TableViewLine
						v-for="item in data.view"
						:key="item.uuid"
						:rows="[item.key_name, prettyDate(item.created_at)]"
						@click="selected = item"
					/>
				</TableView>
			</AccentBox>
			<PaginatorControl
				v-model:current="paginate"
				:max="data?.paginator?.max ?? 1"
			/>

			<template v-if="selected">
				<ModeratorModal
					:item="selected"
					@reload="reload"
					@close="selected = null"
				/>
			</template>
		</template>
		<LoadingPreview v-else />
	</div>
</template>
