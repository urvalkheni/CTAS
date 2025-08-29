import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Waves, Shield, Users, AlertTriangle, ArrowRight } from "lucide-react";
import { useEffect, useState } from "react";
import apiService from "@/services/api";

interface LandingInfo {
  projectName: string;
  tagline: string;
  description: string;
  features: string[];
}

const Home = () => {
  const [landingInfo, setLandingInfo] = useState<LandingInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLandingInfo = async () => {
      try {
        const data = await apiService.getLandingInfo();
        setLandingInfo(data);
      } catch (error) {
        console.error('Failed to fetch landing info:', error);
        // Fallback data
        setLandingInfo({
          projectName: 'Shore Guard Connect',
          tagline: 'Smart Coastal Protection & Mangrove Watch',
          description: 'Real-time coastal threat monitoring and community-driven mangrove conservation platform',
          features: [
            'Real-time coastal alerts',
            'Mangrove monitoring',
            'Community reporting',
            'Data analytics'
          ]
        });
      } finally {
        setLoading(false);
      }
    };

    fetchLandingInfo();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-wave flex items-center justify-center">
        <div className="text-center">
          <Waves className="h-12 w-12 text-primary mx-auto mb-4 animate-pulse" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-wave">
      {/* Header */}
      <header className="border-b bg-card/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Waves className="h-8 w-8 text-primary" />
            <h1 className="text-xl font-bold text-foreground">
              {landingInfo?.projectName || 'Shore Guard Connect'}
            </h1>
          </div>
          <div className="flex gap-2">
            <Button asChild variant="ghost">
              <Link to="/login">Login</Link>
            </Button>
            <Button asChild variant="ocean">
              <Link to="/register">Register</Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-5xl font-bold text-foreground mb-6">
              {landingInfo?.projectName || 'Shore Guard Connect'}
              <span className="block text-primary">
                {landingInfo?.tagline || 'Smart Coastal Protection & Mangrove Watch'}
              </span>
            </h2>
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              {landingInfo?.description || 'Real-time coastal threat monitoring and community-driven mangrove conservation platform. Join authorities, NGOs, and communities in safeguarding our coastlines.'}
            </p>
            
            {/* Hero Image/Illustration */}
            <div className="mb-8">
              <div className="w-64 h-64 mx-auto bg-gradient-ocean rounded-full flex items-center justify-center">
                <Waves className="h-32 w-32 text-white" />
              </div>
            </div>

            {/* Call-to-Action Buttons */}
            <div className="flex gap-4 justify-center flex-wrap">
              <Button asChild size="lg" variant="ocean" className="group">
                <Link to="/register">
                  Login / Register
                  <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Link>
              </Button>
              <Button asChild size="lg" variant="outline" className="group">
                <Link to="/about">
                  Learn More
                  <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h3 className="text-3xl font-bold text-center text-foreground mb-12">
            Platform Features
          </h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
            {landingInfo?.features.map((feature, index) => (
              <Card key={index} className="border-0 shadow-soft hover:shadow-medium transition-all duration-300">
                <CardContent className="p-6 text-center">
                  <div className="bg-gradient-ocean w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    {index === 0 && <AlertTriangle className="h-8 w-8 text-white" />}
                    {index === 1 && <Shield className="h-8 w-8 text-white" />}
                    {index === 2 && <Users className="h-8 w-8 text-white" />}
                    {index === 3 && <Waves className="h-8 w-8 text-white" />}
                  </div>
                  <h4 className="text-lg font-semibold mb-3">{feature}</h4>
                  <p className="text-muted-foreground text-sm">
                    {index === 0 && 'Get instant notifications about coastal threats and environmental hazards.'}
                    {index === 1 && 'Track mangrove health and conservation efforts in real-time.'}
                    {index === 2 && 'Enable communities to report incidents and share observations.'}
                    {index === 3 && 'Analyze trends and make data-driven decisions for coastal management.'}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 bg-gradient-ocean">
        <div className="container mx-auto px-4 text-center">
          <h3 className="text-3xl font-bold text-white mb-4">
            Ready to Make a Difference?
          </h3>
          <p className="text-white/90 text-lg mb-8 max-w-2xl mx-auto">
            Join our platform today and be part of the solution for coastal protection and mangrove conservation.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Button asChild size="lg" variant="secondary" className="group">
              <Link to="/register">
                Login / Register
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="bg-white/10 border-white/20 text-white hover:bg-white/20 group">
              <Link to="/about">
                Learn More
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-card py-8">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Waves className="h-6 w-6 text-primary" />
            <span className="font-semibold">
              {landingInfo?.projectName || 'Shore Guard Connect'}
            </span>
          </div>
          <p className="text-muted-foreground text-sm">
            Protecting coastlines through technology and community collaboration
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Home;