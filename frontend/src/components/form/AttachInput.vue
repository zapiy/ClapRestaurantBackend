<script setup lang="ts">
import { selectFile, useUUID } from "@/utils";
import { reactive, onUpdated, ref } from "vue";

const emit = defineEmits(["changed"]);
const props = defineProps({
  types: {
    type: Array<String>,
    required: false,
    default: null,
    validator: (value: Array<string>) =>
      value == null ||
      (value.length > 0 &&
        value.every((el) => ["image", "video"].includes(el))),
  },
});

const fileExtensions = {
  image: ["jpg", "png", "jpeg"],
  video: ["avi", "mp3", "mp4"],
};
const files = reactive([]);
async function addFile() {
  const file = await selectFile(
    props.types == null
      ? null
      : props.types
          .filter((el) => fileExtensions.hasOwnProperty(el))
          .map((el) => fileExtensions[el])
          .flat(Infinity)
  );
  const ext = /[^.]+$/.exec(file.name)[0];
  files.push({
    uuid: useUUID(),
    type: (Object.entries(fileExtensions).find((pair) =>
      pair[1].includes(ext)
    ) ?? ["file"])[0],
    url: URL.createObjectURL(file),
    file: file,
  });
  emit("changed", { files: files.map((el) => el.file) });
  transfer.items.add(file);
}

const removeFile = (data) => {
  files.splice(files.indexOf(data), 1);
  emit("changed", { files: files.map((el) => el.file) });
};

const transfer = new DataTransfer();
const input = ref();
onUpdated(() => (input.value.files = transfer.files));
</script>

<template>
  <div class="attach-input">
    <button class="add-btn" @click.prevent.stop="addFile">
      <mdicon name="plus" />
    </button>
    <div class="attachments">
      <template v-for="data in files" :key="data.uuid">
        <img
          v-if="data.type == 'image'"
          class="image"
          :src="data.url"
          @click="removeFile(data)"
        />
        <div v-else class="file" @click="removeFile(data)">
          <mdicon
            class="icon"
            :name="data.type == 'video' ? 'video' : 'file-document'"
          />
          <span class="name">{{ data.file.name }}</span>
        </div>
      </template>
      <input type="file" name="attachments" ref="input" hidden />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/globals/mixins.scss";
.attach-input {
  height: 120rem;
  max-width: 100%;
  margin: 5rem;

  @include d-flex(h, $gap: 10rem);

  & > .attachments {
    @include d-flex(h wp, $gap: 10rem);
    box-shadow: var(--rev-shadow);
    height: 100%;
    min-width: 200rem;
    border-radius: 10rem;
    padding: 10rem;
    user-select: none;

    .image {
      height: 100%;
      border-radius: 10rem;
    }
    .file {
      @include d-flex(v c, $gap: 5rem);
      height: 100%;

      .icon {
        width: 30rem;
        height: 30rem;
      }
      .name {
        overflow: hidden;
        max-width: 150rem;
        white-space: wrap;
        text-wrap: wrap;
        text-overflow: ellipsis;
      }
    }
  }

  & > .add-btn {
    width: 50rem;
    height: 50rem;

    border-radius: 50%;
    box-shadow: var(--shadow);
    padding: 5rem;

    &:active {
      box-shadow: var(--rev-shadow);
    }
  }
}
</style>
