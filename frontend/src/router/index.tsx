import { createBrowserRouter } from 'react-router-dom'

import App from '../App'
import Login from '../views/Login'
import Signup from '../views/Signup'
import AuthPage from '../views/AuthPage'
import NotFound from '../views/NotFound'

import AuthContextProvider from '../contexts/AuthContextProvider'
import LogoutPage from '../views/LogoutPage'

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
        path: '/logout',
        element: <LogoutPage />,
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
        path: '*',
        element: <NotFound />,
    },
])

export default router
