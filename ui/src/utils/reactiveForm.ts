import { trigger } from "@vue/reactivity";
import { shallowReactive, isRef, watch, computed, ref } from "vue";

interface ReactiveFieldDefinition {
	required?: boolean;
	validate?: (value: any) => boolean;
	prepare?: (value: any) => any;
	preview?: (value: any) => any;
	submit?: (value: any, form: FormData) => void | any;
	default?: (() => any) | any;
}
interface ReactiveFormInit {
	fields?: { [name: string]: ReactiveFieldDefinition };
	defaults: { [name: string]: any };
	isNew?: boolean;
	isEdit?: boolean;
}
export default function reactiveForm(params: ReactiveFormInit) {
	const obj = {
		defaults:
			(isRef(params.defaults) ? params.defaults.value : params.defaults) ?? {},
		output: {},
	};
	const isEdit = ref(params.isEdit ?? params.isNew ?? false);
	const isNew = ref(params.isNew ?? false);
	const formValid = ref(false);
	const proxy = new Proxy(obj, {
		has(obj, name) {
			if (name.startsWith("__")) {
				return obj.hasOwnProperty(name);
			} else if (name.startsWith("$")) {
				return obj.hasOwnProperty(name.slice(1));
			}
			return params.fields.hasOwnProperty(name);
		},
		get(obj, name) {
			if (typeof name !== "string") return null;
			else if (name.startsWith("__")) {
				return obj[name];
			}

			const info = params?.fields?.[name];
			if (obj.output.hasOwnProperty(name)) {
				const value = obj.output[name];
				return value ? info?.preview?.(value) ?? value : null;
			}
			if (obj.defaults.hasOwnProperty(name)) {
				return obj.defaults?.[name];
			}

			if (info?.default) {
				const value =
					typeof info?.default === "function"
						? info?.default?.call()
						: info?.default;

				obj.defaults[name] = value;
				return value;
			}

			obj.defaults[name] = null;
			return null;
		},
		set(obj, name, value) {
			if (typeof name !== "string") return null;
			else if (name.startsWith("__")) {
				return (obj[name] = value);
			} else if (
				(params?.fields && !params?.fields?.hasOwnProperty(name)) ||
				false
			) {
				return false;
			} else if (!isEdit.value) {
				return false;
			}

			if (typeof value === "string") {
				value = value.trim();
			}

			const info = params?.fields?.[name];
			if (info?.prepare) {
				value = info?.prepare?.(value);
			}

			obj.output[name] = value;

			if (params.fields) {
				formValid.value = !Object.entries(params.fields).some(([key, info]) => {
					const value = obj.output?.[key];
					const required = info.required ?? false;
					if (!value) {
						if (required && !isNew.value && obj.defaults.hasOwnProperty(key)) {
							return false;
						}
						return required;
					}
					return info.validate ? !info.validate(value) : false;
				});
			}
			return true;
		},
	});

	if (isRef(params.defaults)) {
		watch(params.defaults, (val) => {
			if (!val) return;
			obj.defaults = Object.assign(obj.defaults, val);
			Object.keys(val).forEach((key) => trigger(proxy, "set", key));
		});
	}
	watch(isEdit, (val) => {
		if (!val) {
			const keys = Object.keys(obj.output);
			obj.output = {};
			keys.forEach((key) => trigger(proxy, "set", key));
		}
	});

	return {
		form: shallowReactive(proxy),
		formValid: computed(() => formValid.value),
		formEditing: isEdit,
		formNewest: isNew,
		submitForm: function (remote?: Object) {
			if (!params.fields || !isEdit.value || !formValid.value) return null;
			obj.defaults = remote ?? Object.assign(obj.defaults, obj.output);
			obj.output = {};
			isEdit.value = false;
			isNew.value = false;
		},
		generatePostForm: function () {
			if (!params.fields || !isEdit.value || !formValid.value) return null;

			const form = new FormData();
			Object.entries(params.fields).forEach(([key, info]) => {
				let value = obj.output?.[key];
				if (value === undefined || value === null) return;
				value = info?.submit ? info.submit(value, form) : value;

				if (
					value !== undefined &&
					value !== null &&
					(value.constructor == Object || value.constructor == Array)
				) {
					value = JSON.stringify(value);
				}

				if (value) form.set(key, value);
			});
			return form;
		},
	};
}
