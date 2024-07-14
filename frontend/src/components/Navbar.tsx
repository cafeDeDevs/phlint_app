import { useState } from 'react'
import ProfileCard from './ProfileCard'
import '../css/Navbar.css'

const Navbar = () => {
    const [displayProfileCard, setProfileCard] = useState<boolean>(false)

    return (
        <>
            <div className='nav-container'>
                <nav className='navbar'>
                    <button
                        id='hamburger-btn'
                        onClick={() => {
                            setProfileCard(!displayProfileCard)
                        }}>
                        <svg
                            id='hamburger-icon'
                            xmlns='http://www.w3.org/2000/svg'
                            width='2em'
                            height='2em'
                            viewBox='0 0 48 48'>
                            <g
                                fill='none'
                                stroke='#000'
                                strokeLinecap='round'
                                strokeLinejoin='round'
                                strokeWidth='4'>
                                <path d='M7.94971 11.9497H39.9497' />
                                <path d='M7.94971 23.9497H39.9497' />
                                <path d='M7.94971 35.9497H39.9497' />
                            </g>
                        </svg>
                    </button>
                    {displayProfileCard && <ProfileCard />}
                </nav>
            </div>
        </>
    )
}

export default Navbar
