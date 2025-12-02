import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Heart, Phone, Mail, MapPin, Home, Bed, Bath, Square, Plus, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import Header from '@/components/Header';
import { housePlans } from '@/data/housePlans';
import { builtHomes } from '@/data/builtHomes';

export const HouseDetails = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [isFavorite, setIsFavorite] = useState(false);
  const [showFullDescription, setShowFullDescription] = useState(false);
  const [selectedFloor, setSelectedFloor] = useState(0);
  const [newRoomName, setNewRoomName] = useState('');
  const [showAddRoom, setShowAddRoom] = useState(false);
  const [expandedFloors, setExpandedFloors] = useState<Record<number, boolean>>({ 0: true });
  const [showBuyModal, setShowBuyModal] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [contactInfo, setContactInfo] = useState({ name: '', email: '', phone: '' });
  const [paymentInfo, setPaymentInfo] = useState({ 
    cardNumber: '', 
    expiryDate: '', 
    cvv: '' 
  });

  // Find the plan from either housePlans or builtHomes
  const plan = housePlans.find((p) => p.id === id) || builtHomes.find((p) => p.id === id);

  if (!plan) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center">
        <Header />
        <div className="text-center py-20">
          <h1 className="text-3xl font-bold mb-4">House Plan Not Found</h1>
          <p className="text-muted-foreground mb-6">The house plan you're looking for doesn't exist.</p>
          <Button onClick={() => navigate('/house-plans')}>Back to House Plans</Button>
        </div>
      </div>
    );
  }

  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % plan.images.length);
  };

  const prevImage = () => {
    setCurrentImageIndex((prev) => (prev - 1 + plan.images.length) % plan.images.length);
  };

  const toggleFloor = (floorNumber: number) => {
    setExpandedFloors(prev => ({
      ...prev,
      [floorNumber]: !prev[floorNumber]
    }));
  };

  const propertyFeatures = [
    { label: 'Bedrooms', value: plan.bedrooms, icon: Bed },
    { label: 'Bathrooms', value: plan.bathrooms, icon: Bath },
    { label: 'Garage', value: plan.garage, icon: Home },
    { label: 'Levels', value: plan.levels, icon: Home },
    { label: 'Floor Area', value: `${plan.floorArea} m²`, icon: Square },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <div className="container mx-auto px-4 py-8">
        {/* Back Button */}
        <Button 
          variant="ghost" 
          onClick={() => navigate(-1)}
          className="mb-6"
        >
          <ChevronLeft className="w-4 h-4 mr-2" />
          Back
        </Button>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Left Column - Image Gallery and Content */}
          <div className="lg:col-span-3">
            {/* Main Image */}
            <div className="relative mb-4 bg-gray-200 rounded-lg overflow-hidden aspect-video">
              <img
                src={plan.images[currentImageIndex]}
                alt={plan.title}
                className="w-full h-full object-cover"
              />

              {/* Image Navigation */}
              <button
                onClick={prevImage}
                className="absolute left-3 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition-all"
              >
                <ChevronLeft className="w-6 h-6" />
              </button>
              <button
                onClick={nextImage}
                className="absolute right-3 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition-all"
              >
                <ChevronRight className="w-6 h-6" />
              </button>

              {/* Image Counter */}
              <div className="absolute bottom-3 right-3 bg-black/50 text-white px-3 py-1 rounded-full text-sm">
                {currentImageIndex + 1} / {plan.images.length}
              </div>

              {/* Favorite Button */}
              <button
                onClick={() => setIsFavorite(!isFavorite)}
                className="absolute top-3 right-3 bg-white/90 hover:bg-white p-2 rounded-full transition-all"
              >
                <Heart
                  className={`w-6 h-6 ${isFavorite ? 'fill-red-500 text-red-500' : 'text-gray-600'}`}
                />
              </button>
            </div>

            {/* Thumbnail Gallery */}
            <div className="flex gap-2 overflow-x-auto pb-2">
              {plan.images.map((image, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentImageIndex(index)}
                  className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden transition-all ${
                    index === currentImageIndex ? 'ring-2 ring-primary' : 'opacity-70 hover:opacity-100'
                  }`}
                >
                  <img src={image} alt={`View ${index + 1}`} className="w-full h-full object-cover" />
                </button>
              ))}
            </div>

            {/* Description Section */}
            <div className="mt-8 space-y-4">
              <div>
                <h2 className="text-2xl font-bold mb-2">{plan.title}</h2>
                {plan.isNew && (
                  <Badge className="bg-accent text-accent-foreground mb-3">New Listing</Badge>
                )}
              </div>

              <p className="text-gray-600">
                {showFullDescription ? plan.description : `${plan.description?.substring(0, 150)}...`}
              </p>
              {plan.description && plan.description.length > 150 && (
                <Button
                  variant="link"
                  onClick={() => setShowFullDescription(!showFullDescription)}
                  className="p-0 h-auto"
                >
                  {showFullDescription ? '- Show less' : '+ Show more'}
                </Button>
              )}

              {/* Features List */}
              {plan.features && plan.features.length > 0 && (
                <div className="mt-6">
                  <h3 className="text-lg font-semibold mb-4">Key Features</h3>
                  <div className="grid grid-cols-2 gap-3 mb-6">
                    {plan.features.map((feature, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-primary" />
                        <span className="text-sm">{feature}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Property Features Grid with Room Breakdown */}
              <div className="mt-8 grid grid-cols-2 md:grid-cols-5 gap-4">
                {propertyFeatures.map((feature, index) => {
                  const Icon = feature.icon;
                  return (
                    <Card key={index} className="p-4 text-center">
                      <Icon className="w-6 h-6 mx-auto mb-2 text-primary" />
                      <p className="text-sm text-muted-foreground mb-1">{feature.label}</p>
                      <p className="text-lg font-bold">{feature.value}</p>
                    </Card>
                  );
                })}
              </div>

              {/* Room Breakdown - Floor Ground Floor Rooms */}
              {plan.levels && (
                <div className="mt-6 space-y-4">
                  {/* Ground Floor Rooms */}
                  <div>
                    <button
                      onClick={() => toggleFloor(0)}
                      className="w-full flex items-center justify-between p-4 bg-gradient-to-r from-slate-700 to-slate-800 border-3 border-slate-600 rounded-lg hover:from-slate-600 hover:to-slate-700 transition-all cursor-pointer group shadow-lg hover:shadow-slate-700/50 hover:shadow-2xl transform hover:scale-105"
                      style={{
                        boxShadow: '0 0 20px rgba(51, 65, 85, 0.5), 0 0 40px rgba(30, 41, 59, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.05)'
                      }}
                    >
                      <h3 className="text-lg font-black text-white drop-shadow-lg group-hover:text-blue-100 transition-colors animate-pulse">
                        ⚡ GROUND FLOOR ROOMS ⚡
                      </h3>
                      <ChevronRight
                        className={`w-7 h-7 text-white drop-shadow-lg transition-transform ${
                          expandedFloors[0] ? 'rotate-90' : ''
                        }`}
                      />
                    </button>
                    {expandedFloors[0] && (
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-3 p-4 bg-gradient-to-b from-slate-50 to-slate-100 rounded-lg border-2 border-slate-300">
                        {[
                          { name: 'Bedroom', quantity: 2 },
                          { name: 'Bathroom', quantity: 1 },
                          { name: 'Kitchen', quantity: 1 },
                          { name: 'Dining Room', quantity: 1 },
                          { name: 'Living Room', quantity: 1 },
                          { name: 'Pantry', quantity: 1 },
                          { name: 'Veranda', quantity: 1 },
                        ].map((room, index) => (
                          <div key={index} className="border-2 border-slate-400 rounded-lg p-3 text-center bg-white shadow-md hover:shadow-slate-400/50 transform hover:scale-110 transition-all cursor-default">
                            <p className="text-sm text-slate-700 font-bold mb-1">{room.name}</p>
                            <p className="text-2xl font-black text-slate-800">{room.quantity}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Floor 1 Rooms - Only if there are multiple levels */}
                  {plan.levels > 1 && (
                    <div>
                      <button
                        onClick={() => toggleFloor(1)}
                        className="w-full flex items-center justify-between p-4 bg-gradient-to-r from-indigo-700 to-indigo-800 border-3 border-indigo-600 rounded-lg hover:from-indigo-600 hover:to-indigo-700 transition-all cursor-pointer group shadow-lg hover:shadow-indigo-700/50 hover:shadow-2xl transform hover:scale-105"
                        style={{
                          boxShadow: '0 0 20px rgba(67, 56, 202, 0.5), 0 0 40px rgba(55, 48, 163, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.05)'
                        }}
                      >
                        <h3 className="text-lg font-black text-white drop-shadow-lg group-hover:text-indigo-100 transition-colors animate-pulse">
                          ⚡ 1st FLOOR ROOMS ⚡
                        </h3>
                        <ChevronRight
                          className={`w-7 h-7 text-white drop-shadow-lg transition-transform ${
                            expandedFloors[1] ? 'rotate-90' : ''
                          }`}
                        />
                      </button>
                      {expandedFloors[1] && (
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-3 p-4 bg-gradient-to-b from-indigo-50 to-indigo-100 rounded-lg border-2 border-indigo-300">
                          {[
                            { name: 'Bedroom', quantity: 2 },
                            { name: 'Bathroom', quantity: 1 },
                            { name: 'Master Suite', quantity: 1 },
                            { name: 'Study', quantity: 1 },
                            { name: 'Terrace', quantity: 1 },
                          ].map((room, index) => (
                            <div key={index} className="border-2 border-indigo-400 rounded-lg p-3 text-center bg-white shadow-md hover:shadow-indigo-400/50 transform hover:scale-110 transition-all cursor-default">
                              <p className="text-sm text-indigo-700 font-bold mb-1">{room.name}</p>
                              <p className="text-2xl font-black text-indigo-800">{room.quantity}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Floor 2 Rooms - Only if there are 3+ levels */}
                  {plan.levels > 2 && (
                    <div>
                      <button
                        onClick={() => toggleFloor(2)}
                        className="w-full flex items-center justify-between p-4 bg-gradient-to-r from-slate-800 to-slate-900 border-3 border-slate-700 rounded-lg hover:from-slate-700 hover:to-slate-800 transition-all cursor-pointer group shadow-lg hover:shadow-slate-800/50 hover:shadow-2xl transform hover:scale-105"
                        style={{
                          boxShadow: '0 0 20px rgba(30, 41, 59, 0.5), 0 0 40px rgba(15, 23, 42, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.05)'
                        }}
                      >
                        <h3 className="text-lg font-black text-white drop-shadow-lg group-hover:text-slate-100 transition-colors animate-pulse">
                          ⚡ 2nd FLOOR ROOMS ⚡
                        </h3>
                        <ChevronRight
                          className={`w-7 h-7 text-white drop-shadow-lg transition-transform ${
                            expandedFloors[2] ? 'rotate-90' : ''
                          }`}
                        />
                      </button>
                      {expandedFloors[2] && (
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-3 p-4 bg-gradient-to-b from-slate-100 to-slate-200 rounded-lg border-2 border-slate-400">
                          {[
                            { name: 'Bedroom', quantity: 1 },
                            { name: 'Bathroom', quantity: 1 },
                            { name: 'Balcony', quantity: 1 },
                          ].map((room, index) => (
                            <div key={index} className="border-2 border-slate-500 rounded-lg p-3 text-center bg-white shadow-md hover:shadow-slate-500/50 transform hover:scale-110 transition-all cursor-default">
                              <p className="text-sm text-slate-800 font-bold mb-1">{room.name}</p>
                              <p className="text-2xl font-black text-slate-900">{room.quantity}</p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Detailed Specifications */}
            <div className="mt-8 space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-4">Specifications</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  <div className="border rounded-lg p-4">
                    <p className="text-sm text-muted-foreground">Floor Area</p>
                    <p className="text-lg font-bold">{plan.floorArea} m²</p>
                  </div>
                  <div className="border rounded-lg p-4">
                    <p className="text-sm text-muted-foreground">Dimensions</p>
                    <p className="text-lg font-bold">{plan.width}m × {plan.depth}m</p>
                  </div>
                  <div className="border rounded-lg p-4">
                    <p className="text-sm text-muted-foreground">Levels</p>
                    <p className="text-lg font-bold">{plan.levels}</p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-4">Property Details</h3>
                <div className="space-y-3">
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-muted-foreground">Property Type</span>
                    <span className="font-medium">House</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-muted-foreground">Land Size</span>
                    <span className="font-medium">{plan.floorArea} m²</span>
                  </div>
                  <div className="flex justify-between border-b pb-2">
                    <span className="text-muted-foreground">Style</span>
                    <span className="font-medium">{plan.style.join(', ')}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Status</span>
                    <span className="font-medium">{plan.isPopular ? 'Featured' : 'Available'}</span>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-4">Property Amenities</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {(plan.amenities || []).map((amenity, index) => (
                    <div key={index} className="flex items-center gap-2 p-3 bg-blue-50 rounded-lg border border-blue-100">
                      <div className="w-2 h-2 rounded-full bg-primary flex-shrink-0" />
                      <span className="text-sm">{amenity}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Sidebar */}
          <div className="lg:col-span-1">
            {/* Price Card */}
            <Card className="p-6 mb-6">
              <p className="text-sm text-muted-foreground mb-1">Starting Price</p>
              <p className="text-4xl font-bold text-primary mb-6">
                R{plan.price.toLocaleString()}
              </p>

              <Button 
                className="w-full mb-6" 
                size="lg"
                onClick={() => setShowBuyModal(true)}
              >
                Buy Plan
              </Button>

              {/* Quick Stats */}
              <div className="space-y-3 border-t pt-4">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Bedrooms</span>
                  <span className="font-semibold">{plan.bedrooms}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Bathrooms</span>
                  <span className="font-semibold">{plan.bathrooms}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Garage</span>
                  <span className="font-semibold">{plan.garage}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Floor Area</span>
                  <span className="font-semibold">{plan.floorArea} m²</span>
                </div>
              </div>
            </Card>

            {/* Share Card */}
            <Card className="p-6">
              <h3 className="font-semibold mb-4">Share This Property</h3>
              <div className="space-y-2">
                <Button variant="outline" className="w-full justify-start">
                  <span className="mr-2">f</span>
                  Share on Facebook
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <span className="mr-2">𝕏</span>
                  Share on Twitter
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <span className="mr-2">in</span>
                  Share on LinkedIn
                </Button>
              </div>
            </Card>
          </div>
        </div>

        {/* Related Properties Section */}
        <div className="mt-16 border-t pt-12">
          <h2 className="text-2xl font-bold mb-6">Similar Properties</h2>
          <p className="text-muted-foreground">More properties will be displayed here based on similar criteria.</p>
        </div>
      </div>

      {/* Buy Plan Modal */}
      {showBuyModal && !showPaymentModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md bg-white">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">Purchase {plan.title}</h2>
                <button
                  onClick={() => setShowBuyModal(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <div className="space-y-4 mb-6">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Plan Price</p>
                  <p className="text-3xl font-bold text-primary">R{plan.price.toLocaleString()}</p>
                </div>

                <div className="border-t pt-4">
                  <p className="text-sm text-muted-foreground mb-2">Contact Information</p>
                  <input
                    type="text"
                    placeholder="Your Name"
                    value={contactInfo.name}
                    onChange={(e) => setContactInfo({ ...contactInfo, name: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg mb-3 text-sm"
                  />
                  <input
                    type="email"
                    placeholder="Your Email"
                    value={contactInfo.email}
                    onChange={(e) => setContactInfo({ ...contactInfo, email: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg mb-3 text-sm"
                  />
                  <input
                    type="tel"
                    placeholder="Your Phone"
                    value={contactInfo.phone}
                    onChange={(e) => setContactInfo({ ...contactInfo, phone: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm"
                  />
                </div>
              </div>

              <div className="space-y-3">
                <Button 
                  className="w-full" 
                  size="lg"
                  onClick={() => setShowPaymentModal(true)}
                >
                  Proceed to Payment
                </Button>
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => setShowBuyModal(false)}
                >
                  Cancel
                </Button>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Payment Details Modal */}
      {showPaymentModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md bg-white">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">Payment Details</h2>
                <button
                  onClick={() => {
                    setShowPaymentModal(false);
                    setShowBuyModal(false);
                  }}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <div className="space-y-4 mb-6">
                {/* Full Name */}
                <div>
                  <label className="text-sm font-semibold text-gray-700">Full Name</label>
                  <p className="text-lg font-bold text-gray-900">{contactInfo.name || 'John Doe'}</p>
                </div>

                {/* Email */}
                <div>
                  <label className="text-sm font-semibold text-gray-700">Email</label>
                  <p className="text-lg font-bold text-gray-900">{contactInfo.email || 'john@example.com'}</p>
                </div>

                <div className="border-t pt-4">
                  {/* Card Number */}
                  <div className="mb-4">
                    <label className="text-sm font-semibold text-gray-700 block mb-2">Card Number</label>
                    <input
                      type="text"
                      placeholder="1234 5678 9012 3456"
                      maxLength={19}
                      value={paymentInfo.cardNumber}
                      onChange={(e) => {
                        let value = e.target.value.replace(/\s/g, '');
                        value = value.replace(/(\d{4})/g, '$1 ').trim();
                        setPaymentInfo({ ...paymentInfo, cardNumber: value });
                      }}
                      className="w-full px-3 py-2 border rounded-lg text-sm"
                    />
                  </div>

                  {/* Expiry Date and CVV */}
                  <div className="grid grid-cols-2 gap-3 mb-4">
                    <div>
                      <label className="text-sm font-semibold text-gray-700 block mb-2">Expiry Date</label>
                      <input
                        type="text"
                        placeholder="MM/YY"
                        maxLength={5}
                        value={paymentInfo.expiryDate}
                        onChange={(e) => {
                          let value = e.target.value.replace(/\D/g, '');
                          if (value.length >= 2) {
                            value = value.slice(0, 2) + '/' + value.slice(2, 4);
                          }
                          setPaymentInfo({ ...paymentInfo, expiryDate: value });
                        }}
                        className="w-full px-3 py-2 border rounded-lg text-sm"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-semibold text-gray-700 block mb-2">CVV</label>
                      <input
                        type="text"
                        placeholder="123"
                        maxLength={3}
                        value={paymentInfo.cvv}
                        onChange={(e) => setPaymentInfo({ ...paymentInfo, cvv: e.target.value.replace(/\D/g, '') })}
                        className="w-full px-3 py-2 border rounded-lg text-sm"
                      />
                    </div>
                  </div>
                </div>

                {/* Price Summary */}
                <div className="border-t pt-4">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold">Total Amount:</span>
                    <span className="text-2xl font-bold text-primary">R{plan.price.toLocaleString()}</span>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <Button 
                  className="w-full" 
                  size="lg"
                  onClick={() => {
                    setShowPaymentModal(false);
                    setShowSuccessModal(true);
                  }}
                >
                  Complete Purchase
                </Button>
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => setShowPaymentModal(false)}
                >
                  Cancel
                </Button>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Success Modal */}
      {showSuccessModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md bg-white">
            <div className="p-6 text-center">
              {/* Checkmark Circle */}
              <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-12 h-12 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>

              <h2 className="text-2xl font-bold mb-2">Purchase Successful!</h2>
              <p className="text-gray-600 mb-2">Thank you for your purchase.</p>
              
              <div className="bg-gray-50 p-4 rounded-lg mb-6 text-left">
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Plan:</span>
                    <span className="font-semibold">{plan.title}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Amount:</span>
                    <span className="font-semibold">R{plan.price.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Email:</span>
                    <span className="font-semibold">{contactInfo.email}</span>
                  </div>
                </div>
              </div>

              <p className="text-sm text-gray-600 mb-6">
                A confirmation email has been sent to <strong>{contactInfo.email}</strong>
              </p>

              <Button 
                className="w-full" 
                size="lg"
                onClick={() => {
                  setShowSuccessModal(false);
                  setShowBuyModal(false);
                  setContactInfo({ name: '', email: '', phone: '' });
                  setPaymentInfo({ cardNumber: '', expiryDate: '', cvv: '' });
                }}
              >
                Continue Shopping
              </Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};

export default HouseDetails;
