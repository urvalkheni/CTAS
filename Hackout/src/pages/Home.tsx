import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Waves, Shield, Users, AlertTriangle } from "lucide-react";

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-wave">
      {/* Header */}
      <header className="border-b bg-card/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Waves className="h-8 w-8 text-primary" />
            <h1 className="text-xl font-bold text-foreground">Coastal Protection Platform</h1>
          </div>
          <div className="flex gap-2">
            <Button asChild variant="ghost">
              <Link to="/login">Login</Link>
            </Button>
            <Button asChild variant="ocean">
              <Link to="/register">Get Started</Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-5xl font-bold text-foreground mb-6">
              Protecting Our Coasts
              <span className="block text-primary">Together</span>
            </h2>
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Real-time coastal threat monitoring and community-driven mangrove conservation 
              platform. Join authorities, NGOs, and communities in safeguarding our coastlines.
            </p>
            <div className="flex gap-4 justify-center flex-wrap">
              <Button asChild size="lg" variant="ocean">
                <Link to="/register">Join Platform</Link>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link to="/about">Learn More</Link>
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
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <Card className="border-0 shadow-soft hover:shadow-medium transition-all duration-300">
              <CardContent className="p-6 text-center">
                <div className="bg-gradient-ocean w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <AlertTriangle className="h-8 w-8 text-white" />
                </div>
                <h4 className="text-xl font-semibold mb-3">Real-time Alerts</h4>
                <p className="text-muted-foreground">
                  Get instant notifications about coastal threats, sea level changes, 
                  and environmental hazards in your area.
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-soft hover:shadow-medium transition-all duration-300">
              <CardContent className="p-6 text-center">
                <div className="bg-gradient-ocean w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users className="h-8 w-8 text-white" />
                </div>
                <h4 className="text-xl font-semibold mb-3">Community Reports</h4>
                <p className="text-muted-foreground">
                  Enable local communities to report incidents, share observations, 
                  and contribute to coastal protection efforts.
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-soft hover:shadow-medium transition-all duration-300">
              <CardContent className="p-6 text-center">
                <div className="bg-gradient-ocean w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Shield className="h-8 w-8 text-white" />
                </div>
                <h4 className="text-xl font-semibold mb-3">Data Analytics</h4>
                <p className="text-muted-foreground">
                  Track trends, analyze patterns, and make data-driven decisions 
                  for effective coastal management.
                </p>
              </CardContent>
            </Card>
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
          <Button asChild size="lg" variant="secondary">
            <Link to="/register">Get Started Now</Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-card py-8">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Waves className="h-6 w-6 text-primary" />
            <span className="font-semibold">Coastal Protection Platform</span>
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