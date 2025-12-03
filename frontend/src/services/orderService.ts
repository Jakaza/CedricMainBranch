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
    },

    async downloadReceipt(orderId: string): Promise<void> {
        const response = await api.get(`/orders/${orderId}/receipt/`, {
            responseType: 'blob'
        });

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `receipt_${orderId}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    }
};
