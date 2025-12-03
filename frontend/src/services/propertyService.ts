import { api, API_ENDPOINTS } from './api';
import { HousePlan } from '@/types/housePlan';

// Backend response type
interface PropertyResponse {
    id: number;
    title: string;
    category: 'PLAN' | 'BUILT';
    price: number;
    bedrooms: number;
    bathrooms: number;
    garage: number;
    floor_area: number;
    levels: number;
    width: number;
    depth: number;
    styles: string[];
    features: string[];
    amenities: string[];
    floors: any[];
    is_new: boolean;
    is_popular: boolean;
    description: string;
    video_url: string;
    en_suite: number;
    lounges: number;
    dining_areas: number;
    garage_parking: number;
    covered_parking: number;
    pet_friendly: boolean;
    image_urls: string[];
}

// Transform backend response to frontend format
const transformProperty = (property: PropertyResponse): HousePlan => ({
    id: property.id.toString(),
    title: property.title,
    price: property.price,
    bedrooms: property.bedrooms,
    bathrooms: property.bathrooms,
    garage: property.garage,
    floorArea: property.floor_area,
    levels: property.levels,
    width: property.width,
    depth: property.depth,
    style: property.styles,
    isNew: property.is_new,
    isPopular: property.is_popular,
    images: property.image_urls,
    description: property.description,
    features: property.features,
    videoUrl: property.video_url,
    enSuite: property.en_suite,
    lounges: property.lounges,
    diningAreas: property.dining_areas,
    garageParking: property.garage_parking,
    coveredParking: property.covered_parking,
    petFriendly: property.pet_friendly,
    amenities: property.amenities,
    floors: property.floors,
});

export const propertyService = {
    // Get all properties
    async getAll(): Promise<HousePlan[]> {
        const response = await api.get<PropertyResponse[]>(API_ENDPOINTS.properties.list);
        return response.data.map(transformProperty);
    },

    // Get single property by ID
    async getById(id: string): Promise<HousePlan> {
        const response = await api.get<PropertyResponse>(API_ENDPOINTS.properties.detail(id));
        return transformProperty(response.data);
    },

    // Get house plans only
    async getPlans(): Promise<HousePlan[]> {
        const response = await api.get<PropertyResponse[]>(API_ENDPOINTS.properties.plans);
        return response.data.map(transformProperty);
    },

    // Get built homes only
    async getBuilt(): Promise<HousePlan[]> {
        const response = await api.get<PropertyResponse[]>(API_ENDPOINTS.properties.built);
        return response.data.map(transformProperty);
    },

    // Search properties
    async searchProperties(query: string): Promise<HousePlan[]> {
        const response = await api.get<PropertyResponse[]>(`${API_ENDPOINTS.properties.list}?search=${encodeURIComponent(query)}`);
        return response.data.map(transformProperty);
    },
};
