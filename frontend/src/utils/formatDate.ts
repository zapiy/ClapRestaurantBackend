const zeroPad = (num: number, places: number) =>
	String(num).padStart(places, "0");

interface IPDParams {
	date: string;
	useDate?: boolean;
	useTime?: boolean;
}

const prettyDate = (params: IPDParams) => {
	if (!params) return "<Empty>";

	let temp;
	if (typeof params == "string") {
		temp = new Date(params);
	} else {
		if (!params.date) return "<Empty>";

		temp = new Date(params.date);

		if (params.useTime && !params.useDate) {
			return zeroPad(temp.getHours(), 2) + ":" + zeroPad(temp.getMinutes(), 2);
		} else if (!params.useTime && params.useDate) {
			return (
				zeroPad(temp.getDate(), 2) +
				"-" +
				zeroPad(temp.getMonth() + 1, 2) +
				"-" +
				temp.getFullYear()
			);
		}
	}
	return (
		zeroPad(temp.getDate(), 2) +
		"-" +
		zeroPad(temp.getMonth() + 1, 2) +
		"-" +
		temp.getFullYear() +
		" " +
		zeroPad(temp.getHours(), 2) +
		":" +
		zeroPad(temp.getMinutes(), 2)
	);
};
export default prettyDate;
