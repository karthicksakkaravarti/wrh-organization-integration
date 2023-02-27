const setup = [
  {
    path: '/setup',
    redirect: '/setup/portalsetings',
  },
  {
    path: '/setup/portalsetings',
    component: () => import('@/views/Setup/UserProfile.vue'),
    name: 'Portal Settings',
    meta: {
      layout: 'SetupLayout',
    },
  },
  {
    path: '/setup/authentication',
    component: () => import('@/views/Setup/Authentication.vue'),
    name: 'Authentication Settings',
    meta: {
      layout: 'SetupLayout',
    },
  },
  {
    path: '/setup/layout/form_edit/:form/:id',
    component: () => import('@/views/Setup/Layout/FormEdit.vue'),
    name: 'Form Edit',
    meta: {
      layout: 'SetupLayout',
    },
  },
  // Email Services
  // {
  //   path: '/setup/services/email/email_template',
  //   component: () => import('@/views/Setup/services/email/EmailTemplate.vue'),
  //   name: 'Email Template',
  //   meta: {
  //     layout: 'setup',
  //   },
  // },
]
export default setup
