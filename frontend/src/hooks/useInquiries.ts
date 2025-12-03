import { useMutation } from '@tanstack/react-query';
import { inquiryService, ContactMessageData, QuoteRequestData } from '@/services/inquiryService';

// Submit contact message
export const useSubmitContact = () => {
    return useMutation({
        mutationFn: (data: ContactMessageData) => inquiryService.submitContact(data),
    });
};

// Submit quote request
export const useSubmitQuote = () => {
    return useMutation({
        mutationFn: (data: QuoteRequestData) => inquiryService.submitQuote(data),
    });
};
