<script setup lang="ts">
import {
	AccentBox,
	TableView,
	TableViewLine,
	PaginatorControl,
	ClickableContainer,
	LoadingPreview,
} from "@/components";
import { ActionButton, InfoView, ModalWindow } from "@/components/form";
import { store } from "@/defines";
import { fetcher, pusher } from "@/defines";
import { prettyDate, selectFile } from "@/utils";
import { ref, watch } from "vue";
import useSWRV from "swrv";
import SearchControl from "@/components/SearchControl.vue";

const selectedUser = ref(null);
const switchUser = async () => {
	console.log("Switching user");
	const resp = await pusher(`/user/${selectedUser.value?.uuid}`, {
		data: {
			op: "switch",
		},
	});
	selectedUser.value = await resp.json();
	await reload();
};

const changeAvatar = async () => {
	const selected = selectedUser.value;
	const image = await selectFile(["jpg", "jpeg", "png"]);
	const form = new FormData();
	form.append("avatar", image);

	const resp = await pusher(`/user/${selected?.uuid}`, {
		data: form,
	});
	if (resp.status != 200) {
		if (resp.status >= 500) {
			store.notify("Error on server side, try later!!!");
		} else if (resp.status == 406) {
			store.notify(
				"Validation error, most likely this email is registered, use the search"
			);
		}
	}
	selectedUser.value = await resp.json();
	await reload();
};

const addUser = (edit: boolean = false) => {
	const selected = selectedUser.value;
	selectedUser.value = null;

	store.showDialog({
		title: "Add user",
		inputs: {
			full_name: {
				placeholder: "Full Name",
				min: 1,
				max: 150,
				value: edit ? selected?.full_name : null,
			},
			email: {
				placeholder: "Email",
				type: "email",
				max: 120,
				value: edit ? selected?.email : null,
			},
			birthday: {
				placeholder: "Birthday",
				type: "date",
				value: edit ? selected?.birthday : null,
			},
			working_at: {
				placeholder: "Start Working Day",
				type: "date",
				value: edit ? selected?.working_at : Date.now(),
			},
		},
		handle: async function (data: object) {
			const resp = await pusher(`/user/${selected?.uuid ?? "new"}`, {
				data: data,
			});
			if (resp.status != 200) {
				store.notify("Error on server side, try later!!!");
				return false;
			}
			await reload();
			return true;
		},
	});
};

const paginate = ref(1);
const searchQuery = ref();
const { data, mutate: reload } = useSWRV("/users", (url) => {
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
			<AccentBox title="Users">
				<template #center>
					<SearchControl v-model:query="searchQuery" />
				</template>
				<template #actions>
					<ActionButton text="Add user" @click="addUser" />
				</template>

				<TableView
					:header="['Full Name', 'Birthday', 'Start Working Day', 'Status']"
				>
					<TableViewLine
						v-for="item in data.view"
						:key="item.uuid"
						@click="selectedUser = item"
						:rows="[
							item.full_name,
							prettyDate({ date: item.birthday, useDate: true }),
							prettyDate({ date: item.working_at, useDate: true }),
							item?.status,
						]"
					/>
				</TableView>
			</AccentBox>
			<PaginatorControl
				v-model:current="paginate"
				:max="data?.paginator?.max ?? 1"
			/>
		</template>
		<LoadingPreview v-else />

		<ModalWindow
			:visible="selectedUser != null"
			@close="selectedUser = null"
			:title="selectedUser?.full_name"
		>
			<ClickableContainer @click="changeAvatar" :image="selectedUser?.avatar" />

			<InfoView
				:items="{
					Birthday: prettyDate({ date: selectedUser?.birthday, useDate: true }),
					'Start working day': prettyDate({
						date: selectedUser?.working_at,
						useDate: true,
					}),
					Status: selectedUser?.status,
				}"
			/>

			<template #actions>
				<ActionButton
					text="Cancel"
					size="ex"
					color="cancel"
					@click="selectedUser = null"
				/>
				<ActionButton
					v-if="selectedUser.status == 'leave'"
					text="Restore"
					size="ex"
					color="confirm"
					@click="switchUser"
				/>
				<template v-else>
					<ActionButton
						text="Fired"
						size="ex"
						color="cancel"
						@click="switchUser"
					/>
					<ActionButton text="Edit" size="ex" @click="() => addUser(true)" />
				</template>
			</template>
		</ModalWindow>
	</div>
</template>
