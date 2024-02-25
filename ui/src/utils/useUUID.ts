function replacePattern(c: string) {
	const r = (Math.random() * 16) | 0;
	const v = c == "x" ? r : (r & 0x3) | 0x8;
	return v.toString(16);
}

export default function useUUID(prefix?: string) {
	const _pattern = "xxxx-xxxxxxxxxxxx";
	return (prefix ? `${prefix}--` : "") + _pattern.replace(/x/g, replacePattern);
}
