import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { orderService } from "@/services/orderService";
import Header from "@/components/Header";

const PaymentSuccess = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const orderId = searchParams.get("order_id");

    useEffect(() => {
        if (orderId) {
            orderService.verifyPaymentSuccess(orderId).catch(console.error);
        }
    }, [orderId]);

    return (
        <div className="min-h-screen bg-background">
            <Header />
            <div className="container py-20 flex flex-col items-center justify-center text-center space-y-6">
                <CheckCircle className="h-24 w-24 text-green-500 animate-bounce" />
                <h1 className="text-4xl font-bold text-foreground">Payment Successful!</h1>
                <p className="text-lg text-muted-foreground max-w-md">
                    Thank you for your purchase. We have received your order and will process it shortly.
                    You will receive an email with your house plans soon.
                </p>
                <div className="flex gap-4">
                    <Button onClick={() => navigate("/")} size="lg">
                        Return Home
                    </Button>
                    <Button onClick={() => navigate("/house-plans")} variant="outline" size="lg">
                        Browse More Plans
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default PaymentSuccess;
