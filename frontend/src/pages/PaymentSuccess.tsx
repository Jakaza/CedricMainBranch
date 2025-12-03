import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { CheckCircle, Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { orderService } from "@/services/orderService";
import Header from "@/components/Header";
import { useToast } from "@/components/ui/use-toast";

const PaymentSuccess = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const { toast } = useToast();
    const orderId = searchParams.get("order_id");
    const [downloading, setDownloading] = useState(false);

    useEffect(() => {
        if (orderId) {
            orderService.verifyPaymentSuccess(orderId).catch(console.error);
        }
    }, [orderId]);

    const handleDownloadReceipt = async () => {
        if (!orderId) return;

        setDownloading(true);
        try {
            await orderService.downloadReceipt(orderId);
            toast({
                title: "Receipt Downloaded",
                description: "Your payment receipt has been downloaded successfully.",
            });
        } catch (error) {
            console.error("Download error:", error);
            toast({
                title: "Download Failed",
                description: "Could not download receipt. Please try again.",
                variant: "destructive"
            });
        } finally {
            setDownloading(false);
        }
    };

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
                <div className="flex flex-col sm:flex-row gap-4">
                    <Button
                        onClick={handleDownloadReceipt}
                        size="lg"
                        disabled={!orderId || downloading}
                        className="gap-2"
                    >
                        <Download className="h-4 w-4" />
                        {downloading ? "Downloading..." : "Download Receipt"}
                    </Button>
                    <Button onClick={() => navigate("/")} variant="outline" size="lg">
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
