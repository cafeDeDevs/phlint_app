/* TODO: Rename this view as something closer to Phlint or PhlintApp
 * as it is not just the gallery, but the application itself after login */
import '../App.css'
import { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'

/* TODO: Display Spinner Animation While User Waits for Images To Load */
/* TODO: Cache Around 20 Images Client Side Before Asking For More From Server */
/* TODO: Implement Intersection Observer Pattern whereby more images are loaded as user scrolls page */
const Gallery = () => {
    const [images, setImages] = useState<string[]>([])
    const [errorMsg, setErrorMsg] = useState<string | null>(null)

    useEffect(() => {
        const grabGallery = async (): Promise<void> => {
            try {
                const galleryRes = await fetch(
                    import.meta.env.VITE_BACKEND_GALLERY_ROUTE,
                    {
                        method: 'GET',
                        credentials: 'include',
                    },
                )
                if (!galleryRes.ok)
                    throw new Error(
                        'An Error Occurred While Trying To Retrieve Your Gallery',
                    )
                const { imagesAsBase64 } = await galleryRes.json()
                setImages(imagesAsBase64)
            } catch (err) {
                if (err instanceof Error) {
                    console.error('ERROR :=>', err.message)
                    setErrorMsg(err.message)
                }
            }
        }
        grabGallery()
    }, [])
    return (
        <>
            <div className='phlint-app'>
                <Navbar />
                {/* TODO: Using the key as an index is bad security practice, change way key is defined...*/}
                {/* TODO: Provide Better Accessibility Descriptions For Images (defined by user upon upload)*/}
                <div className='gallery'>
                    {images.map((image, index) => (
                        <img
                            key={index}
                            src={`data:image/jpg;base64,${image}`}
                            alt={`Gallery Image ${index + 1}`}
                        />
                    ))}
                </div>
                {errorMsg && <p>{errorMsg}</p>}
            </div>
        </>
    )
}
export default Gallery
