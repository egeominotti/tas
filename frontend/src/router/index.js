import Vue from 'vue'
import Router from 'vue-router'

const TheContainer = () => import('@/containers/TheContainer')
const Dashboard = () => import('@/views/Dashboard')


const BotFutures = () => import('@/views/tas/bot/BotFutures')
const BotSpot = () => import('@/views/tas/bot/BotSpot')
const ExchangeAccount = () => import('@/views/tas/bot/ExchangeAccount')
const BotHistory = () => import('@/views/tas/bot/BotHistory')


const Page404 = () => import('@/views/pages/Page404')
const Page500 = () => import('@/views/pages/Page500')
const Login = () => import('@/views/pages/Login')

Vue.use(Router)

export default new Router({
    mode: 'hash',
    linkActiveClass: 'open active',
    scrollBehavior: () => ({y: 0}),
    routes: [
        {
            path: '/',
            redirect: '/dashboard',
            name: 'Home',
            component: TheContainer,
            children: [
                {
                    path: 'dashboard',
                    name: 'Dashboard',
                    component: Dashboard
                },
                {
                    path: '/bot',
                    redirect: '/bot/list',
                    name: 'Bot',
                    component: {
                        render(c) {
                            return c('router-view')
                        }
                    },
                    children: [
                        {
                            path: 'listFutures',
                            name: 'ListFutures',
                            component: BotFutures
                        },
                        {
                            path: 'listSpot',
                            name: 'ListSpot',
                            component: BotSpot
                        },
                        {
                            path: 'history',
                            name: 'History',
                            component: BotHistory
                        },
                    ]
                },
                {
                    path: '/account',
                    redirect: '/account/',
                    name: 'Account',
                    component: {
                        render(c) {
                            return c('router-view')
                        }
                    },
                    children: [
                        {
                            path: 'viewExchange',
                            name: 'viewExchange',
                            component: ExchangeAccount
                        },
                    ]
                },
            ]
        },
        {
            path: '/pages',
            redirect: '/pages/404',
            name: 'Pages',
            component: {
                render(c) {
                    return c('router-view')
                }
            },
            children: [
                {
                    path: '404',
                    name: 'Page404',
                    component: Page404
                },
                {
                    path: '500',
                    name: 'Page500',
                    component: Page500
                },
                {
                    path: 'login',
                    name: 'Login',
                    component: Login
                },
            ]
        }
    ]
})
