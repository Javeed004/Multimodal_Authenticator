import React, { useState, useRef, useCallback } from "react";
import Webcam from "react-webcam";
import axios from "axios";

function AgeVerificationModal({ onVerified, onSkip }) {
  const [isCapturing, setIsCapturing] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const webcamRef = useRef(null);

  const captureAndVerify = useCallback(async () => {
    setError("");
    setIsCapturing(true);
    setIsVerifying(true);

    try {
      // Capture image from webcam
      const imageSrc = webcamRef.current.getScreenshot();

      if (!imageSrc) {
        throw new Error("Failed to capture image");
      }

      // Convert base64 to blob
      const response = await fetch(imageSrc);
      const blob = await response.blob();

      // Create form data
      const formData = new FormData();
      formData.append("file", blob, "photo.jpg");

      // Send to API
      const apiResponse = await axios.post(
        "http://localhost:8000/predict/both",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );

      const data = apiResponse.data;
      setResult(data);

      // Check if age is 18 or above
      if (data.predicted_age >= 18) {
        setTimeout(() => {
          onVerified(data);
        }, 2000);
      } else {
        setError(
          "Access Denied: You must be 18 or older to access this content.",
        );
      }
    } catch (err) {
      console.error("Verification error:", err);
      setError(
        err.response?.data?.detail || "Verification failed. Please try again.",
      );
    } finally {
      setIsVerifying(false);
      setIsCapturing(false);
    }
  }, [onVerified]);

  return (
    <div className="fixed inset-0 bg-black/95 flex items-center justify-center z-[2000] p-5">
      <div className="bg-gradient-to-br from-[#1a1a1a] to-[#2d2d2d] rounded-2xl max-w-2xl w-full shadow-2xl border-2 border-purple-500">
        <div className="text-center py-8 px-8 border-b border-gray-700">
          <h2 className="text-3xl font-bold mb-2 bg-gradient-to-r from-purple-500 to-purple-700 bg-clip-text text-transparent">
            🔞 Age Verification Required
          </h2>
          <p className="text-gray-400 text-sm">
            This content is restricted to users 18 years and older
          </p>
        </div>

        <div className="p-8">
          <div className="w-full max-w-2xl mx-auto mb-5 rounded-xl overflow-hidden bg-black shadow-lg">
            {!isCapturing && (
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                className="w-full h-auto block"
                videoConstraints={{
                  width: 640,
                  height: 480,
                  facingMode: "user",
                }}
              />
            )}
            {isCapturing && (
              <div className="w-full aspect-[4/3]">
                <img
                  src={webcamRef.current?.getScreenshot()}
                  alt="Captured"
                  className="w-full h-full object-cover"
                />
              </div>
            )}
          </div>

          {error && (
            <div className="bg-red-900/20 border-2 border-red-600 text-red-400 px-4 py-4 rounded-lg mb-5 text-center font-medium">
              ⚠️ {error}
            </div>
          )}

          {result && !error && (
            <div className="bg-green-900/20 border-2 border-green-600 text-green-400 px-5 py-5 rounded-lg mb-5 text-center">
              <h3 className="text-xl font-bold mb-4">
                ✓ Verification Successful
              </h3>
              <p className="text-white leading-7 mb-3">
                <strong>Status:</strong> Age verified (18+)
                <br />
                <strong>Gender:</strong> {result.gender}
              </p>
              <p className="text-green-400 font-bold mt-3 animate-pulse">
                Access Granted! Redirecting...
              </p>
            </div>
          )}

          <div className="flex flex-col gap-3">
            <button
              className="bg-gradient-to-r from-purple-500 to-purple-700 text-white px-8 py-4 text-base font-bold rounded-lg transition-all hover:shadow-lg hover:-translate-y-0.5 disabled:opacity-60 disabled:cursor-not-allowed"
              onClick={captureAndVerify}
              disabled={isVerifying}
            >
              {isVerifying ? "🔄 Verifying..." : "📸 Capture & Verify Age"}
            </button>
            <button
              className="bg-transparent text-gray-500 border border-gray-600 px-6 py-3 text-sm rounded-lg transition-all hover:border-gray-500 hover:text-gray-400 disabled:opacity-40 disabled:cursor-not-allowed"
              onClick={onSkip}
              disabled={isVerifying}
            >
              Skip (Testing Only)
            </button>
          </div>
        </div>

        <div className="py-5 px-8 border-t border-gray-700 text-center">
          <p className="text-gray-500 text-xs">
            🔒 Your image is processed securely and not stored on our servers
          </p>
        </div>
      </div>
    </div>
  );
}

export default AgeVerificationModal;
