import { useState, useRef } from 'react'
import './App.css'

function App() {
  const [originalImage, setOriginalImage] = useState(null)
  const [processedImage, setProcessedImage] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [photoId, setPhotoId] = useState(null)
  const [context, setContext] = useState('')
  const fileInputRef = useRef(null)

  const handleAddPhoto = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0]
    if (file) {
      if (file.type.startsWith('image/')) {
        // Display image preview
        const reader = new FileReader()
        reader.onloadend = () => {
          setOriginalImage(reader.result)
          setProcessedImage(null)
          setError(null)
        }
        reader.readAsDataURL(file)

        // Upload photo to backend
        try {
          const formData = new FormData()
          formData.append('photo', file)

          const response = await fetch('http://localhost:8000/api/v1/add-photo/', {
            method: 'POST',
            body: formData,
          })

          if (!response.ok) {
            throw new Error('Failed to upload photo')
          }

          const data = await response.json()
          if (data.photo_id) {
            setPhotoId(data.photo_id)
          }
        } catch (err) {
          setError(err.message || 'Error uploading photo')
          console.error('Error:', err)
        }
      } else {
        setError('Please select a valid image file')
      }
    }
  }

  const handleRemovePhoto = async () => {
    // Remove photo from backend if photoId exists
    if (photoId) {
      try {
        await fetch('http://localhost:8000/api/v1/remove-photo/', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ photo_id: photoId }),
        })
      } catch (err) {
        console.error('Error removing photo from backend:', err)
      }
    }

    setOriginalImage(null)
    setProcessedImage(null)
    setError(null)
    setPhotoId(null)
    setContext('')
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleGenerateBackground = async () => {
    if (!originalImage || !photoId) {
      setError('Please upload an image first')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const apiResponse = await fetch('http://localhost:8000/api/v1/generate-background/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          photo_id: photoId,
          context: context || null,
        }),
      })

      if (!apiResponse.ok) {
        const errorData = await apiResponse.json()
        throw new Error(errorData.message || 'Failed to generate background')
      }

      const data = await apiResponse.json()
      
      // If the API returns a URL or base64 image
      if (data.background) {
        setProcessedImage(data.background)
      } else {
        throw new Error('No background image received')
      }
    } catch (err) {
      setError(err.message || 'Error generating background. Please try again.')
      console.error('Error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            AI Product Photo Background Changer
          </h1>
          <p className="text-gray-400">
            Upload a product photo and let AI transform the background
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-6xl mx-auto">
          {/* Image Display Area */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* Original Image */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-xl font-semibold mb-4 text-gray-300">Original Photo</h2>
              <div className="relative aspect-square bg-gray-900 rounded-lg border-2 border-dashed border-gray-700 flex items-center justify-center overflow-hidden">
                {originalImage ? (
                  <img
                    src={originalImage}
                    alt="Original"
                    className="w-full h-full object-contain"
                  />
                ) : (
                  <div className="text-center text-gray-500">
                    <svg
                      className="w-16 h-16 mx-auto mb-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                    <p>No image uploaded</p>
                  </div>
                )}
              </div>
            </div>

            {/* Processed Image */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-xl font-semibold mb-4 text-gray-300">AI Generated Background</h2>
              <div className="relative aspect-square bg-gray-900 rounded-lg border-2 border-dashed border-gray-700 flex items-center justify-center overflow-hidden">
                {isLoading ? (
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
                    <p className="text-gray-400">Generating background...</p>
                  </div>
                ) : processedImage ? (
                  <img
                    src={processedImage}
                    alt="Processed"
                    className="w-full h-full object-contain"
                  />
                ) : (
                  <div className="text-center text-gray-500">
                    <svg
                      className="w-16 h-16 mx-auto mb-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                      />
                    </svg>
                    <p>Generated image will appear here</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Context Input */}
          {originalImage && (
            <div className="mb-6 bg-gray-800 rounded-lg p-6 border border-gray-700">
              <label htmlFor="context" className="block text-sm font-medium text-gray-300 mb-2">
                Background Context (Optional)
              </label>
              <input
                id="context"
                type="text"
                value={context}
                onChange={(e) => setContext(e.target.value)}
                placeholder="e.g., beach scene with palm trees, modern office, nature background..."
                className="w-full px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="mt-2 text-xs text-gray-400">
                Describe the background you want AI to generate. Leave empty for AI to decide.
              </p>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mb-6 bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-wrap gap-4 justify-center">
            <button
              onClick={handleAddPhoto}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors duration-200 flex items-center gap-2 shadow-lg shadow-blue-500/20"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4v16m8-8H4"
                />
              </svg>
              Add Photo
            </button>

            <button
              onClick={handleRemovePhoto}
              disabled={!originalImage}
              className="px-6 py-3 bg-red-600 hover:bg-red-700 disabled:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-50 text-white font-semibold rounded-lg transition-colors duration-200 flex items-center gap-2 shadow-lg shadow-red-500/20"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
              Remove Photo
            </button>

            <button
              onClick={handleGenerateBackground}
              disabled={!originalImage || isLoading}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-700 disabled:to-gray-700 disabled:cursor-not-allowed disabled:opacity-50 text-white font-semibold rounded-lg transition-all duration-200 flex items-center gap-2 shadow-lg shadow-purple-500/20"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Generating...
                </>
              ) : (
                <>
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                    />
                  </svg>
                  Generate Background
                </>
              )}
            </button>
          </div>

          {/* Hidden File Input */}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="hidden"
          />
        </div>
      </div>
    </div>
  )
}

export default App
