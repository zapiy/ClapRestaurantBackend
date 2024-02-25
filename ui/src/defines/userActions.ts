import { store } from ".";
import { Permission, hasPermission } from "./permission";
import { pusher } from "./remoteFetcher";

const actions = [
	{
		text: "Logout",
		handle: async () => {
			await pusher("/logout");
			window.location.replace("/");
		},
	},
];

if (hasPermission(Permission.OWNER)) {
	actions.unshift({
		text: "Change password",
		handle: async () =>
			store.showDialog({
				title: "Change super user password",
				inputs: {
					password: {
						placeholder: "Password",
						required: true,
					},
				},
				handle: async function (data: object) {
					const resp = await pusher(`/super`, {
						data: data,
					});
					if (resp.status != 200) {
						store.notify("Error on server side, try later!!!");
						return false;
					}
					store.notify("Password changed successfully!!!");
					return true;
				},
			}),
	});
}

export default actions;
