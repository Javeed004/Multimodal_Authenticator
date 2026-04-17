# Age Verification YouTube Clone (React + Tailwind CSS)

A modern React-based video platform with facial age verification using AI and styled with Tailwind CSS.

## 🚀 Features

- 🎥 **YouTube-like Interface** - Modern dark theme video grid
- 📸 **Real-time Facial Recognition** - Webcam-based age verification
- 🔐 **18+ Age Gate** - Blocks access for users under 18
- 🤖 **AI-Powered** - Integration with FastAPI backend
- 💾 **Session Storage** - No repeated verification needed
- 🎨 **Tailwind CSS** - Beautiful, responsive utility-first styling

## 📦 Installation

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Backend API

Make sure your FastAPI server is running:

```bash
# In the project root directory
cd ..
python app.py
```

The API should be accessible at `http://localhost:8000`

### 3. Start React App

```bash
npm start
```

Opens at `http://localhost:3000`

## 🎯 How It Works

1. **Initial Visit** → Age verification modal appears
2. **Camera Permission** → User grants webcam access
3. **Capture Photo** → Click button to take facial photo
4. **AI Processing** → Sends image to FastAPI backend
5. **Age Prediction** → AI model analyzes and predicts age/gender
6. **Access Decision**:
   - ✅ Age ≥ 18 → Access granted
   - ❌ Age < 18 → Access denied
7. **Session Persistence** → Verified users bypass future checks

## 🛠️ Tech Stack

- **React 18** - Frontend framework
- **Tailwind CSS** - Utility-first CSS framework
- **react-webcam** - Webcam capture component
- **axios** - HTTP client for API calls
- **FastAPI** - Backend API (Python)
- **TensorFlow** - AI model (backend)

## 📝 API Endpoints

- `POST /predict/both` - Predicts age and gender from facial image

## 🧪 Testing

Use the **"Skip (Testing Only)"** button to bypass verification during development.

## 🎨 Tailwind Configuration

The project uses custom Tailwind colors:

- Background: `#0f0f0f`
- Headers: `#212121`
- Accent: Purple gradient (`purple-500` to `purple-700`)

## 🔐 Security Notes

**This is a demo/prototype.** For production deployment:

- ✅ Add authentication & authorization
- ✅ Implement rate limiting
- ✅ Store verification audit logs
- ✅ Add liveness detection (prevent photo spoofing)
- ✅ Use HTTPS for all requests
- ✅ Configure proper CORS policies
- ✅ Add data privacy compliance (GDPR, CCPA)

## 📱 Responsive Design

Fully responsive grid layout:

- **Mobile**: 1 column
- **Tablet**: 2 columns
- **Desktop**: 3-4 columns

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
