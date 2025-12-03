import { api, API_ENDPOINTS } from './api';

export interface ContactMessageData {
    name: string;
    email: string;
    phone?: string;
    subject: string;
    message: string;
}

export interface QuoteRequestData {
    full_name: string;
    email: string;
    phone: string;
    city: string;
    preferred_style: string;
    custom_style?: string;
    bedrooms: number;
    bathrooms: number;
    other_rooms?: string;
    yard_length: number;
    yard_breadth: number;
    budget: string;
    description: string;
}

export const inquiryService = {
    // Submit contact message
    async submitContact(data: ContactMessageData): Promise<void> {
        await api.post(API_ENDPOINTS.inquiries.contact, data);
    },

    // Submit quote request
    async submitQuote(data: QuoteRequestData): Promise<void> {
        await api.post(API_ENDPOINTS.inquiries.quotes, data);
    },
};
