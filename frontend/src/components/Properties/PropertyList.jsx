import PropertyCard from './PropertyCard';

const PropertyList = ({ properties, isLoading }) => {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="bg-marlin rounded-lg border border-primary/20 overflow-hidden animate-pulse"
          >
            <div className="h-48 bg-port-gore"></div>
            <div className="p-4 space-y-3">
              <div className="h-4 bg-port-gore rounded w-3/4"></div>
              <div className="h-3 bg-port-gore rounded w-1/2"></div>
              <div className="flex space-x-4">
                <div className="h-3 bg-port-gore rounded w-16"></div>
                <div className="h-3 bg-port-gore rounded w-16"></div>
              </div>
              <div className="h-8 bg-port-gore rounded"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (!properties || properties.length === 0) {
    return (
      <div className="bg-marlin rounded-lg border border-primary/20 p-12 text-center">
        <svg
          className="w-16 h-16 mx-auto text-primary mb-4"
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
        <h3 className="text-xl font-semibold text-white mb-2">No Properties Found</h3>
        <p className="text-primary">
          Try asking the AI assistant about properties in different areas or with different
          requirements.
        </p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-white">
          Available Properties{' '}
          <span className="text-primary text-base">({properties.length})</span>
        </h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {properties.map((property) => (
          <PropertyCard key={property.id} property={property} />
        ))}
      </div>
    </div>
  );
};

export default PropertyList;
