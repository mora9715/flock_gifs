import VueRouter from 'vue-router'

import All from '../components/All'
import Featured from '../components/Featured'
import Info from '../components/Info'
import UploadForm from '../components/UploadForm'
import Error from '../components/Error'
import Settings from '../components/Settings'

const router = new VueRouter({
  routes: [
    {
      path: '/',
      component: All,
      name: 'home',
      props: true
    },
    {
      path: '/featured',
      component: Featured,
      name: 'featured',
      props: true
    },
    {
      path: '/upload',
      component: UploadForm,
      name: 'upload',
      props: true
    },
    {
      path: '/info',
      component: Info,
      name: 'info',
      props: true
    },
    {
      path: '/error',
      component: Error,
      name: 'error',
      props: true
    },
    {
      path: '/settings',
      component: Settings,
      name: 'settings',
      props: true
    }
  ],
  // mode: 'history'
});

export default router;