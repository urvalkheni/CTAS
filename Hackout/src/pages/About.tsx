import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Waves, Eye, AlertTriangle, Users, BarChart3, MapPin, ArrowLeft } from "lucide-react";

const About = () => {
  return (
    <div className="min-h-screen bg-gradient-wave">
      {/* Header */}
      <header className="border-b bg-card/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Waves className="h-8 w-8 text-primary" />
            <h1 className="text-xl font-bold text-foreground">Coastal Protection Platform</h1>
          </div>
          <Button asChild variant="ghost">
            <Link to="/" className="flex items-center gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Home
            </Link>
          </Button>
        </div>
      </header>

      <div className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <section className="text-center mb-16">
          <h1 className="text-4xl font-bold text-foreground mb-6">
            About Our Platform
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Our comprehensive coastal protection platform combines cutting-edge technology 
            with community engagement to safeguard coastlines and preserve marine ecosystems.
          </p>
        </section>

        {/* Main Features */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center text-foreground mb-12">
            Two Core Systems
          </h2>
          
          <div className="grid lg:grid-cols-2 gap-8 mb-12">
            <Card className="border-0 shadow-medium">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="bg-gradient-alert w-12 h-12 rounded-lg flex items-center justify-center">
                    <AlertTriangle className="h-6 w-6 text-white" />
                  </div>
                  <CardTitle className="text-2xl">Coastal Threat Alert</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground mb-4">
                  Real-time monitoring and early warning system for coastal threats including 
                  sea level rise, erosion, pollution, and extreme weather events.
                </p>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-primary rounded-full"></div>
                    AI-powered anomaly detection
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-primary rounded-full"></div>
                    Automated alert notifications
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-primary rounded-full"></div>
                    Multi-channel communication
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-primary rounded-full"></div>
                    Severity-based response protocols
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-medium">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="bg-gradient-ocean w-12 h-12 rounded-lg flex items-center justify-center">
                    <Eye className="h-6 w-6 text-white" />
                  </div>
                  <CardTitle className="text-2xl">Mangrove Watch</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground mb-4">
                  Community-driven monitoring and conservation platform for mangrove ecosystems, 
                  enabling collaborative protection efforts.
                </p>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-accent rounded-full"></div>
                    Community reporting tools
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-accent rounded-full"></div>
                    Geotagged photo documentation
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-accent rounded-full"></div>
                    Gamification and leaderboards
                  </li>
                  <li className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-accent rounded-full"></div>
                    Progress tracking and analytics
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Platform Features */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-center text-foreground mb-12">
            Platform Features
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card className="border-0 shadow-soft">
              <CardContent className="p-6 text-center">
                <Users className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Role-Based Access</h3>
                <p className="text-sm text-muted-foreground">
                  Tailored experiences for Authorities, NGOs, and Community members
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-soft">
              <CardContent className="p-6 text-center">
                <MapPin className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Interactive Maps</h3>
                <p className="text-sm text-muted-foreground">
                  Visual representation of alerts, reports, and coastal data
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-soft">
              <CardContent className="p-6 text-center">
                <BarChart3 className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Analytics Dashboard</h3>
                <p className="text-sm text-muted-foreground">
                  Comprehensive insights and trend analysis
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-soft">
              <CardContent className="p-6 text-center">
                <AlertTriangle className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Real-time Alerts</h3>
                <p className="text-sm text-muted-foreground">
                  Instant notifications for threats and emergencies
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-soft">
              <CardContent className="p-6 text-center">
                <Users className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Community Reports</h3>
                <p className="text-sm text-muted-foreground">
                  Crowd-sourced incident reporting and verification
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-soft">
              <CardContent className="p-6 text-center">
                <BarChart3 className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Leaderboards</h3>
                <p className="text-sm text-muted-foreground">
                  Gamified engagement and community recognition
                </p>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Call to Action */}
        <section className="text-center">
          <Card className="border-0 shadow-strong bg-gradient-ocean">
            <CardContent className="p-12">
              <h2 className="text-3xl font-bold text-white mb-4">
                Join Our Mission
              </h2>
              <p className="text-white/90 text-lg mb-8 max-w-2xl mx-auto">
                Be part of a global community working together to protect our coastlines 
                and preserve marine ecosystems for future generations.
              </p>
              <div className="flex gap-4 justify-center flex-wrap">
                <Button asChild size="lg" variant="secondary">
                  <Link to="/register">Get Started</Link>
                </Button>
                <Button asChild size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-primary">
                  <Link to="/login">Sign In</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </section>
      </div>
    </div>
  );
};

export default About;