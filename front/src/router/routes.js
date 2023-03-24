const routes = [
  {
    path: '/login',
    component: () => import('pages/Login.vue'), name: 'Login',
  },
  {
    path: '/',
    component: () => import('layouts/MainMenuLayout.vue'),
    name: 'Home',
    children: [
      {path: '', component: () => import('pages/ProgramDescription.vue'), name: 'Description'},
      {path: '/phones', component: () => import('pages/Phones.vue'), name: 'Phones'},
      {path: '/training', component: ()=> import('pages/TrainingPage.vue'), name: 'Training'},
      {path: '/settings', component: ()=> import('pages/SettingsPage.vue'), name: 'Settings'},
    ],
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
