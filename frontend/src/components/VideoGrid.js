import React from "react";
import VideoCard from "./VideoCard";

// Dummy video data
const dummyVideos = [
  {
    id: 1,
    thumbnail: "https://picsum.photos/seed/video1/320/180",
    title: "Introduction to Machine Learning - Full Course",
    channel: "Tech Academy",
    views: "1.2M",
    uploadTime: "3 days ago",
    duration: "12:45",
  },
  {
    id: 2,
    thumbnail: "https://picsum.photos/seed/video2/320/180",
    title: "Building a REST API with FastAPI",
    channel: "Code Masters",
    views: "850K",
    uploadTime: "1 week ago",
    duration: "25:30",
  },
  {
    id: 3,
    thumbnail: "https://picsum.photos/seed/video3/320/180",
    title: "React Hooks Explained",
    channel: "Web Dev Pro",
    views: "2.1M",
    uploadTime: "2 weeks ago",
    duration: "18:22",
  },
  {
    id: 4,
    thumbnail: "https://picsum.photos/seed/video4/320/180",
    title: "Deep Learning for Computer Vision",
    channel: "AI Research Lab",
    views: "670K",
    uploadTime: "5 days ago",
    duration: "45:10",
  },
  {
    id: 5,
    thumbnail: "https://picsum.photos/seed/video5/320/180",
    title: "CSS Grid Layout Tutorial",
    channel: "Design Code",
    views: "950K",
    uploadTime: "1 month ago",
    duration: "15:48",
  },
  {
    id: 6,
    thumbnail: "https://picsum.photos/seed/video6/320/180",
    title: "Python Data Science Complete Guide",
    channel: "Data Science Hub",
    views: "1.8M",
    uploadTime: "2 months ago",
    duration: "2:15:30",
  },
  {
    id: 7,
    thumbnail: "https://picsum.photos/seed/video7/320/180",
    title: "Advanced JavaScript Patterns",
    channel: "JS Ninjas",
    views: "520K",
    uploadTime: "1 week ago",
    duration: "32:15",
  },
  {
    id: 8,
    thumbnail: "https://picsum.photos/seed/video8/320/180",
    title: "Docker and Kubernetes Essentials",
    channel: "DevOps Daily",
    views: "1.5M",
    uploadTime: "3 weeks ago",
    duration: "42:00",
  },
  {
    id: 9,
    thumbnail: "https://picsum.photos/seed/video9/320/180",
    title: "TensorFlow 2.0 Complete Course",
    channel: "ML Academy",
    views: "890K",
    uploadTime: "4 days ago",
    duration: "1:28:45",
  },
  {
    id: 10,
    thumbnail: "https://picsum.photos/seed/video10/320/180",
    title: "Building Scalable Node.js Apps",
    channel: "Backend Masters",
    views: "720K",
    uploadTime: "2 weeks ago",
    duration: "38:20",
  },
  {
    id: 11,
    thumbnail: "https://picsum.photos/seed/video11/320/180",
    title: "Vue.js 3 Composition API",
    channel: "Vue Community",
    views: "640K",
    uploadTime: "1 month ago",
    duration: "28:55",
  },
  {
    id: 12,
    thumbnail: "https://picsum.photos/seed/video12/320/180",
    title: "Database Design Best Practices",
    channel: "Database Pro",
    views: "1.1M",
    uploadTime: "2 days ago",
    duration: "22:10",
  },
];

function VideoGrid() {
  const userAge = sessionStorage.getItem("userAge");
  const userGender = sessionStorage.getItem("userGender");

  return (
    <div className="p-5">
      {userAge && (
        <div className="bg-gradient-to-r from-purple-500 to-purple-700 text-white px-5 py-3 rounded-lg mb-5 text-center font-medium shadow-lg">
          ✓ Age Verified: {Math.round(userAge)} years old ({userGender})
        </div>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
        {dummyVideos.map((video) => (
          <VideoCard key={video.id} video={video} />
        ))}
      </div>
    </div>
  );
}

export default VideoGrid;
