import React, { useState, useRef, useCallback } from "react";
import Webcam from "react-webcam";
import axios from "axios";

function AgeVerificationModal({ onVerified, onSkip }) {
  const [isCapturing, setIsCapturing] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [verificationStep, setVerificationStep] = useState("");
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const webcamRef = useRef(null);

  const getSupportedAudioMimeType = () => {
    const types = [
      "audio/webm;codecs=opus",
      "audio/webm",
      "audio/mp4",
      "audio/ogg;codecs=opus",
    ];
    return types.find((type) => MediaRecorder.isTypeSupported(type)) || "";
  };

  const captureFacePrediction = useCallback(async () => {
    setVerificationStep("Capturing face...");
    setIsCapturing(true);
    try {
      const imageSrc = webcamRef.current.getScreenshot();
      if (!imageSrc) {
        throw new Error("Failed to capture image");
      }

      const response = await fetch(imageSrc);
      const blob = await response.blob();
      const formData = new FormData();
      formData.append("file", blob, "photo.jpg");

      setVerificationStep("Checking face age and gender...");
      const apiResponse = await axios.post(
        "http://localhost:8000/predict/both",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );

      return apiResponse.data;
    } finally {
      setIsCapturing(false);
    }
  }, []);

  const recordVoiceSample = useCallback(async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      throw new Error("Microphone access is not supported in this browser.");
    }

    if (!window.MediaRecorder) {
      throw new Error("Audio recording is not supported in this browser.");
    }

    setVerificationStep("Recording voice sample...");
    setIsRecording(true);

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mimeType = getSupportedAudioMimeType();
    const chunks = [];

    return new Promise((resolve, reject) => {
      let recorder;

      try {
        recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      } catch (e) {
        stream.getTracks().forEach((track) => track.stop());
        reject(new Error("Unable to start voice recording."));
        return;
      }

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };

      recorder.onerror = () => {
        stream.getTracks().forEach((track) => track.stop());
        setIsRecording(false);
        reject(new Error("Voice recording failed."));
      };

      recorder.onstop = () => {
        stream.getTracks().forEach((track) => track.stop());
        setIsRecording(false);

        if (!chunks.length) {
          reject(new Error("No voice audio captured."));
          return;
        }

        const blobType = mimeType || "audio/webm";
        resolve(new Blob(chunks, { type: blobType }));
      };

      recorder.start();
      setTimeout(() => {
        if (recorder.state !== "inactive") {
          recorder.stop();
        }
      }, 3500);
    });
  }, []);

  const predictVoice = useCallback(async (audioBlob) => {
    setVerificationStep("Analyzing voice...");
    const formData = new FormData();
    formData.append("file", audioBlob, "voice.webm");

    const apiResponse = await axios.post(
      "http://localhost:8000/predict/voice",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      },
    );

    return apiResponse.data;
  }, []);

  const captureAndVerify = useCallback(async () => {
    setError("");
    setResult(null);
    setIsVerifying(true);

    try {
      const faceData = await captureFacePrediction();
      if (faceData.predicted_age < 18) {
        throw new Error(
          "Access denied: face age check failed. You must be 18 or older.",
        );
      }

      const audioBlob = await recordVoiceSample();
      const voiceData = await predictVoice(audioBlob);

      if (voiceData.predicted_age < 18) {
        throw new Error(
          "Access denied: voice age check failed. You must be 18 or older.",
        );
      }

      const faceGender = String(faceData.gender || "").toLowerCase();
      const voiceGender = String(voiceData.gender_prediction || "").toLowerCase();
      if (
        faceGender &&
        voiceGender &&
        voiceGender !== "other" &&
        faceGender !== voiceGender
      ) {
        throw new Error(
          "Access denied: face and voice gender predictions do not match.",
        );
      }

      const combinedResult = {
        face: faceData,
        voice: voiceData,
        gender: faceData.gender,
      };

      setResult(combinedResult);
      setVerificationStep("Verification successful");

      setTimeout(() => {
        onVerified(combinedResult);
      }, 1800);
    } catch (err) {
      console.error("Verification error:", err);
      setVerificationStep("");
      setError(
        err.response?.data?.detail || err.message || "Verification failed. Please try again.",
      );
    } finally {
      setIsVerifying(false);
      setIsCapturing(false);
      setIsRecording(false);
    }
  }, [captureFacePrediction, onVerified, predictVoice, recordVoiceSample]);

  return (
    <div className="fixed inset-0 bg-black/95 flex items-center justify-center z-[2000] p-5">
      <div className="bg-gradient-to-br from-[#1a1a1a] to-[#2d2d2d] rounded-2xl max-w-2xl w-full shadow-2xl border-2 border-purple-500">
        <div className="text-center py-8 px-8 border-b border-gray-700">
          <h2 className="text-3xl font-bold mb-2 bg-gradient-to-r from-purple-500 to-purple-700 bg-clip-text text-transparent">
            🔞 Age Verification Required
          </h2>
          <p className="text-gray-400 text-sm">
            Face + voice verification is required (18+ only)
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
                <strong>Status:</strong> Face + voice verified (18+)
                <br />
                <strong>Face Age:</strong> {result.face.predicted_age} years
                <br />
                <strong>Voice Age Group:</strong> {result.voice.age_prediction}
                <br />
                <strong>Gender:</strong> {result.gender}
              </p>
              <p className="text-green-400 font-bold mt-3 animate-pulse">
                Access Granted! Redirecting...
              </p>
            </div>
          )}

          {verificationStep && isVerifying && (
            <div className="bg-blue-900/20 border-2 border-blue-600 text-blue-300 px-4 py-3 rounded-lg mb-5 text-center font-medium">
              {isRecording ? "🎤 " : "⏳ "}
              {verificationStep}
            </div>
          )}

          <div className="flex flex-col gap-3">
            <button
              className="bg-gradient-to-r from-purple-500 to-purple-700 text-white px-8 py-4 text-base font-bold rounded-lg transition-all hover:shadow-lg hover:-translate-y-0.5 disabled:opacity-60 disabled:cursor-not-allowed"
              onClick={captureAndVerify}
              disabled={isVerifying}
            >
              {isVerifying ? "🔄 Verifying..." : "📸 + 🎤 Verify With Face & Voice"}
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
            🔒 Your face and voice samples are processed for verification and not stored
          </p>
        </div>
      </div>
    </div>
  );
}

export default AgeVerificationModal;
