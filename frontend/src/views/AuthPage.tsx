import { useNavigate } from 'react-router-dom'

const AuthPage = () => {
    const navigate = useNavigate()

    const logout = async () => {
        console.log('Logout button clicked')
        const accessToken = localStorage.getItem('access_token')
        console.log('Retrieved access token:', accessToken)

        if (!accessToken) {
            console.log('No access token found')
            return
        }

        try {
            console.log('Attempting to call fetch API for logout...')
            const response = await fetch('http://localhost:8000/api/logout/', {
                method: 'POST',
                headers: {
                    Authorization: `Token ${accessToken}`,
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            })

            console.log('Logout response status:', response.status)
            if (response.ok) {
                const data = await response.json()
                console.log(data.message)
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                alert('Logout success')
                navigate('/logout')
            } else {
                const errorDataMessage = await response.json()
                console.error('Logout unsuccessful', errorDataMessage)
                alert('Logout unsuccessful')
            }
        } catch (error) {
            console.error('Error!:', error)
            alert('Error')
        }
    }

    return (
        <>
            <div>Congratulations! You Are Authenticated!</div>
            <button onClick={logout}>LOGOUT</button>
        </>
    )
}

export default AuthPage

// import React from 'react'
// import { useNavigate } from 'react-router-dom'

// const AuthPage = () => {
//     const navigate = useNavigate()

//     const logout = async () => {
//         console.log('Logout function called successfully')
//         const accessToken = localStorage.getItem('access_token')
//         console.log('Retrieved access token:', accessToken)

//         if (!accessToken) {
//             console.log('No access token found')
//             return
//         }

//         try {
//             console.log('Attempting to call fetch API for logout...')
//             const response = await fetch('http://localhost:8000/api/logout/', {
//                 method: 'POST',
//                 headers: {
//                     Authorization: `Token ${accessToken}`,
//                     'Content-Type': 'application/json',
//                 },
//                 credentials: 'include',
//             })

//             console.log('Logout response status:', response.status)
//             if (response.ok) {
//                 const data = await response.json()
//                 console.log(data.message)
//                 localStorage.removeItem('access_token')
//                 localStorage.removeItem('refresh_token')
//                 alert('Logout success')
//                 navigate('/logout')
//             } else {
//                 const errorDataMessage = await response.json()
//                 console.error('Logout unsuccessful', errorDataMessage)
//                 alert('Logout unsuccessful')
//             }
//         } catch (error) {
//             console.error('Error!:', error)
//             alert('Error')
//         }
//     }

//     return (
//         <>
//             <div>Congratulations! You Are Authenticated!</div>
//             <button
//                 onClick={() => {
//                     console.log('Logout button clicked')
//                     logout()
//                 }}>
//                 LOGOUT
//             </button>
//         </>
//     )
// }

// export default AuthPage
