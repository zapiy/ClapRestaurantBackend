export enum Permission {
	OWNER = 5,
	ADMIN = 1,
}

export const hasPermission = (permission: Permission) =>
	window.GLOBAL_INAPP_PERMISSION >= permission;
