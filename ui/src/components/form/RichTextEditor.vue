<script module lang="ts">
import Quill from "quill";
const Image = Quill.import("formats/image");
const Video = Quill.import("formats/video");
Image.sanitize = (url) => url;
Video.sanitize = (url) => url;
</script>

<script setup lang="ts">
import Delta from "quill-delta";
import { computed, onUpdated, ref } from "vue";
import { QuillEditor } from "@vueup/vue-quill";
import { selectFile } from "@/utils";

const emit = defineEmits(["update:content"]);
const props = defineProps({
	placeholder: {
		type: String,
		required: false,
		default: "Write something...",
	},
	content: {
		type: Object,
		required: false,
	},
	readOnly: {
		type: Boolean,
		required: false,
		default: false,
	},
});

const cachedFiles = {};

const imageSupportedExtensions = ["jpg", "jpeg", "png"];
const videoSupportedExtensions = ["mp4", "mp3", "avi"];

const editorToolbar = {
	container: [
		[{ header: [false, 6, 5, 4, 3, 2, 1] }],
		["bold", "italic", "underline", "strike"],

		[{ align: [] }, { list: "ordered" }, { list: "bullet" }],
		[
			{ indent: "-1" },
			{ indent: "+1" },
			{ script: "sub" },
			{ script: "super" },
		],
		[{ color: [] }, { background: [] }],
		["clean"],

		["blockquote", "code-block", "link", "video", "image"],
	],
	handlers: {
		image: async function () {
			const image = await selectFile(imageSupportedExtensions);
			if (image) {
				const index = this.quill.getSelection(0).index;
				const url = URL.createObjectURL(image);
				const hash = new URL(url.slice(5)).pathname.slice(1);
				cachedFiles[hash] = image;

				quill.value.getQuill().insertEmbed(index, "image", url);
			}
		},
		video: async function () {
			const video = await selectFile(videoSupportedExtensions);
			if (video) {
				const index = this.quill.getSelection(0).index;
				const url = URL.createObjectURL(video);
				const hash = new URL(url.slice(5)).pathname.slice(1);
				cachedFiles[hash] = video;

				quill.value.getQuill().insertEmbed(index, "video", url);
			}
		},
	},
};

const supportedBlobExtensions = ["image", "video"];

function updateContent(delta) {
	const attachments = {};
	const rich = delta.ops.map((line) => {
		if (line.hasOwnProperty("insert") && typeof line.insert === "object") {
			const blob_key = supportedBlobExtensions.find((el) =>
				line.insert.hasOwnProperty(el)
			);
			if (blob_key && line.insert[blob_key].startsWith("blob:")) {
				const hash = new URL(line.insert[blob_key].slice(5)).pathname.slice(1);
				const file = cachedFiles[hash];
				attachments[hash] = new File([file], hash, { type: file.type });
			}
		}
		return line;
	});

	emit("update:content", {
		ops: rich,
		attachments: attachments,
	});
}

const quill = ref();
const renderKey = ref(true);

onUpdated(async () => {
	const editor = quill.value.getQuill();

	editor.root.dataset.placeholder = props.placeholder;
	if (props.readOnly) {
		editor.disable();
	} else {
		editor.enable();
	}
});

const contentHandler = computed({
	get: () => (props.content ? new Delta(props.content) : null),
	set: updateContent,
});
</script>

<template>
	<div class="rich-editor" :class="{ readOnly }">
		<template v-if="renderKey">
			<QuillEditor
				ref="quill"
				:toolbar="editorToolbar"
				:theme="'snow'"
				:placeholder="props.placeholder"
				v-model:content="contentHandler"
			/>
			<!-- :modules="editorModules" -->
		</template>
	</div>
</template>

<style lang="scss">
.rich-editor {
	min-width: 300rem;

	&.readOnly .ql-toolbar {
		display: none;
	}
	.ql-editor {
		min-height: 150rem;
	}
}
</style>
