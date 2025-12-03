import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { XCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { orderService } from "@/services/orderService";
import Header from "@/components/Header";

const PaymentCancel = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const orderId = searchParams.get("order_id");

    useEffect(() => {
        if (orderId) {
            orderService.verifyPaymentCancel(orderId).catch(console.error);
        }
    }, [orderId]);

    return (
        <div className="min-h-screen bg-background">
            <Header />
            <div className="container py-20 flex flex-col items-center justify-center text-center space-y-6">
                <XCircle className="h-24 w-24 text-red-500 animate-pulse" />
                <h1 className="text-4xl font-bold text-foreground">Payment Cancelled</h1>
                <p className="text-lg text-muted-foreground max-w-md">
                    Your payment was cancelled. No charges were made.
                    If you experienced any issues, please try again or contact support.
                </p>
                <div className="flex gap-4">
                    <Button onClick={() => navigate("/")} variant="outline" size="lg">
                        Return Home
                    </Button>
                    <Button onClick={() => navigate(-1)} size="lg">
                        Try Again
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default PaymentCancel;
