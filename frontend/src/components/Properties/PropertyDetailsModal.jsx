import { useState } from 'react';

const PropertyDetailsModal = ({ property, onClose }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [showContactFallback, setShowContactFallback] = useState(false);
  const [toast, setToast] = useState({ show: false, message: '' });

  if (!property) return null;

  const {
    title,
    area,
    address,
    property_type,
    bedrooms,
    bathrooms,
    rent_price,
    description,
    images = [],
    landlord,
  } = property;

  // Format Nigerian phone number for WhatsApp
  const cleanPhoneNumber = (phone) => {
    if (!phone) return null;
    // Remove all non-digit characters
    let cleaned = phone.replace(/\D/g, '');
    // Convert 080... to 234...
    if (cleaned.startsWith('0')) {
      cleaned = '234' + cleaned.substring(1);
    }
    // Ensure it starts with 234
    if (!cleaned.startsWith('234')) {
      cleaned = '234' + cleaned;
    }
    return cleaned;
  };

  // Format price to Nigerian Naira
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-NG', {
      style: 'currency',
      currency: 'NGN',
      minimumFractionDigits: 0,
    }).format(price);
  };

  // Handle Contact Landlord
  const handleContactLandlord = () => {
    if (!landlord?.phone_number) {
      setShowContactFallback(true);
      return;
    }

    // Show contact modal directly (better UX for MVP with test data)
    setShowContactFallback(true);
  };

  // Handle Schedule Visit
  const handleScheduleVisit = () => {
    if (!landlord?.phone_number) {
      setShowContactFallback(true);
      return;
    }

    // Show contact modal directly (better UX for MVP with test data)
    setShowContactFallback(true);
  };

  // Copy to clipboard
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      setToast({ show: true, message: `Copied: ${text}` });
      setTimeout(() => {
        setToast({ show: false, message: '' });
      }, 2000);
    });
  };

  // Handle image navigation
  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % images.length);
  };

  const prevImage = () => {
    setCurrentImageIndex((prev) => (prev - 1 + images.length) % images.length);
  };

  const currentImage = images.length > 0
    ? images[currentImageIndex].image_url
    : 'https://via.placeholder.com/800x600?text=No+Image';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
      {/* Modal Container */}
      <div className="relative w-full max-w-4xl max-h-[90vh] bg-marlin rounded-2xl overflow-hidden shadow-2xl border border-primary/20 animate-slide-up">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-10 w-10 h-10 bg-port-gore/80 hover:bg-port-gore rounded-full flex items-center justify-center text-white transition-colors"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Scrollable Content */}
        <div className="overflow-y-auto max-h-[90vh] custom-scrollbar">
          {/* Image Gallery */}
          <div className="relative h-96 bg-port-gore">
            <img
              src={currentImage}
              alt={title}
              className="w-full h-full object-cover"
              onError={(e) => {
                e.target.src = 'https://via.placeholder.com/800x600?text=Property+Image';
              }}
            />

            {/* Image Navigation */}
            {images.length > 1 && (
              <>
                <button
                  onClick={prevImage}
                  className="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-port-gore/80 hover:bg-port-gore rounded-full flex items-center justify-center text-white transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                <button
                  onClick={nextImage}
                  className="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-port-gore/80 hover:bg-port-gore rounded-full flex items-center justify-center text-white transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>

                {/* Image Counter */}
                <div className="absolute bottom-4 right-4 bg-port-gore/80 text-white px-3 py-1 rounded-full text-sm">
                  {currentImageIndex + 1} / {images.length}
                </div>
              </>
            )}

            {/* Property Type Badge */}
            <div className="absolute top-4 left-4 bg-gradient-to-r from-rajah to-primary text-white px-4 py-2 rounded-full text-sm font-semibold shadow-lg">
              {property_type}
            </div>
          </div>

          {/* Property Details */}
          <div className="p-6">
            {/* Title and Price */}
            <div className="mb-6">
              <h2 className="text-3xl font-bold text-white mb-2">{title}</h2>
              <div className="flex items-center text-primary text-lg mb-3">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {area}
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-bold text-rajah">{formatPrice(rent_price)}</span>
                <span className="text-white/60">/ year</span>
              </div>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
                <div className="flex items-center text-primary mb-2">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                  </svg>
                  <span className="text-white font-semibold">Bedrooms</span>
                </div>
                <p className="text-2xl font-bold text-white">{bedrooms}</p>
              </div>

              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
                <div className="flex items-center text-primary mb-2">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" />
                  </svg>
                  <span className="text-white font-semibold">Bathrooms</span>
                </div>
                <p className="text-2xl font-bold text-white">{bathrooms}</p>
              </div>

              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
                <div className="flex items-center text-primary mb-2">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                  <span className="text-white font-semibold">Type</span>
                </div>
                <p className="text-lg font-bold text-white capitalize">{property_type}</p>
              </div>

              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
                <div className="flex items-center text-primary mb-2">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span className="text-white font-semibold">Status</span>
                </div>
                <p className="text-lg font-bold text-green-400">Available</p>
              </div>
            </div>

            {/* Description */}
            {description && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-white mb-3">Description</h3>
                <p className="text-white/80 leading-relaxed">{description}</p>
              </div>
            )}

            {/* Address */}
            {address && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-white mb-3">Address</h3>
                <p className="text-white/80">{address}</p>
              </div>
            )}

            {/* Thumbnail Gallery */}
            {images.length > 1 && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-white mb-3">Gallery</h3>
                <div className="grid grid-cols-4 md:grid-cols-6 gap-2">
                  {images.map((img, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentImageIndex(index)}
                      className={`relative h-20 rounded-lg overflow-hidden border-2 transition-all ${
                        index === currentImageIndex
                          ? 'border-rajah scale-105'
                          : 'border-white/20 hover:border-primary/50'
                      }`}
                    >
                      <img
                        src={img.image_url}
                        alt={`Property ${index + 1}`}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          e.target.src = 'https://via.placeholder.com/100?text=Img';
                        }}
                      />
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                onClick={handleContactLandlord}
                disabled={!landlord?.phone_number}
                className={`flex-1 py-3 rounded-lg font-semibold transition-all shadow-lg ${
                  landlord?.phone_number
                    ? 'bg-gradient-to-r from-rajah to-primary hover:from-rajah/90 hover:to-primary/90 text-white'
                    : 'bg-white/10 text-white/50 cursor-not-allowed'
                }`}
              >
                Contact Landlord
              </button>
              <button
                onClick={handleScheduleVisit}
                disabled={!landlord?.phone_number}
                className={`flex-1 py-3 rounded-lg font-semibold transition-all ${
                  landlord?.phone_number
                    ? 'bg-white/10 hover:bg-white/20 backdrop-blur-sm text-white border border-white/20'
                    : 'bg-white/5 text-white/50 cursor-not-allowed border border-white/10'
                }`}
              >
                Schedule Visit
              </button>
            </div>

            {/* Fallback Contact Info Modal */}
            {showContactFallback && landlord && (
              <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
                <div className="bg-marlin rounded-2xl p-6 max-w-md w-full border border-primary/20">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-bold text-white">Contact Information</h3>
                    <button
                      onClick={() => setShowContactFallback(false)}
                      className="text-white/60 hover:text-white"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <p className="text-primary text-sm mb-1">Landlord Name</p>
                      <p className="text-white font-semibold">{landlord.full_name}</p>
                    </div>

                    {landlord.phone_number && (
                      <div>
                        <p className="text-primary text-sm mb-1">Phone Number</p>
                        <div className="flex items-center gap-2 mb-2">
                          <a
                            href={`tel:${landlord.phone_number}`}
                            className="text-white font-semibold hover:text-rajah flex-1"
                          >
                            {landlord.phone_number}
                          </a>
                          <button
                            onClick={() => copyToClipboard(landlord.phone_number)}
                            className="bg-white/10 hover:bg-white/20 px-3 py-1 rounded text-sm text-white"
                          >
                            Copy
                          </button>
                        </div>
                        <div className="flex gap-2">
                          <a
                            href={`tel:${landlord.phone_number}`}
                            className="flex-1 bg-gradient-to-r from-rajah to-primary hover:from-rajah/90 hover:to-primary/90 text-white px-4 py-2 rounded-lg text-sm font-semibold text-center transition-all"
                          >
                            📞 Call
                          </a>
                          <a
                            href={`https://wa.me/${cleanPhoneNumber(landlord.phone_number)}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex-1 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-semibold text-center transition-all"
                          >
                            💬 WhatsApp
                          </a>
                        </div>
                      </div>
                    )}

                    {landlord.email && (
                      <div>
                        <p className="text-primary text-sm mb-1">Email</p>
                        <div className="flex items-center gap-2">
                          <a
                            href={`mailto:${landlord.email}`}
                            className="text-white font-semibold hover:text-rajah flex-1"
                          >
                            {landlord.email}
                          </a>
                          <button
                            onClick={() => copyToClipboard(landlord.email)}
                            className="bg-white/10 hover:bg-white/20 px-3 py-1 rounded text-sm text-white"
                          >
                            Copy
                          </button>
                        </div>
                      </div>
                    )}

                    <div className="pt-4">
                      <p className="text-white/60 text-sm">
                        You can call, email, or WhatsApp the landlord directly using the contact information above.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Toast Notification */}
      {toast.show && (
        <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-[60] animate-fade-in">
          <div className="bg-gradient-to-r from-rajah to-primary text-white px-6 py-3 rounded-full shadow-lg flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="font-semibold">{toast.message}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default PropertyDetailsModal;
