<template>
	<div class="loading-freeze-skin">
		<div class="spinner">
			<div class="line"></div>
		</div>
	</div>
</template>

<style lang="scss" scoped>
@import "@/globals/mixins.scss";

.loading-freeze-skin {
	position: fixed;
	top: var(--header-height);
	left: 0;
	width: 100vw;
	height: calc(105vh - var(--header-height));
	z-index: 99;

	background-color: rgba(0, 0, 0, 0.5);

	display: flex;
	justify-content: center;
	align-items: center;

	.spinner {
		width: 100%;
		height: 10rem;
		overflow: hidden;
		border-radius: 5rem;

		& > .line {
			background: var(--primary-color);
			width: 0;
			height: 100%;
			border-radius: 2rem;
			margin-top: 0;
			margin-left: -25%;

			@include animation(
				2s infinite linear,
				(
					(margin-left: 0, width: 50%),
					(margin-left: 50%, width: 50%),
					(margin-left: 75%, width: 25%),
					(margin-left: 100%)
				)
			);
		}
	}
}
</style>
