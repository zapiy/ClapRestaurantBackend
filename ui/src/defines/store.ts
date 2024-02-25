// import { createStore } from "vuex";
import { reactive } from "vue";

interface IInputInfo {
	placeholder: string;
	type?: string;
	required?: boolean;
	min?: number;
	max?: number;
	value?: any;
}
interface IDialogContext {
	title?: string;
	text?: string;
	inputs?: { [Key: string]: IInputInfo };
	attach?: boolean;
	handle?:
		| ((data: object) => Promise<boolean>)
		| ((data: object) => Promise<void>);
}
const store = reactive({
	sidebarShown: false,
	isProcessing: false,
	dialogContext: null,
	notifications: [],
	switchSidebar() {
		this.sidebarShown = !this.sidebarShown;
	},
	showDialog(context: IDialogContext) {
		this.dialogContext = context;
	},
	notify(text: string) {
		const data = reactive({
			id: Math.random() * 9000,
			text: text,
			progress: 100,
		});
		data.interval = setInterval(() => {
			data.progress -= 1;
			if (data.progress <= 0) {
				this.notifications = this.notifications.filter(
					(el) => el.id !== data.id
				);
			}
		}, text.length * 1.5);

		data.stop = () => {
			clearInterval(data.interval);
			this.notifications = this.notifications.filter((el) => el.id !== data.id);
		};
		this.notifications.unshift(data);
	},
});

export default store;
