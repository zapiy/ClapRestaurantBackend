import { createRouter, createWebHashHistory } from "vue-router";
import { hasPermission, Permission } from "./permission";

const routes = [
	{
		path: "/",
		name: "Users",
		icon: "account",
		component: () => import("@/views/UsersView.vue"),
	},
	{
		path: "/news",
		name: "News",
		icon: "newspaper",
		component: () => import("@/views/news/NewsView.vue"),
	},
	{
		path: "/news/:uuid",
		component: () => import("@/views/news/NewsItem.vue"),
	},
	{
		path: "/foods",
		name: "Menu",
		icon: "food",
		component: () => import("@/views/food/FoodsView.vue"),
	},
	{
		path: "/food/category/:uuid",
		component: () => import("@/views/food/FoodCategory.vue"),
	},
	{
		path: "/food/:uuid",
		component: () => import("@/views/food/FoodItem.vue"),
	},
	{
		path: "/quizzes",
		name: "Trainings",
		icon: "help-box-multiple",
		component: () => import("@/views/quiz/QuizView.vue"),
	},
	{
		path: "/quiz/:uuid",
		component: () => import("@/views/quiz/QuizItem.vue"),
	},
	{
		path: "/sprints",
		name: "Sprints",
		icon: "check-decagram",
		component: () => import("@/views/sprints/SprintQuizzesView.vue"),
	},
	{
		path: "/sprint/quiz/:uuid",
		component: () => import("@/views/sprints/SprintQuizView.vue"),
	},
	{
		path: "/sprint/quiz/:quiz/:user",
		component: () => import("@/views/sprints/SprintUserQuizView.vue"),
	},
	{
		path: "/sprint/:uuid",
		component: () => import("@/views/sprints/SprintItem.vue"),
	},
];

if (hasPermission(Permission.OWNER)) {
	routes.push({
		path: "/moderators",
		name: "Managers",
		icon: "shield-crown",
		component: () => import("@/views/moderator/ModeratorView.vue"),
	});
}

const router = createRouter({
	history: createWebHashHistory(location.pathname + "/admin/"),
	routes: routes,
});

function routerSetQuery(name, value) {
	router.replace({
		query: {
			...router.currentRoute.value.query,
			[name]: value,
		},
	});
}

const currentRoute = () => router.currentRoute;

export { router, routerSetQuery, currentRoute };
