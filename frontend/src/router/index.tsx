import { createBrowserRouter } from 'react-router-dom'

import App from '../App'
import AuthPage from '../views/AuthPage'
import Gallery from '../views/Gallery'
import Login from '../views/Login'
import Signup from '../views/Signup'
import NotFound from '../views/NotFound'

import EmailRegistration from '../views/EmailRegistration'

import AuthContextProvider from '../contexts/AuthContextProvider'

const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
    },
    {
        path: '/signup',
        element: <Signup />,
    },
    {
        path: '/login',
        element: <Login />,
    },
    {
        path: '/auth',
        element: (
            <AuthContextProvider>
                <AuthPage />
            </AuthContextProvider>
        ),
    },
    {
        path: '/gallery',
        element: (
            <AuthContextProvider>
                <Gallery />
            </AuthContextProvider>
        ),
    },
    {
        path: '*',
        element: <NotFound />,
    },
    {
        path: '/email-registration',
        element: <EmailRegistration />,
    },
])

export default router
