import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { 
  Waves, 
  AlertTriangle, 
  FileText, 
  Trophy, 
  TrendingUp, 
  Settings,
  MapPin,
  Users,
  Plus
} from "lucide-react";
import { Link, useLocation } from "react-router-dom";

const Dashboard = () => {
  const location = useLocation();
  const [userRole] = useState<"authority" | "ngo" | "community">("community"); // Mock role

  const navigationItems = [
    { title: "Dashboard", url: "/dashboard", icon: Waves },
    { title: "Alerts", url: "/alerts", icon: AlertTriangle },
    { title: "Reports", url: "/reports", icon: FileText },
    { title: "Leaderboard", url: "/leaderboard", icon: Trophy },
    { title: "Trends", url: "/trends", icon: TrendingUp },
    { title: "Settings", url: "/settings", icon: Settings },
  ];

  const isActive = (path: string) => location.pathname === path;

  const getNavClass = (path: string) => 
    isActive(path) ? "bg-muted text-primary font-medium" : "hover:bg-muted/50";

  const mockAlerts = [
    { id: 1, type: "Sea Level Rise", severity: "high", location: "Mumbai Coast", time: "2 hours ago" },
    { id: 2, type: "Coral Bleaching", severity: "medium", location: "Goa Beach", time: "5 hours ago" },
    { id: 3, type: "Pollution Detected", severity: "low", location: "Chennai Port", time: "1 day ago" }
  ];

  const mockReports = [
    { id: 1, type: "Mangrove Damage", reporter: "Local Fisher", location: "Sundarbans", status: "verified" },
    { id: 2, type: "Plastic Waste", reporter: "Beach Cleaner", location: "Juhu Beach", status: "pending" },
  ];

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-gradient-wave">
        <Sidebar className="border-r">
          <SidebarContent>
            <div className="p-4 border-b">
              <div className="flex items-center gap-2">
                <Waves className="h-6 w-6 text-primary" />
                <span className="font-semibold text-sm">Coastal Protection</span>
              </div>
            </div>
            
            <SidebarGroup>
              <SidebarGroupLabel>Navigation</SidebarGroupLabel>
              <SidebarGroupContent>
                <SidebarMenu>
                  {navigationItems.map((item) => (
                    <SidebarMenuItem key={item.title}>
                      <SidebarMenuButton asChild>
                        <Link to={item.url} className={getNavClass(item.url)}>
                          <item.icon className="h-4 w-4" />
                          <span>{item.title}</span>
                        </Link>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  ))}
                </SidebarMenu>
              </SidebarGroupContent>
            </SidebarGroup>
          </SidebarContent>
        </Sidebar>

        <main className="flex-1 p-6">
          <header className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-4">
              <SidebarTrigger />
              <div>
                <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
                <p className="text-muted-foreground">Welcome back to your coastal protection center</p>
              </div>
            </div>
            <Badge variant="outline" className="capitalize">
              {userRole} User
            </Badge>
          </header>

          <div className="grid lg:grid-cols-3 gap-6 mb-8">
            <Card className="border-0 shadow-soft">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Active Alerts</CardTitle>
                <AlertTriangle className="h-4 w-4 text-warning" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">12</div>
                <p className="text-xs text-muted-foreground">
                  +2 from last hour
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-soft">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Community Reports</CardTitle>
                <FileText className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">247</div>
                <p className="text-xs text-muted-foreground">
                  +18 this week
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-soft">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Your Points</CardTitle>
                <Trophy className="h-4 w-4 text-accent" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">1,420</div>
                <p className="text-xs text-muted-foreground">
                  Rank #23 globally
                </p>
              </CardContent>
            </Card>
          </div>

          <div className="grid lg:grid-cols-2 gap-6">
            <Card className="border-0 shadow-medium">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5" />
                  Recent Alerts
                </CardTitle>
                <CardDescription>Latest coastal threats in your area</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockAlerts.map((alert) => (
                    <div key={alert.id} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className={`w-3 h-3 rounded-full ${
                          alert.severity === 'high' ? 'bg-destructive' : 
                          alert.severity === 'medium' ? 'bg-warning' : 'bg-success'
                        }`} />
                        <div>
                          <p className="font-medium text-sm">{alert.type}</p>
                          <p className="text-xs text-muted-foreground flex items-center gap-1">
                            <MapPin className="h-3 w-3" />
                            {alert.location}
                          </p>
                        </div>
                      </div>
                      <span className="text-xs text-muted-foreground">{alert.time}</span>
                    </div>
                  ))}
                </div>
                <Button asChild variant="outline" className="w-full mt-4">
                  <Link to="/alerts">View All Alerts</Link>
                </Button>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-medium">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Community Activity
                </CardTitle>
                <CardDescription>Recent reports from your network</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockReports.map((report) => (
                    <div key={report.id} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                      <div>
                        <p className="font-medium text-sm">{report.type}</p>
                        <p className="text-xs text-muted-foreground">by {report.reporter}</p>
                        <p className="text-xs text-muted-foreground flex items-center gap-1">
                          <MapPin className="h-3 w-3" />
                          {report.location}
                        </p>
                      </div>
                      <Badge 
                        variant={report.status === 'verified' ? 'default' : 'secondary'}
                        className="text-xs"
                      >
                        {report.status}
                      </Badge>
                    </div>
                  ))}
                </div>
                <div className="flex gap-2 mt-4">
                  {userRole === 'community' && (
                    <Button asChild variant="ocean" className="flex-1">
                      <Link to="/reports" className="flex items-center gap-2">
                        <Plus className="h-4 w-4" />
                        Report Incident
                      </Link>
                    </Button>
                  )}
                  <Button asChild variant="outline" className="flex-1">
                    <Link to="/reports">View All</Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
};

export default Dashboard;