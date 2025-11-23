# AI Product Photo Background Changer

A full-stack web application that uses AI to automatically remove backgrounds from product photos and replace them with AI-generated professional backgrounds. Perfect for e-commerce product photography!

## 🎯 Features

- **Upload Product Photos**: Easy drag-and-drop or click-to-upload interface
- **AI Background Removal**: Automatically removes backgrounds from product images using advanced AI
- **AI Background Generation**: Generates professional, customizable backgrounds using DALL-E 3
- **Real-time Preview**: See your original and processed images side-by-side
- **Custom Context**: Provide context for background generation (e.g., "beach scene", "modern office")
- **Dark Theme UI**: Beautiful, modern dark-themed interface built with Tailwind CSS
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Tech Stack

### Frontend
- **React 19.2.0** - Modern UI library
- **Vite** - Fast build tool and dev server
- **Tailwind CSS 3.4** - Utility-first CSS framework (Dark theme)
- **JavaScript/JSX** - Frontend logic

### Backend
- **Django 5.1.4** - Python web framework
- **Django REST Framework** - Building RESTful APIs
- **OpenAI API (DALL-E 3)** - AI background generation
- **rembg** - AI-powered background removal
- **Pillow (PIL)** - Image processing
- **SQLite** - Database (default, can be changed)
- **django-cors-headers** - CORS handling for frontend-backend communication

### AI/ML Libraries
- **rembg** - Background removal using deep learning
- **onnxruntime** - Runtime for ML models
- **OpenAI SDK** - DALL-E 3 integration

## 📁 Project Structure

```
PhotoBackgroundChanger/
│
├── backend/
│   ├── PhotoBackgroundChanger/          # Django project root
│   │   ├── manage.py                    # Django management script
│   │   ├── db.sqlite3                   # SQLite database
│   │   ├── media/                       # Uploaded media files
│   │   │   └── photos/                  # User uploaded photos
│   │   ├── PhotoAnalyzer/               # Main Django app
│   │   │   ├── models.py                # Photo model
│   │   │   ├── views.py                 # API views (add, remove, generate)
│   │   │   ├── serializers.py           # DRF serializers
│   │   │   ├── urls.py                  # App URL routing
│   │   │   └── migrations/              # Database migrations
│   │   └── PhotoBackgroundChanger/      # Django settings
│   │       ├── settings.py              # Django configuration
│   │       ├── urls.py                  # Main URL routing
│   │       └── wsgi.py                  # WSGI config
│   └── requirements.txt                 # Python dependencies
│
├── frontend/
│   └── Photo-Background-Changer/        # React app
│       ├── src/
│       │   ├── App.jsx                  # Main React component
│       │   ├── main.jsx                 # React entry point
│       │   ├── index.css                # Global styles (Tailwind)
│       │   └── App.css                  # Component styles
│       ├── public/                      # Static assets
│       ├── package.json                 # Node dependencies
│       ├── vite.config.js               # Vite configuration
│       ├── tailwind.config.js           # Tailwind configuration
│       └── postcss.config.js            # PostCSS configuration
│
└── README.md                            # This file
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **npm** or **yarn** - Comes with Node.js
- **OpenAI API Key** - [Get API Key](https://platform.openai.com/api-keys)
- **Git** - [Download Git](https://git-scm.com/downloads)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd PhotoBackgroundChanger
```

### 2. Backend Setup

#### Navigate to backend directory:
```bash
cd backend
```

#### Create a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Python dependencies:
```bash
pip install -r requirements.txt
```

#### Create `.env` file:
Create a `.env` file in the `backend/PhotoBackgroundChanger/` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Important**: Replace `your_openai_api_key_here` with your actual OpenAI API key.

#### Run database migrations:
```bash
cd PhotoBackgroundChanger
python manage.py makemigrations
python manage.py migrate
```

### 3. Frontend Setup

#### Navigate to frontend directory:
```bash
cd ../frontend/Photo-Background-Changer
```

#### Install Node dependencies:
```bash
npm install
```

## ▶️ Running the Application

### Start the Backend Server

```bash
# From backend/PhotoBackgroundChanger directory
python manage.py runserver
```

The backend will run on `http://localhost:8000`

**Note**: On first run, `rembg` will download a model file (~170MB). This is automatic and only happens once.

### Start the Frontend Development Server

Open a new terminal:

```bash
# From frontend/Photo-Background-Changer directory
npm run dev
```

The frontend will run on `http://localhost:5173`

### Access the Application

Open your browser and navigate to: `http://localhost:5173`

## 📡 API Documentation

The backend provides three main API endpoints:

### Base URL
```
http://localhost:8000/api/v1/
```

### 1. Add Photo

Upload a product photo to the server.

**Endpoint**: `POST /api/v1/add-photo/`

**Request**:
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `photo` (file): Image file (jpg, jpeg, png, gif, webp)
  - Max file size: 10MB

**Response** (Success - 200):
```json
{
  "message": "Photo added successfully",
  "photo_id": 1
}
```

**Response** (Error - 400):
```json
{
  "message": "Photo not valid",
  "errors": {
    "photo": ["File type not supported. Allowed types: jpg, jpeg, png, gif, webp"]
  }
}
```

**Example** (using curl):
```bash
curl -X POST http://localhost:8000/api/v1/add-photo/ \
  -F "photo=@/path/to/your/image.jpg"
```

---

### 2. Remove Photo

Delete a photo from the server.

**Endpoint**: `DELETE /api/v1/remove-photo/`

**Request**:
- Method: `DELETE`
- Content-Type: `application/json`
- Body:
```json
{
  "photo_id": 1
}
```

**Response** (Success - 200):
```json
{
  "message": "Photo removed successfully"
}
```

**Response** (Error - 400):
```json
{
  "message": "Photo not found"
}
```

**Example** (using curl):
```bash
curl -X DELETE http://localhost:8000/api/v1/remove-photo/ \
  -H "Content-Type: application/json" \
  -d '{"photo_id": 1}'
```

---

### 3. Generate Background

Generate a new AI background and composite it with the product photo.

**Endpoint**: `POST /api/v1/generate-background/`

**Request**:
- Method: `POST`
- Content-Type: `application/json`
- Body:
```json
{
  "photo_id": 1,
  "context": "beach scene with palm trees"  // Optional
}
```

**Response** (Success - 200):
```json
{
  "background": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**Response** (Error - 400):
```json
{
  "message": "Photo ID not provided"
}
```

**Response** (Error - 404):
```json
{
  "message": "Photo not found"
}
```

**Response** (Error - 500):
```json
{
  "message": "Error generating background",
  "error": "OpenAI API error: ..."
}
```

**Example** (using curl):
```bash
curl -X POST http://localhost:8000/api/v1/generate-background/ \
  -H "Content-Type: application/json" \
  -d '{"photo_id": 1, "context": "modern office background"}'
```

---

## 🔄 How It Works

### Workflow

1. **User Uploads Photo**
   - User selects an image file through the frontend
   - Image is uploaded to the backend via `POST /api/v1/add-photo/`
   - Image is validated (file type, size)
   - Image is saved to the database and file system
   - Photo ID is returned to the frontend

2. **User Requests Background Generation**
   - User clicks "Generate Background" button
   - Optional: User provides context for the background
   - Frontend sends request to `POST /api/v1/generate-background/`

3. **Backend Processing** (3 steps):
   
   **Step 1: Background Removal**
   - Backend retrieves the uploaded photo
   - Uses `rembg` library to remove the background
   - Creates a transparent PNG of the product

   **Step 2: AI Background Generation**
   - Uses OpenAI DALL-E 3 API to generate a new background
   - Prompt includes user context (if provided)
   - Downloads the generated background image

   **Step 3: Image Compositing**
   - Uses Pillow (PIL) to composite the product (without background) onto the new background
   - Centers the product on the background
   - Converts to base64 format for frontend display

4. **Result Display**
   - Final composite image is returned as base64
   - Frontend displays the result in the "AI Generated Background" section
   - User can see side-by-side comparison

### Technical Details

- **Background Removal**: Uses `rembg` library which employs deep learning models (U²-Net) to detect and remove backgrounds
- **Background Generation**: Uses OpenAI's DALL-E 3 model to generate high-quality, context-aware backgrounds
- **Image Processing**: Uses Pillow for resizing, compositing, and format conversion
- **CORS**: Configured to allow frontend (localhost:5173) to communicate with backend (localhost:8000)

## 🎨 Frontend Features

- **Dark Theme**: Modern dark UI with Tailwind CSS
- **Responsive Design**: Works on all screen sizes
- **Image Preview**: Real-time preview of uploaded images
- **Loading States**: Visual feedback during processing
- **Error Handling**: User-friendly error messages
- **Context Input**: Optional text input for background customization

## 🔧 Configuration

### Backend Settings

Edit `backend/PhotoBackgroundChanger/PhotoBackgroundChanger/settings.py`:

- **CORS_ALLOWED_ORIGINS**: Add frontend URLs if deploying
- **MEDIA_ROOT**: Change media file storage location
- **ALLOWED_HOSTS**: Add your domain for production

### Frontend Configuration

Edit `frontend/Photo-Background-Changer/src/App.jsx`:

- **API Base URL**: Change `http://localhost:8000` to your backend URL

## 🐛 Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'rembg'`
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: `OPENAI_API_KEY is not set`
- **Solution**: Create `.env` file in `backend/PhotoBackgroundChanger/` with your API key

**Issue**: CORS errors
- **Solution**: Ensure `django-cors-headers` is installed and `CORS_ALLOWED_ORIGINS` includes your frontend URL

**Issue**: `rembg` model download fails
- **Solution**: Check internet connection. The model (~170MB) downloads automatically on first use.

### Frontend Issues

**Issue**: CSS not loading
- **Solution**: Ensure Tailwind CSS is properly configured. Run `npm install` again.

**Issue**: API requests failing
- **Solution**: Check that backend is running on `http://localhost:8000` and CORS is configured

**Issue**: Images not displaying
- **Solution**: Check browser console for errors. Ensure backend media files are accessible.

## 💰 Cost Considerations

### OpenAI API Costs (DALL-E 3)

- **Standard Quality (1024x1024)**: $0.040 per image
- **HD Quality (1024x1024)**: $0.080 per image
- **Standard Quality (1024x1792 or 1792x1024)**: $0.080 per image
- **HD Quality (1024x1792 or 1792x1024)**: $0.120 per image

**Note**: DALL-E 3 doesn't use tokens. Pricing is per image generated.

### Free Alternatives

For development/testing, consider:
- Using DALL-E 2 (cheaper but lower quality)
- Implementing a free background removal API
- Using local models for background removal (already using `rembg`)

## 📝 Environment Variables

Create a `.env` file in `backend/PhotoBackgroundChanger/`:

```env
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional (for production)
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🚀 Deployment

### Backend Deployment

1. Set `DEBUG=False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up static file serving
5. Configure environment variables on your hosting platform
6. Use a production WSGI server (Gunicorn, uWSGI)

### Frontend Deployment

1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Deploy the `dist/` folder to a static hosting service (Vercel, Netlify, etc.)
3. Update API URLs in `App.jsx` to point to your production backend

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 👨‍💻 Author

Created with ❤️ for AI-powered product photography

## 🙏 Acknowledgments

- OpenAI for DALL-E 3 API
- rembg project for background removal
- Django and React communities

---

**Happy Coding! 🚀**

