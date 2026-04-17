import React from "react";

function Header({ onLogout, isVerified }) {
  return (
    <header className="flex justify-between items-center px-4 py-3 bg-[#212121] sticky top-0 z-[1000] shadow-lg">
      <div className="flex items-center gap-4">
        <button className="text-white text-2xl p-2 hover:bg-gray-700 rounded-full transition">
          ☰
        </button>
        <div className="flex items-center gap-2 text-xl font-bold">
          <span className="text-red-600 text-3xl">▶</span>
          <span className="text-white tracking-tight">ViewTube</span>
        </div>
      </div>

      <div className="flex-1 max-w-2xl mx-10">
        <div className="flex items-center bg-[#121212] border border-[#303030] rounded-full overflow-hidden">
          <input
            type="text"
            placeholder="Search"
            className="flex-1 bg-transparent border-none px-4 py-3 text-white text-base outline-none"
          />
          <button className="bg-[#303030] px-5 py-3 text-lg hover:bg-[#404040] transition">
            🔍
          </button>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="text-white text-2xl p-2 hover:bg-gray-700 rounded-full transition">
          📹
        </button>
        <button className="text-white text-2xl p-2 hover:bg-gray-700 rounded-full transition">
          🔔
        </button>
        <button className="bg-gradient-to-br from-purple-500 to-purple-700 text-white text-2xl w-10 h-10 rounded-full flex items-center justify-center hover:shadow-lg transition">
          👤
        </button>
        {isVerified && (
          <button
            onClick={onLogout}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-semibold transition flex items-center gap-2"
            title="Logout"
          >
            🚪 Logout
          </button>
        )}
      </div>
    </header>
  );
}

export default Header;
