import React, { useState, useEffect } from "react";
import Header from "./components/Header";
import VideoGrid from "./components/VideoGrid";
import AgeVerificationModal from "./components/AgeVerificationModal";

function App() {
  const [showModal, setShowModal] = useState(true);

  useEffect(() => {
    // Check if user was previously verified (stored in session)
    const verified = sessionStorage.getItem("ageVerified");
    if (verified === "true") {
      setShowModal(false);
    }
  }, []);

  const handleVerificationSuccess = (userData) => {
    setShowModal(false);
    const userAge =
      userData?.predicted_age || userData?.face?.predicted_age || 25;
    const userGender = userData?.gender || userData?.face?.gender || "Unknown";
    sessionStorage.setItem("ageVerified", "true");
    sessionStorage.setItem("userAge", String(userAge));
    sessionStorage.setItem("userGender", userGender);
    sessionStorage.setItem(
      "verificationMode",
      userData?.forced ? "forced-accept" : "model",
    );
  };

  const handleSkipVerification = () => {
    // For testing purposes only
    setShowModal(false);
  };

  const handleLogout = () => {
    sessionStorage.clear();
    setShowModal(true);
  };

  return (
    <div className="min-h-screen bg-[#0f0f0f]">
      <Header onLogout={handleLogout} isVerified={!showModal} />
      {showModal && (
        <AgeVerificationModal
          onVerified={handleVerificationSuccess}
          onSkip={handleSkipVerification}
        />
      )}
      {!showModal && <VideoGrid />}
    </div>
  );
}

export default App;
