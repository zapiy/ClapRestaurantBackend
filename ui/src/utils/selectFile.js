import AsyncLock from "./asyncLock";
import { store } from "@/defines";

async function selectFile(extensions = null) {
	const input = Object.assign(document.createElement("input"), {
		type: "file",
	});

	if (extensions) {
		input.accept = extensions.map((el) => `.${el}`).join(",");
	}

	const extras = {
		lock: new AsyncLock(),
		value: null,
	};

	const onChanged = (ev) => {
		if (ev.target.files) {
			const file = ev.target.files[0];

			if (
				extensions != null &&
				(!file || !file.name.match(`\\.(` + extensions.join("|") + `)$`))
			) {
				store.notify("Unsupported file type!");
				return;
			}
			extras.value = file;
		}
		extras.lock.free();
	};

	input.onchange = onChanged;
	input.click();

	await extras.lock.lock(true);

	return extras.value;
}

export default selectFile;
