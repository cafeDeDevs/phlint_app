/* TODO: Rename this view as something closer to Phlint or PhlintApp
 * as it is not just the gallery, but the application itself after login */
import '../App.css'
import { ChangeEvent, useEffect, useRef, useState } from 'react'
import Navbar from '../components/Navbar'

import urls from '../config/urls'

/* TODO: Display Spinner Animation While User Waits for Images To Load */
/* TODO: Cache Around 20 Images Client Side Before Asking For More From Server */
/* TODO: Implement Intersection Observer Pattern whereby more images are loaded as user scrolls page */
const Gallery = () => {
    const [files, setFiles] = useState<File[]>([])
    const [errorMsg, setErrorMsg] = useState<string | null>(null)
    const [images, setImages] = useState<string[]>([])
    const inputRef = useRef<HTMLInputElement | null>(null)
    const [galleryUpdated, setGalleryUpdated] = useState<boolean>(false)

    useEffect(() => {
        const grabGallery = async (): Promise<void> => {
            try {
                const galleryRes = await fetch(urls.BACKEND_GALLERY_ROUTE, {
                    method: 'GET',
                    credentials: 'include',
                })
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
    }, [galleryUpdated])

    useEffect(() => {
        if (!files.length) return
        const imageData = new FormData()
        files.forEach((file, i) => {
            imageData.append(`file-${i}`, file, file.name)
        })
        const uploadImage = async (): Promise<void> => {
            try {
                const uploadImageRes = await fetch(
                    urls.BACKEND_UPLOAD_IMAGE_ROUTE,
                    {
                        method: 'POST',
                        credentials: 'include',
                        body: imageData,
                    },
                )
                const jsonRes = await uploadImageRes.json()
                if (!uploadImageRes.ok) throw new Error(jsonRes.message)
                setGalleryUpdated((prev) => !prev)
            } catch (err) {
                if (err instanceof Error) {
                    console.error('ERROR :=>', err.message)
                    setErrorMsg(err.message)
                }
            }
        }
        uploadImage()
        setFiles([])
    }, [files])

    const handleUploadClick = (): void => {
        inputRef.current?.click()
    }

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>): void => {
        if (e.target.files) {
            setFiles([...files, e.target.files[0]])
        }
    }

    return (
        <>
            <div className='phlint-app'>
                <Navbar />
                {/* TODO: Using the key as an index is bad security practice, change way key is defined...*/}
                {/* TODO: Provide Better Accessibility Descriptions For Images (defined by user upon upload)*/}
                <div className='gallery'>
                    {/* TODO: Move this into own modal/component */}
                    {/* TODO: Handle Parent/Child Event Bubbling */}
                    <div className='upload-form'>
                        <input
                            className='file-picker'
                            type='file'
                            accept='image/*'
                            onChange={handleFileChange}
                            ref={inputRef}
                        />
                        <button
                            className='upload-btn'
                            onClick={handleUploadClick}>
                            Upload Image
                        </button>
                    </div>
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
