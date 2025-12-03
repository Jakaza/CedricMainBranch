import { useEffect, useState } from 'react';
import Header from '@/components/Header';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Home,
  Pencil,
  Edit3,
  Hammer,
  Eye,
  DollarSign,
  Users,
  MapPin,
  CheckCircle,
  FileCheck,
  ArrowRight,
  Zap,
  Home as HomeIcon
} from 'lucide-react';
import { Link } from 'react-router-dom';
import house1 from '@/assets/house1.jpg';
import house2 from '@/assets/house2.jpg';
import { settingsService, Service, PlanModification } from '@/services/settingsService';

const Services = () => {
  const [services, setServices] = useState<Service[]>([]);
  const [planModifications, setPlanModifications] = useState<PlanModification[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [servicesData, modificationsData] = await Promise.all([
          settingsService.getServices(),
          settingsService.getPlanModifications()
        ]);
        setServices(servicesData);
        setPlanModifications(modificationsData);
      } catch (error) {
        console.error('Error fetching services data:', error);
      }
    };
    fetchData();
  }, []);

  const getIcon = (iconName: string) => {
    const icons: { [key: string]: any } = {
      Home, Pencil, Edit3, Hammer, Eye, DollarSign, Users, MapPin, CheckCircle, FileCheck, Zap
    };
    return icons[iconName] || Home;
  };

  const processSteps = [
    {
      number: '01',
      title: 'Initial Consultation',
      description: 'We understand your vision, budget, and requirements through detailed discussion.',
    },
    {
      number: '02',
      title: 'Concept Design',
      description: 'Our architects create preliminary sketches and layout options for your review.',
    },
    {
      number: '03',
      title: 'Detailed Design',
      description: 'We develop detailed architectural drawings with all technical specifications.',
    },
    {
      number: '04',
      title: '3D Visualization',
      description: 'Photo-realistic 3D renders help you visualize the final result.',
    },
    {
      number: '05',
      title: 'Revisions & Approval',
      description: 'We incorporate your feedback and finalize all designs to your satisfaction.',
    },
    {
      number: '06',
      title: 'Project Delivery',
      description: 'Receive submission-ready plans with all documentation and certifications.',
    },
  ];

  const whyChooseUs = [
    {
      title: '20+ Years Experience',
      description: 'Decades of expertise in architectural design and house planning.',
    },
    {
      title: 'Award-Winning Architects',
      description: 'Our team has won multiple awards for design excellence.',
    },
    {
      title: 'Client-Focused Approach',
      description: 'We prioritize your vision and needs throughout the entire process.',
    },
    {
      title: 'Quality Guaranteed',
      description: 'Every design meets the highest standards of quality and compliance.',
    },
    {
      title: 'Timely Delivery',
      description: 'We respect your timeline and deliver on schedule, every time.',
    },
    {
      title: 'Competitive Pricing',
      description: 'Premium quality services at prices that fit your budget.',
    },
  ];

  return (
    <>
      <Header />
      <div className="min-h-screen bg-background">
        {/* Hero Section */}
        <div
          className="relative bg-cover bg-center py-32 text-white"
          style={{
            backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(${house1})`,
          }}
        >
          <div className="container mx-auto px-4">
            <h1 className="text-6xl font-bold mb-4">Our Architectural Services</h1>
            <p className="text-2xl text-white/90 max-w-2xl">
              High-quality house plans, custom designs, and professional building solutions tailored to your needs.
            </p>
          </div>
        </div>

        {/* Services Overview Grid */}
        <div className="py-20 bg-background">
          <div className="container mx-auto px-4">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-foreground mb-4">Our Complete Service Range</h2>
              <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
                From concept to completion, we offer comprehensive architectural services to bring your dream home to life.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {services.map((service, index) => {
                const Icon = getIcon(service.icon_name);
                return (
                  <Card key={service.id} className="p-8 hover:shadow-xl transition-all duration-300 hover:border-primary group">
                    <div className="flex items-start justify-between mb-4">
                      <div className="p-4 bg-primary/10 rounded-lg group-hover:bg-primary/20 transition-colors">
                        <Icon className="h-8 w-8 text-primary" />
                      </div>
                      {service.badge && (
                        <Badge className="bg-primary/20 text-primary hover:bg-primary/30">
                          {service.badge}
                        </Badge>
                      )}
                    </div>

                    <h3 className="text-xl font-bold text-foreground mb-3">{service.title}</h3>
                    <p className="text-muted-foreground mb-6 leading-relaxed">{service.description}</p>

                  </Card>
                );
              })}
            </div>
          </div>
        </div>

        {/* Custom Design Process Section */}
        <div className="py-20 bg-muted/30">
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-bold text-foreground mb-4 text-center">Our Design Process</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto text-center mb-16">
              A structured, collaborative approach to create your perfect home.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {processSteps.map((step, index) => (
                <div key={index} className="relative">
                  <Card className="p-8 h-full">
                    <div className="mb-4">
                      <span className="text-5xl font-bold text-primary/20">{step.number}</span>
                    </div>
                    <h3 className="text-xl font-bold text-foreground mb-3">{step.title}</h3>
                    <p className="text-muted-foreground">{step.description}</p>
                  </Card>
                  {index < processSteps.length - 1 && (
                    <div className="hidden lg:block absolute top-8 -right-4 w-8 h-1 bg-primary/30"></div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Service Details Section */}
        <div className="py-20 bg-background">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-20">
              <div>
                <h2 className="text-4xl font-bold text-foreground mb-6">Professional Plan Modifications</h2>
                <ul className="space-y-4">
                  {planModifications.map((mod) => (
                    <li key={mod.id} className="flex gap-3">
                      <CheckCircle className="h-6 w-6 text-primary flex-shrink-0 mt-1" />
                      <div>
                        <h4 className="font-semibold text-foreground">{mod.title}</h4>
                        <p className="text-muted-foreground">{mod.description}</p>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
              <img src={house2} alt="Plan Modifications" className="rounded-lg shadow-lg" />
            </div>

            {/* Why Choose Us */}
            <div className="mt-20">
              <h2 className="text-4xl font-bold text-foreground mb-12 text-center">Why Choose Our Architect Team</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {whyChooseUs.map((reason, index) => (
                  <Card key={index} className="p-8 text-center hover:shadow-lg transition-shadow">
                    <Zap className="h-8 w-8 text-primary mx-auto mb-4" />
                    <h3 className="text-lg font-bold text-foreground mb-2">{reason.title}</h3>
                    <p className="text-muted-foreground">{reason.description}</p>
                  </Card>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Call-To-Action Section */}
        <div
          className="relative bg-cover bg-center py-32 text-white"
          style={{
            backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url(${house1})`,
          }}
        >
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-5xl font-bold mb-4">Ready to Start Your Project?</h2>
            <p className="text-2xl text-white/90 mb-8 max-w-2xl mx-auto">
              Let our expert architects help you design and plan your dream home today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/contact">
                <Button size="lg" className="bg-white text-primary hover:bg-white/90">
                  Request a Custom Design
                </Button>
              </Link>
              <Link to="/house-plans">
                <Button size="lg" variant="outline" className="border-white text-white hover:bg-white/10">
                  Browse House Plans
                </Button>
              </Link>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="bg-primary text-primary-foreground py-16">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-8">
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <HomeIcon className="h-6 w-6 text-primary-foreground" />
                  <span className="text-lg font-bold text-primary-foreground">Cedric House Planning</span>
                </div>
                <p className="text-sm">
                  Creating beautiful, functional house plans for your dream home.
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-primary-foreground mb-4">House Plans</h3>
                <ul className="space-y-2 text-sm">
                  <li><a href="#" className="hover:opacity-80 transition-opacity">Modern Plans</a></li>
                  <li><a href="#" className="hover:opacity-80 transition-opacity">Traditional Plans</a></li>
                  <li><a href="#" className="hover:opacity-80 transition-opacity">Small House Plans</a></li>
                  <li><a href="#" className="hover:opacity-80 transition-opacity">Luxury Plans</a></li>
                </ul>
              </div>

              <div>
                <h3 className="font-semibold text-primary-foreground mb-4">Services</h3>
                <ul className="space-y-2 text-sm">
                  <li><a href="#" className="hover:opacity-80 transition-opacity">Custom Design</a></li>
                  <li><a href="#" className="hover:opacity-80 transition-opacity">Plan Modifications</a></li>
                  <li><a href="#" className="hover:opacity-80 transition-opacity">Construction Support</a></li>
                  <li><a href="#" className="hover:opacity-80 transition-opacity">Cost Estimates</a></li>
                </ul>
              </div>

              <div>
                <h3 className="font-semibold text-primary-foreground mb-4">Support</h3>
                <ul className="space-y-2 text-sm">
                  <li><a href="#" className="hover:opacity-80 transition-opacity">Contact Us</a></li>
                  <li><a href="#" className="hover:opacity-80 transition-opacity">FAQ</a></li>
                  <li><a href="#" className="hover:opacity-80 transition-opacity">Shipping Info</a></li>
                  <li><a href="#" className="hover:opacity-80 transition-opacity">Returns</a></li>
                </ul>
              </div>
            </div>

            <div className="pt-8 border-t border-primary-foreground/20 text-center text-sm">
              <p className="mb-2">© 2024 Cedric House Planning and Construction. All rights reserved.</p>
              <p className="text-xs">Website Developers: <a href="#" className="text-red-400 hover:text-red-300 transition-opacity">TAD Developers</a></p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
};

export default Services;
