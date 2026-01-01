import { useState } from 'react';
import PropertyDetailsModal from './PropertyDetailsModal';

const PropertyCard = ({ property }) => {
  const [showModal, setShowModal] = useState(false);

  const {
    title,
    area,
    property_type,
    bedrooms,
    bathrooms,
    rent_price,
    furnishing_status,
    images = [],
  } = property;

  // Format price to Nigerian Naira
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-NG', {
      style: 'currency',
      currency: 'NGN',
      minimumFractionDigits: 0,
    }).format(price);
  };

  // Get first image or placeholder
  const mainImage = images.length > 0 ? images[0].image_url : '/placeholder-property.jpg';

  return (
    <>
    <div className="bg-marlin rounded-lg overflow-hidden border border-primary/20 hover:border-primary/50 transition-all duration-300 fade-in">
      {/* Property Image */}
      <div className="relative h-48 bg-port-gore overflow-hidden flex items-center justify-center">
        <img
          src={mainImage}
          alt={title}
          className="w-full h-full object-cover hover:scale-110 transition-transform duration-300"
          onError={(e) => {
            e.target.style.display = 'none';
          }}
        />
        <div className="absolute top-3 right-3 bg-port-gore/80 text-white px-3 py-1 rounded-full text-xs font-semibold">
          {property_type}
        </div>
      </div>

      {/* Property Details */}
      <div className="p-4">
        <h3 className="text-lg font-semibold text-white mb-2 line-clamp-1">{title}</h3>

        <div className="flex items-center text-primary text-sm mb-3">
          <svg
            className="w-4 h-4 mr-1"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
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
          {area}
        </div>

        {/* Property Features */}
        <div className="flex items-center space-x-4 mb-4 text-sm text-white">
          <div className="flex items-center">
            <svg
              className="w-4 h-4 mr-1 text-primary"
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
            {bedrooms} Beds
          </div>
          <div className="flex items-center">
            <svg
              className="w-4 h-4 mr-1 text-primary"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"
              />
            </svg>
            {bathrooms} Baths
          </div>
          {furnishing_status && (
            <div className="text-rajah text-xs font-semibold">{furnishing_status}</div>
          )}
        </div>

        {/* Price */}
        <div className="border-t border-primary/20 pt-3">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-primary">Annual Rent</p>
              <p className="text-xl font-bold text-rajah">{formatPrice(rent_price)}</p>
            </div>
            <button
              onClick={() => setShowModal(true)}
              className="bg-primary hover:bg-primary/80 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
            >
              View Details
            </button>
          </div>
        </div>
      </div>
    </div>

    {/* Property Details Modal */}
    {showModal && (
      <PropertyDetailsModal
        property={property}
        onClose={() => setShowModal(false)}
      />
    )}
    </>
  );
};

export default PropertyCard;
