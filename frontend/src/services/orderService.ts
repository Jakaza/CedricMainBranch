import { api } from './api';

export interface CheckoutResponse {
    redirectUrl: string;
    order_id: number;
}

export const orderService = {
    async createCheckoutSession(planId: string, customerEmail?: string): Promise<CheckoutResponse> {
        const response = await api.post<CheckoutResponse>('/orders/checkout/', {
            plan_id: planId,
            customer_email: customerEmail
        });
        return response.data;
    },

    async verifyPaymentSuccess(orderId: string): Promise<void> {
        await api.post('/orders/success/', { order_id: orderId });
    },

    async verifyPaymentCancel(orderId: string): Promise<void> {
        await api.post('/orders/cancel/', { order_id: orderId });
    }
};
