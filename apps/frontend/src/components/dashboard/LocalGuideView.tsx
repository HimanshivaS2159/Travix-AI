import React, { useState } from 'react';
import { MapPin, Star, Clock, DollarSign, Info, Eye, Utensils, Lightbulb, Gem } from 'lucide-react';

interface Attraction {
  id: string;
  name: string;
  category: string;
  description: string;
  location: string;
  rating: number;
  visit_duration: string;
  entry_fee: string;
  best_time: string;
  tips: string[];
}

interface Restaurant {
  id: string;
  name: string;
  cuisine: string;
  specialty: string;
  location: string;
  rating: number;
  price_range: string;
  must_try: string[];
}

interface LocalTip {
  category: string;
  tip: string;
  importance: string;
}

interface LocalGuideData {
  city: string;
  attractions?: Attraction[];
  restaurants?: Restaurant[];
  tips?: LocalTip[];
  hidden_gems?: string[];
  summary?: {
    attractions_count: number;
    restaurants_count: number;
    tips_count: number;
    hidden_gems_count: number;
  };
}

interface LocalGuideViewProps {
  data: LocalGuideData;
  message: string;
}

export function LocalGuideView({ data, message }: LocalGuideViewProps) {
  const [activeTab, setActiveTab] = useState<'attractions' | 'restaurants' | 'tips' | 'gems'>('attractions');

  // Determine which tab to show based on available data
  const hasAttractions = data.attractions && data.attractions.length > 0;
  const hasRestaurants = data.restaurants && data.restaurants.length > 0;
  const hasTips = data.tips && data.tips.length > 0;
  const hasGems = data.hidden_gems && data.hidden_gems.length > 0;

  return (
    <div className="p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          <MapPin className="inline-block w-6 h-6 mr-2 text-blue-600" />
          Local Guide: {data.city}
        </h2>
        <p className="text-gray-600">{message}</p>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-2 mb-6 border-b border-gray-200">
        {hasAttractions && (
          <button
            onClick={() => setActiveTab('attractions')}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === 'attractions'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Eye className="inline-block w-4 h-4 mr-2" />
            Attractions {data.summary && `(${data.summary.attractions_count})`}
          </button>
        )}
        {hasRestaurants && (
          <button
            onClick={() => setActiveTab('restaurants')}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === 'restaurants'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Utensils className="inline-block w-4 h-4 mr-2" />
            Restaurants {data.summary && `(${data.summary.restaurants_count})`}
          </button>
        )}
        {hasTips && (
          <button
            onClick={() => setActiveTab('tips')}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === 'tips'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Lightbulb className="inline-block w-4 h-4 mr-2" />
            Travel Tips {data.summary && `(${data.summary.tips_count})`}
          </button>
        )}
        {hasGems && (
          <button
            onClick={() => setActiveTab('gems')}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === 'gems'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Gem className="inline-block w-4 h-4 mr-2" />
            Hidden Gems {data.summary && `(${data.summary.hidden_gems_count})`}
          </button>
        )}
      </div>

      {/* Tab Content */}
      {activeTab === 'attractions' && hasAttractions && (
        <AttractionsTab attractions={data.attractions!} />
      )}
      {activeTab === 'restaurants' && hasRestaurants && (
        <RestaurantsTab restaurants={data.restaurants!} />
      )}
      {activeTab === 'tips' && hasTips && <TipsTab tips={data.tips!} />}
      {activeTab === 'gems' && hasGems && <GemsTab gems={data.hidden_gems!} />}
    </div>
  );
}

// Attractions Tab Component
function AttractionsTab({ attractions }: { attractions: Attraction[] }) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {attractions.map((attraction) => (
        <div key={attraction.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow">
          <div className="mb-3">
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-lg font-bold text-gray-900">{attraction.name}</h3>
              <div className="flex items-center gap-1 bg-yellow-100 px-2 py-1 rounded">
                <Star className="w-3 h-3 text-yellow-600 fill-yellow-600" />
                <span className="text-sm font-medium text-yellow-700">{attraction.rating}</span>
              </div>
            </div>
            <span className="inline-block bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded">
              {attraction.category}
            </span>
          </div>

          <p className="text-sm text-gray-600 mb-4">{attraction.description}</p>

          <div className="space-y-2 mb-4">
            <div className="flex items-start gap-2 text-sm">
              <MapPin className="w-4 h-4 text-gray-500 mt-0.5 flex-shrink-0" />
              <span className="text-gray-700">{attraction.location}</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <Clock className="w-4 h-4 text-gray-500 flex-shrink-0" />
              <span className="text-gray-700">{attraction.visit_duration}</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <DollarSign className="w-4 h-4 text-gray-500 flex-shrink-0" />
              <span className="text-gray-700">{attraction.entry_fee}</span>
            </div>
          </div>

          <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
            <div className="flex items-center gap-2 text-sm text-blue-800 mb-1">
              <Clock className="w-4 h-4" />
              <span className="font-medium">Best time to visit:</span>
            </div>
            <p className="text-sm text-blue-700">{attraction.best_time}</p>
          </div>

          {attraction.tips.length > 0 && (
            <div>
              <div className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                <Info className="w-4 h-4 text-green-600" />
                Insider Tips:
              </div>
              <ul className="space-y-1">
                {attraction.tips.map((tip, idx) => (
                  <li key={idx} className="text-sm text-gray-600 flex items-start gap-2">
                    <span className="text-green-600 mt-1">•</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

// Restaurants Tab Component
function RestaurantsTab({ restaurants }: { restaurants: Restaurant[] }) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {restaurants.map((restaurant) => (
        <div key={restaurant.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow">
          <div className="mb-3">
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-lg font-bold text-gray-900">{restaurant.name}</h3>
              <div className="flex items-center gap-1 bg-yellow-100 px-2 py-1 rounded">
                <Star className="w-3 h-3 text-yellow-600 fill-yellow-600" />
                <span className="text-sm font-medium text-yellow-700">{restaurant.rating}</span>
              </div>
            </div>
            <div className="flex gap-2">
              <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded">
                {restaurant.cuisine}
              </span>
              <span className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">
                {restaurant.price_range}
              </span>
            </div>
          </div>

          <p className="text-sm text-gray-600 mb-4">{restaurant.specialty}</p>

          <div className="flex items-start gap-2 text-sm mb-4">
            <MapPin className="w-4 h-4 text-gray-500 mt-0.5 flex-shrink-0" />
            <span className="text-gray-700">{restaurant.location}</span>
          </div>

          {restaurant.must_try.length > 0 && (
            <div className="p-3 bg-orange-50 rounded-lg border border-orange-100">
              <div className="flex items-center gap-2 text-sm font-medium text-orange-800 mb-2">
                <Utensils className="w-4 h-4" />
                Must Try Dishes:
              </div>
              <div className="flex flex-wrap gap-2">
                {restaurant.must_try.map((dish, idx) => (
                  <span
                    key={idx}
                    className="bg-orange-100 text-orange-700 text-xs px-2 py-1 rounded"
                  >
                    {dish}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

// Tips Tab Component
function TipsTab({ tips }: { tips: LocalTip[] }) {
  const getImportanceBadge = (importance: string) => {
    switch (importance) {
      case 'high':
        return <span className="bg-red-100 text-red-700 text-xs px-2 py-1 rounded">High Priority</span>;
      case 'medium':
        return <span className="bg-yellow-100 text-yellow-700 text-xs px-2 py-1 rounded">Medium</span>;
      default:
        return <span className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">Low</span>;
    }
  };

  const categorizedTips = tips.reduce((acc, tip) => {
    if (!acc[tip.category]) {
      acc[tip.category] = [];
    }
    acc[tip.category].push(tip);
    return acc;
  }, {} as Record<string, LocalTip[]>);

  return (
    <div className="space-y-6">
      {Object.entries(categorizedTips).map(([category, categoryTips]) => (
        <div key={category} className="bg-white rounded-lg shadow-sm border border-gray-200 p-5">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-yellow-600" />
            {category}
          </h3>
          <div className="space-y-3">
            {categoryTips.map((tip, idx) => (
              <div
                key={idx}
                className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex-1">
                  <p className="text-sm text-gray-700">{tip.tip}</p>
                </div>
                {getImportanceBadge(tip.importance)}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

// Hidden Gems Tab Component
function GemsTab({ gems }: { gems: string[] }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {gems.map((gem, idx) => (
        <div
          key={idx}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow cursor-pointer"
        >
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center flex-shrink-0">
              <Gem className="w-5 h-5 text-white" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">{gem}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
