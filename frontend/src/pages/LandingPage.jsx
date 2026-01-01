import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import ImageCarousel from '../components/common/ImageCarousel';

const LandingPage = () => {
  const navigate = useNavigate();

  // Modern Header with glassmorphism
  const LandingHeader = () => (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/5 backdrop-blur-md border-b border-white/10">
      <div className="container mx-auto px-6 py-5 flex items-center justify-between">
        <div className="flex items-center space-x-3 group cursor-pointer">
          <div className="w-12 h-12 bg-gradient-to-br from-rajah to-primary rounded-xl flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-transform duration-300">
            <svg
              className="w-7 h-7 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
              />
            </svg>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Housing Intelligence</h1>
            <p className="text-sm text-primary/80">Find Your Perfect Home</p>
          </div>
        </div>
        <button
          onClick={() => navigate('/chat')}
          className="relative px-8 py-3 bg-gradient-to-r from-rajah to-rajah/80 text-white rounded-full font-semibold shadow-lg hover:shadow-rajah/50 transform hover:scale-105 transition-all duration-300 overflow-hidden group"
        >
          <span className="relative z-10 flex items-center space-x-2">
            <span>Get Started</span>
            <svg className="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </span>
          <div className="absolute inset-0 bg-gradient-to-r from-rajah/50 to-transparent transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></div>
        </button>
      </div>
    </header>
  );
  const featuresRef = useRef([]);

  // Hero images for carousel
  const heroImages = [
    {
      url: 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1200&h=600&fit=crop',
      alt: 'Modern Lagos apartment',
    },
    {
      url: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1200&h=600&fit=crop',
      alt: 'Luxury property in Lagos',
    },
    {
      url: 'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=1200&h=600&fit=crop',
      alt: 'Beautiful home interior',
    },
    {
      url: 'https://images.unsplash.com/photo-1600607687644-aac4c3eac7f4?w=1200&h=600&fit=crop',
      alt: 'Lagos residential area',
    },
  ];

  // Features data
  const features = [
    {
      icon: (
        <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
          />
        </svg>
      ),
      title: 'AI-Powered Chat',
      description: 'Ask natural questions about properties and areas. Our intelligent assistant understands what you need.',
    },
    {
      icon: (
        <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
      ),
      title: 'Real Tenant Reviews',
      description: 'Get honest insights from people who actually lived there. Know about power, water, security, and more.',
    },
    {
      icon: (
        <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
          />
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
      ),
      title: 'Lagos-Focused',
      description: 'Specialized knowledge of Lagos areas - from Lekki to Ikeja, Victoria Island to Yaba. We know Lagos.',
    },
    {
      icon: (
        <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      ),
      title: 'Transparent Pricing',
      description: 'See actual rent prices in Naira. No hidden fees, no surprises. Know what you can afford.',
    },
  ];

  // Intersection Observer for scroll animations
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, index) => {
          if (entry.isIntersecting) {
            setTimeout(() => {
              entry.target.classList.add('slide-up');
              entry.target.style.opacity = '1';
            }, index * 100);
          }
        });
      },
      { threshold: 0.1 }
    );

    featuresRef.current.forEach((ref) => {
      if (ref) observer.observe(ref);
    });

    return () => {
      featuresRef.current.forEach((ref) => {
        if (ref) observer.unobserve(ref);
      });
    };
  }, []);

  return (
    <div className="min-h-screen bg-port-gore">
      {/* Header */}
      <LandingHeader />

      {/* Hero Section */}
      <section className="relative h-screen overflow-hidden">
        <ImageCarousel images={heroImages} interval={5000} />

        {/* Gradient Overlays */}
        <div className="absolute inset-0 bg-gradient-to-b from-port-gore/60 via-transparent to-port-gore/90 z-[5]"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-port-gore/40 to-transparent z-[5]"></div>

        {/* Floating Elements */}
        <div className="absolute top-1/4 left-10 w-20 h-20 bg-rajah/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/3 right-20 w-32 h-32 bg-primary/20 rounded-full blur-3xl animate-pulse delay-700"></div>

        {/* Hero Content */}
        <div className="absolute inset-0 flex items-center justify-center z-10">
          <div className="text-center px-6 max-w-5xl">
            <div className="inline-block mb-4 px-5 py-2 bg-white/10 backdrop-blur-sm rounded-full border border-white/20">
              <span className="text-rajah font-semibold text-sm">AI-Powered Property Search</span>
            </div>

            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight fade-in">
              Find Your Perfect
              <br />
              <span className="bg-gradient-to-r from-rajah via-primary to-rajah bg-clip-text text-transparent animate-gradient">
                Lagos Home
              </span>
            </h1>

            <p className="text-lg md:text-xl text-white/80 mb-8 leading-relaxed max-w-3xl mx-auto">
              Experience the future of property search. Chat with our intelligent AI assistant to discover homes, explore neighborhoods, and read authentic tenant reviews.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
              <button
                onClick={() => navigate('/chat')}
                className="group relative px-8 py-4 bg-gradient-to-r from-rajah to-primary text-white rounded-2xl text-lg font-bold shadow-2xl hover:shadow-rajah/50 transform hover:scale-105 transition-all duration-300 overflow-hidden"
              >
                <span className="relative z-10 flex items-center space-x-2">
                  <span>Start Your Search</span>
                  <svg className="w-5 h-5 transform group-hover:translate-x-2 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </span>
                <div className="absolute inset-0 bg-white/20 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></div>
              </button>

              <button
                onClick={() => document.getElementById('features').scrollIntoView({ behavior: 'smooth' })}
                className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white rounded-2xl text-lg font-bold border-2 border-white/20 hover:bg-white/20 hover:border-white/40 transition-all duration-300"
              >
                Learn More
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6 max-w-2xl mx-auto">
              <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:bg-white/10 transition-all duration-300">
                <div className="text-3xl font-bold text-rajah mb-1">80+</div>
                <div className="text-sm text-white/70">Properties</div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:bg-white/10 transition-all duration-300">
                <div className="text-3xl font-bold text-primary mb-1">250+</div>
                <div className="text-sm text-white/70">Reviews</div>
              </div>
              <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:bg-white/10 transition-all duration-300">
                <div className="text-3xl font-bold text-white mb-1">24/7</div>
                <div className="text-sm text-white/70">AI Support</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-32 px-6 bg-gradient-to-b from-marlin to-port-gore relative overflow-hidden">
        {/* Background Elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-rajah/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-primary/10 rounded-full blur-3xl"></div>

        <div className="container mx-auto max-w-7xl relative z-10">
          <div className="text-center mb-20">
            <div className="inline-block mb-4 px-6 py-2 bg-rajah/20 backdrop-blur-sm rounded-full border border-rajah/30">
              <span className="text-rajah font-semibold text-sm">Why Choose Us</span>
            </div>
            <h2 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
              Everything You Need to
              <br />
              <span className="bg-gradient-to-r from-rajah to-primary bg-clip-text text-transparent">
                Find Your Dream Home
              </span>
            </h2>
            <p className="text-xl text-white/70 max-w-3xl mx-auto">
              We combine cutting-edge AI technology with real tenant experiences to give you the most comprehensive property search platform in Lagos
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                ref={(el) => (featuresRef.current[index] = el)}
                className="group relative bg-gradient-to-br from-white/5 to-white/[0.02] backdrop-blur-sm rounded-3xl p-8 opacity-0 transition-all duration-500 border border-white/10 hover:border-rajah/50 hover:shadow-2xl hover:shadow-rajah/20 overflow-hidden"
              >
                {/* Hover gradient */}
                <div className="absolute inset-0 bg-gradient-to-br from-rajah/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

                <div className="relative z-10">
                  <div className="mb-6 inline-block p-4 bg-gradient-to-br from-rajah/20 to-primary/20 rounded-2xl text-rajah group-hover:scale-110 transition-transform duration-300">
                    {feature.icon}
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-4 group-hover:text-rajah transition-colors">
                    {feature.title}
                  </h3>
                  <p className="text-white/70 leading-relaxed">
                    {feature.description}
                  </p>
                </div>

                {/* Corner accent */}
                <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-rajah/20 to-transparent rounded-bl-3xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 px-6 bg-port-gore relative overflow-hidden">
        {/* Background gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-rajah/20 via-transparent to-primary/20"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full h-full max-w-4xl">
          <div className="w-full h-full bg-gradient-to-r from-rajah/10 to-primary/10 rounded-full blur-3xl"></div>
        </div>

        <div className="container mx-auto max-w-5xl text-center relative z-10">
          <div className="bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-3xl p-12 md:p-16 border border-white/20 shadow-2xl">
            <h2 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
              Ready to Find Your
              <br />
              <span className="bg-gradient-to-r from-rajah to-primary bg-clip-text text-transparent">
                Dream Home?
              </span>
            </h2>
            <p className="text-xl md:text-2xl text-white/80 mb-10 max-w-2xl mx-auto">
              Join hundreds of happy tenants who found their perfect home using our AI-powered platform. Start your journey today.
            </p>
            <button
              onClick={() => navigate('/chat')}
              className="group relative px-12 py-6 bg-gradient-to-r from-rajah to-primary text-white rounded-2xl text-xl font-bold shadow-2xl hover:shadow-rajah/50 transform hover:scale-105 transition-all duration-300 overflow-hidden"
            >
              <span className="relative z-10 flex items-center justify-center space-x-3">
                <span>Start Your Search Now</span>
                <svg className="w-6 h-6 transform group-hover:translate-x-2 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </span>
              <div className="absolute inset-0 bg-white/20 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></div>
            </button>
            <p className="mt-6 text-white/60 text-sm">No credit card required • Free forever</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-marlin/50 backdrop-blur-sm py-12 px-6 border-t border-white/10">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col items-center text-center space-y-6">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-rajah to-primary rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
              </div>
              <span className="text-xl font-bold text-white">Housing Intelligence</span>
            </div>

            {/* Description */}
            <p className="text-white/70 max-w-md">
              Making Lagos housing transparent and accessible through AI-powered search and authentic tenant reviews.
            </p>

            {/* Copyright */}
            <div className="pt-6 border-t border-white/10 w-full">
              <p className="text-white/60 text-sm">
                © 2025 Housing Intelligence Platform. All rights reserved.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
