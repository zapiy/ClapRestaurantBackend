const baseUrl = import.meta.env.PROD
	? "/@/api/admin"
	: "http://localhost:8000/@/api/admin";

interface IPusherParams {
	data: object;
	method?: string;
}
const pusher = async (url: string, params?: IPusherParams) => {
	const cookies =
		document.cookie === ""
			? {}
			: Object.fromEntries(
					document.cookie.split("; ").map((el) => el.split("="))
			  );

	const headers = {
		"X-CSRF-TOKEN": cookies["admin_csrf_token"] ?? "none",
	};
	if (params?.data && !(params?.data instanceof FormData)) {
		headers["Content-Type"] = "application/json";
	}
	return await fetch(baseUrl + url, {
		method: params?.method ?? (params?.data ? "POST" : "GET"),
		headers: headers,
		mode: import.meta.env.PROD ? "same-origin" : "cors",
		referrerPolicy: import.meta.env.PROD ? "same-origin" : "no-referrer",
		body: params?.data
			? params?.data instanceof FormData
				? params.data
				: JSON.stringify(params.data)
			: null,
	});
};

class RequestError extends Error {
	constructor(message?: string, code?: number) {
		super(message);
		this.code = code;
	}
}

const fetcher = async (url: string, params: object): Promise<Object> => {
	const resp = await pusher(
		url + (params ? "?" + new URLSearchParams(params).toString() : "")
	);
	if (resp.status >= 300) {
		throw new RequestError(`Bad status code: ${resp.status}`, resp.status);
	}
	return await resp.json();
};

export { fetcher, pusher };
