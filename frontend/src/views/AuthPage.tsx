import React from 'react'
import { useNavigate } from 'react-router-dom'

const AuthPage = () => {
    const navigate = useNavigate()

    const testNavigation = () => {
        console.log('Test navigation to /logout')
        navigate('/logout')
    }

    const logout = async () => {
        console.log('Logout function called successfully')
        const accessToken = localStorage.getItem('access_token')
        console.log('Retrieved access token:', accessToken)

        if (!accessToken) {
            console.log('No access token found')
            return
        }

        try {
            console.log('Sending fetch request')
            const response = await fetch('http://localhost:8000/api/logout/', {
                method: 'POST',
                headers: {
                    Authorization: `Token ${accessToken}`,
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            })
            console.log('Fetch request completed')

            if (response.ok) {
                const data = await response.json()
                console.log('Logout response data:', data)
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                alert('Logout success')
                console.log('TRYING TO NAVIGATE TO LOGOUT')
                navigate('/logout')
            } else {
                const errorDataMessage = await response.json()
                console.error('Logout unsuccessful', errorDataMessage)
                alert('Logout unsuccessful')
            }
        } catch (error) {
            console.error('Error during logout:', error)
            alert('Error')
        }
    }

    return (
        <>
            <div>Congratulations! You Are Authenticated!</div>
            <button onClick={logout}>LOGOUT</button>
            <button onClick={testNavigation}>Test Navigation</button>
        </>
    )
}

export default AuthPage
