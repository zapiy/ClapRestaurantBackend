<script setup lang="ts">
import {
	AppHeader,
	AppSidebar,
	AppNotifications,
	AppFastModal,
	AppLoadingFreeze,
} from "@/components/app";
</script>

<template>
	<AppHeader />

	<section class="content">
		<AppSidebar />

		<main>
			<RouterView v-slot="{ Component }">
				<Transition name="fade" mode="out-in">
					<Component :key="$route.path" :is="Component" />
				</Transition>
			</RouterView>
		</main>
	</section>

	<AppFastModal v-if="$store.dialogContext" />
	<AppLoadingFreeze v-if="$store.isProcessing" />
	<AppNotifications
		v-if="$store.notifications && $store.notifications.length > 0"
	/>
</template>

<style lang="scss" scoped>
@import "@/globals/mixins.scss";

.content {
	position: fixed;
	top: var(--header-height);
	left: 0;
	width: 100vw;
	height: calc(105vh - var(--header-height));

	@include d-flex(h);

	main {
		width: 100%;
		height: 100%;
		overflow-y: auto;
		padding: 10rem 5rem 50rem;
		z-index: 1;

		.fade-enter-active,
		.fade-leave-active {
			transition:
				opacity 0.2s,
				margin 0.2s;
		}

		.fade-enter-from,
		.fade-leave-to {
			opacity: 0;
			margin-left: 20%;
		}
	}
}
</style>
