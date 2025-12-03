import { api } from './api';

export interface SiteSettings {
    company_name: string;
    tagline: string;
    hero_title: string;
    hero_description: string;
    about_title: string;
    about_description: string;
    who_we_are_content: string;
    mission_statement: string;
    years_experience: string;
    projects_completed: string;
    client_satisfaction: string;
}

export interface ContactInformation {
    phone_number: string;
    email: string;
    support_email: string;
    address: string;
    monday_friday: string;
    saturday: string;
    sunday: string;
    facebook_url: string;
    twitter_url: string;
    instagram_url: string;
}

export interface TeamMember {
    id: number;
    name: string;
    role: string;
    experience: string;
    specialty: string;
    image: string;
    order: number;
}

export interface Testimonial {
    id: number;
    name: string;
    role: string;
    content: string;
    rating: number;
    initials: string;
    created_at: string;
}

export const settingsService = {
    async getSettings(): Promise<SiteSettings> {
        const response = await api.get<SiteSettings>('/settings/settings/');
        return response.data;
    },

    async getContactInfo(): Promise<ContactInformation> {
        const response = await api.get<ContactInformation>('/settings/contact-info/');
        return response.data;
    },

    async getTeamMembers(): Promise<TeamMember[]> {
        const response = await api.get<TeamMember[]>('/settings/team/');
        return response.data;
    },

    async getTestimonials(): Promise<Testimonial[]> {
        const response = await api.get<Testimonial[]>('/settings/testimonials/');
        return response.data;
    }
};
