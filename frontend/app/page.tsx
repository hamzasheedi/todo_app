'use client';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0B0F1A] via-[#0E1424] to-[#090C16] text-white overflow-hidden">
      {/* Background glow effects */}
      <div className="fixed inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-[rgba(0,245,255,0.05)] rounded-full blur-3xl"></div>
        <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-[rgba(176,38,255,0.05)] rounded-full blur-3xl"></div>
      </div>

      <div className="relative z-10 container mx-auto px-6 py-12 min-h-screen flex flex-col items-center justify-center">
        {/* Hero Section */}
        <div className="max-w-2xl w-full text-center">
          <div className="text-2xl font-bold mb-8 flex items-center justify-center">
            <span className="text-[#00F5FF] mr-2">✓</span>
            <span className="text-white">TaskFlow</span>
          </div>

          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
            <span className="block text-[#F5F7FA] mb-2">Organize your tasks.</span>
            <span className="block text-[#F5F7FA] mb-2">Stay focused.</span>
            <span className="block text-[#F5F7FA] relative">
              Get things done.
              <span className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-[#00F5FF] to-[#B026FF] opacity-70"></span>
            </span>
          </h1>

          <p className="text-lg text-[#AAB0C0] mb-12 leading-relaxed max-w-lg mx-auto">
            A modern productivity app designed to help you manage your tasks efficiently with a sleek, futuristic interface that keeps you motivated and on track.
          </p>

          {/* Feature Highlights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-[#11162A] bg-opacity-60 backdrop-blur-sm rounded-xl border border-gray-700 p-6 hover:border-[#00F5FF]/50 transition-all duration-300">
              <div className="text-[#00F5FF] text-2xl mb-3">✓</div>
              <h3 className="text-[#F5F7FA] font-medium mb-2">Task Management</h3>
              <p className="text-[#AAB0C0] text-sm">Simple and clean interface to organize your daily tasks</p>
            </div>
            <div className="bg-[#11162A] bg-opacity-60 backdrop-blur-sm rounded-xl border border-gray-700 p-6 hover:border-[#B026FF]/50 transition-all duration-300">
              <div className="text-[#B026FF] text-2xl mb-3">✦</div>
              <h3 className="text-[#F5F7FA] font-medium mb-2">Smart Prioritization</h3>
              <p className="text-[#AAB0C0] text-sm">Focus on what matters most with priority indicators</p>
            </div>
            <div className="bg-[#11162A] bg-opacity-60 backdrop-blur-sm rounded-xl border border-gray-700 p-6 hover:border-[#39FF14]/50 transition-all duration-300">
              <div className="text-[#39FF14] text-2xl mb-3">📊</div>
              <h3 className="text-[#F5F7FA] font-medium mb-2">Progress Tracking</h3>
              <p className="text-[#AAB0C0] text-sm">Visualize your productivity and celebrate achievements</p>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4">
            <a
              href="/signup"
              className="px-8 py-4 bg-transparent border-2 border-[#00F5FF] text-[#00F5FF] rounded-lg font-semibold text-center hover:bg-[#00F5FF] hover:bg-opacity-10 transition-all duration-300 hover:shadow-lg hover:shadow-[#00F5FF]/30 focus:outline-none focus:ring-2 focus:ring-[#00F5FF] focus:ring-opacity-50 inline-block w-full sm:w-auto"
            >
              Get Started
            </a>
            <a
              href="/login"
              className="px-8 py-4 bg-transparent border-2 border-[#B026FF] text-[#B026FF] rounded-lg font-semibold text-center hover:bg-[#B026FF] hover:bg-opacity-10 transition-all duration-300 hover:shadow-lg hover:shadow-[#B026FF]/30 focus:outline-none focus:ring-2 focus:ring-[#B026FF] focus:ring-opacity-50 inline-block w-full sm:w-auto"
            >
              Sign In
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}