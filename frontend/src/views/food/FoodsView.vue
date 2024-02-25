<script setup lang="ts">
import { AccentBox, LoadingPreview, TreeView } from "@/components";
import { ActionButton } from "@/components/form";
import { fetcher, pusher } from "@/defines";
import { store } from "@/defines";
import useSWRV from "swrv";

const removeCategory = (category: object) =>
	store.showDialog({
		title: "Delete",
		text: "Are you sure you want to delete?",
		handle: async function () {
			const resp = await pusher(`/food/category/${category.uuid}`, {
				method: "DELETE",
				data: {
					uuid: category.uuid,
				},
			});
			if (resp.status != 200) {
				store.notify("Error on server side, try later!!!");
				return false;
			}
			await reload();
			return true;
		},
	});

const addCategory = (parent?: object, is_edit: boolean = false) =>
	store.showDialog({
		title: "Add category",
		inputs: {
			image: {
				placeholder: "Image",
				type: "image",
			},
			name: {
				placeholder: "Name",
				min: 1,
				max: 100,
				value: is_edit ? parent?.name : null,
			},
		},
		handle: async function (data: object) {
			if (parent && !is_edit) {
				data.append("parent", parent.uuid);
			}
			const resp = await pusher(
				`/food/category/` + (is_edit ? parent?.uuid : "new"),
				{
					data: data,
				}
			);
			if (resp.status != 200) {
				store.notify("Error on server side, try later!!!");
				return false;
			}
			await reload();
			return true;
		},
	});

const { data, error, mutate: reload } = useSWRV("/food/category", fetcher);
</script>

<template>
	<div class="inner">
		<h1 v-if="error">Fail to receive data!</h1>
		<template v-else-if="data != null">
			<AccentBox title="Menu">
				<template #actions>
					<ActionButton text="Add category" @click="addCategory" />
				</template>

				<TreeView
					v-for="category in data"
					:key="category.uuid"
					:title="category.name"
					:image="category.image"
					@click="
						if (!category.children || category.children?.length == 0)
							$router.push(`/food/category/${category.uuid}`);
					"
				>
					<template #actions>
						<ActionButton
							text="Edit"
							color="gold"
							@click="() => addCategory(category, true)"
						/>
						<ActionButton
							text="Add sub category"
							v-if="!category.has_foods"
							@click="() => addCategory(category)"
						/>
						<ActionButton
							text="Remove"
							v-if="
								!category.has_foods &&
								(!category.children || category.children?.length == 0)
							"
							@click="() => removeCategory(category)"
						/>
					</template>

					<template
						#default
						v-if="category.children && category.children.length > 0"
					>
						<TreeView
							v-for="sub in category.children"
							:key="sub.uuid"
							:title="sub.name"
							:image="sub.image"
							@click="
								if (!sub.children || sub.children.length == 0)
									$router.push(`/food/category/${sub.uuid}`);
							"
						>
							<template #actions>
								<ActionButton
									text="Edit"
									color="gold"
									@click="() => addCategory(sub, true)"
								/>
								<ActionButton
									text="Remove"
									v-if="
										!sub.has_foods &&
										(!sub.children || sub.children?.length == 0)
									"
									@click="() => removeCategory(sub)"
								/>
							</template>
						</TreeView>
					</template>
				</TreeView>
			</AccentBox>
		</template>
		<LoadingPreview v-else />
	</div>
</template>
