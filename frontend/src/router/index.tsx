import { createBrowserRouter } from 'react-router-dom'

import App from '../App'
import Signup from '../views/Signup'
import Login from '../views/Login'
import EmailRegistration from '../views/EmailRegistration'
import AuthPage from '../views/AuthPage'
import Gallery from '../views/Gallery'
import Onboarding from '../views/Onboarding.tsx'
import NotFound from '../views/NotFound'

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
        path: '/email-registration',
        element: <EmailRegistration />,
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
        path: '/onboarding',
        element: <Onboarding />,
    },
    {
        path: '*',
        element: <NotFound />,
    },
])

export default router
