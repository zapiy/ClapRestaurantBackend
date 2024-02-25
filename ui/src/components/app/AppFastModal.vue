<script setup lang="ts">
import {
  ModalWindow,
  InputField,
  ActionButton,
  AttachInput,
  InfoView,
} from "@/components/form";
import { store } from "@/defines";
import { ref } from "vue";

const modalDialogForm = ref();
var modalDialogLock = false;
async function handleModalDialogClose() {
  if (modalDialogLock) return;
  store.dialogContext = null;
}
const validators = {
  email: (val) =>
    val.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    ),
  number: (val) => /^\d*$/.test(val),
  phone: (val) =>
    val.match(/^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/),
};
async function handleModalDialog() {
  const ctx = store.dialogContext;
  if (ctx.handle) {
    if (modalDialogLock) return;
    modalDialogLock = true;
    try {
      if (ctx.inputs || ctx.attach) {
        const form = new FormData(modalDialogForm.value);

        if (!ctx.inputs) {
          if ((await ctx.handle(form)) ?? true) {
            store.dialogContext = null;
          }
          return;
        }

        const data = Object.fromEntries(form.entries());

        const requiredFields = Object.entries(data)
          .filter(
            ([key, val]) =>
              (ctx.inputs[key]?.required ?? true) &&
              val.length == 0 &&
              !["tags"].includes(ctx.inputs[key].type)
          )
          .map((pair) => ctx.inputs[pair[0]].placeholder);

        if (requiredFields.length == 0) {
          if (
            Object.entries(data).every(([key, value]) => {
              const info = ctx.inputs[key];
              if (!info) return true;

              const type = info.type ?? "text",
                name = info.placeholder ?? key;

              if (type == "tags") {
                const list = modalDialogForm.value.querySelector(
                  `input[name="${key}"]`
                ).tags;

                if ((!info?.required ?? true) && list.length == 0) {
                  store.notify(`Field '` + name + `' cannot be empty`);
                  return false;
                }

                data[key] = list;
                form.set(key, JSON.stringify(list));

                return !list.some((el) => {
                  if (info.min && el.length < info.min) {
                    store.notify(
                      `Length item '${el}' of field '${name}' cannot be less than ${info.min}`
                    );
                    return true;
                  } else if (info.max && el.length > info.max) {
                    store.notify(
                      `Length item '${el}' of field '${name}' cannot be more than ${info.max}`
                    );
                    return true;
                  }
                });
              }

              if ((!info?.required ?? true) && value.length == 0) return true;

              if (validators.hasOwnProperty(type) && !validators[type](value)) {
                store.notify(
                  "Field ''" + name + "' is not in the correct format"
                );
                return false;
              }

              if (type === "number") {
                value = data[key] = Number(value);

                if (info.min && value < info.min) {
                  store.notify(
                    `Field '` + name + `' cannot be less than ${info.min}`
                  );
                  return false;
                } else if (info.max && value > info.max) {
                  store.notify(
                    `Field '` + name + `' cannot be more than ${info.max}`
                  );
                  return false;
                }
              } else if (info.min && value.length < info.min) {
                store.notify(
                  `Field length '` + name + `' cannot be less than ${info.min}`
                );
                return false;
              } else if (info.max && value.length > info.max) {
                store.notify(
                  `Field length '` + name + `' cannot be more than ${info.max}`
                );
                return false;
              }
              return true;
            })
          ) {
            Object.entries(ctx.inputs).forEach(([key, info]) => {
              if (info.type == "checkbox") {
                form.set(key, form.has(key) ? "true" : "false");
                return true;
              }
            });

            if ((await ctx.handle(form)) ?? true) {
              store.dialogContext = null;
            }
          }
        } else {
          store.notify(
            "Fields (" + requiredFields.join(", ") + ") cannot be empty"
          );
        }
      } else if ((await ctx.handle()) ?? true) {
        store.dialogContext = null;
      }
    } finally {
      modalDialogLock = false;
    }
  } else {
    store.dialogContext = null;
  }
}
</script>
<template>
  <ModalWindow
    :title="$store.dialogContext.title"
    @close="handleModalDialogClose"
    visible
  >
    <span v-if="$store.dialogContext.text">{{
      $store.dialogContext.text
    }}</span>
    <form
      v-if="$store.dialogContext.inputs || $store.dialogContext.attach"
      ref="modalDialogForm"
      @submit.prevent="handleModalDialog"
    >
      <InputField
        v-for="(inp, key) in $store.dialogContext.inputs"
        :key="key"
        :name="key"
        :placeholder="inp.placeholder"
        :type="inp.type ?? 'text'"
        :value="inp.value"
        :required="inp.required"
        size="fw"
      />
      <AttachInput v-if="$store.dialogContext.attach" />
    </form>
    <template #actions>
      <ActionButton
        text="Cancel"
        v-if="$store.dialogContext.inputs"
        size="ex"
        color="cancel"
        @:click="handleModalDialogClose"
      />
      <ActionButton
        text="Okay"
        size="ex"
        color="confirm"
        @:click="handleModalDialog"
      />
    </template>
  </ModalWindow>
</template>
