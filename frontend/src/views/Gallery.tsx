import { useEffect, useState } from 'react'

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
            <div>Your Gallery</div>
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
        </>
    )
}
export default Gallery
