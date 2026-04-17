import React from "react";

function VideoCard({ video }) {
  return (
    <div className="cursor-pointer transition-transform hover:scale-105">
      <div className="relative w-full pb-[56.25%] bg-[#1a1a1a] rounded-xl overflow-hidden">
        <img
          src={video.thumbnail}
          alt={video.title}
          className="absolute top-0 left-0 w-full h-full object-cover"
        />
        <span className="absolute bottom-2 right-2 bg-black/80 text-white px-2 py-1 rounded text-xs font-bold">
          {video.duration}
        </span>
      </div>
      <div className="flex gap-3 mt-3">
        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-purple-500 to-purple-700 flex items-center justify-center text-white font-bold flex-shrink-0">
          {video.channel[0]}
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-white text-sm font-medium leading-5 mb-1 line-clamp-2">
            {video.title}
          </h3>
          <p className="text-gray-400 text-xs mb-1">{video.channel}</p>
          <p className="text-gray-400 text-xs">
            {video.views} views • {video.uploadTime}
          </p>
        </div>
      </div>
    </div>
  );
}

export default VideoCard;
