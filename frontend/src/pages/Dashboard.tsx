import { useState, useEffect } from 'react';
import { Brain, Eye, MessageSquare, CheckCircle2, Loader2 } from 'lucide-react';

const Dashboard = () => {
  const [activeAgent, setActiveAgent] = useState(0);

  const agents = [
    {
      name: 'Researcher',
      icon: Brain,
      status: 'Reading and summarizing sources...',
      color: 'bg-primary',
      progress: 100,
    },
    {
      name: 'Reviewer A',
      icon: Eye,
      status: 'Analyzing logical consistency...',
      color: 'bg-secondary',
      progress: 100,
    },
    {
      name: 'Reviewer B',
      icon: Eye,
      status: 'Identifying gaps and biases...',
      color: 'bg-secondary',
      progress: 100,
    },
    {
      name: 'Synthesizer',
      icon: MessageSquare,
      status: 'Generating collective insights...',
      color: 'bg-accent',
      progress: 75,
    },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveAgent((prev) => (prev + 1) % agents.length);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 text-foreground">Agent Collaboration</h1>
          <p className="text-muted-foreground text-lg">
            Watch as AI agents analyze and debate your research topic
          </p>
        </div>

        {/* Agent Network Visualization */}
        <div className="bg-card rounded-2xl shadow-lg border border-border p-8 mb-8">
          <div className="relative">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {agents.map((agent, index) => {
                const Icon = agent.icon;
                const isActive = index === activeAgent;

                return (
                  <div key={agent.name} className="flex flex-col items-center space-y-3">
                    <div
                      className={`w-24 h-24 ${agent.color} rounded-2xl flex items-center justify-center transition-all duration-300 ${
                        isActive ? 'scale-110 shadow-lg animate-pulse-glow' : 'opacity-60'
                      }`}
                    >
                      <Icon className="w-12 h-12 text-white" />
                    </div>
                    <div className="text-center">
                      <h3 className="font-semibold text-foreground">{agent.name}</h3>
                      {isActive && (
                        <p className="text-xs text-accent mt-1">Active</p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Connecting Lines (decorative) */}
            <svg className="absolute inset-0 pointer-events-none" style={{ zIndex: -1 }}>
              <line
                x1="25%"
                y1="50%"
                x2="50%"
                y2="50%"
                stroke="hsl(var(--border))"
                strokeWidth="2"
                strokeDasharray="5,5"
              />
              <line
                x1="50%"
                y1="50%"
                x2="75%"
                y2="50%"
                stroke="hsl(var(--border))"
                strokeWidth="2"
                strokeDasharray="5,5"
              />
            </svg>
          </div>
        </div>

        {/* Agent Status Cards */}
        <div className="space-y-4">
          {agents.map((agent, index) => {
            const Icon = agent.icon;
            const isComplete = agent.progress === 100;
            const isActive = index === activeAgent;

            return (
              <div
                key={agent.name}
                className={`bg-card rounded-xl shadow-md border p-6 transition-all ${
                  isActive ? 'border-accent shadow-lg' : 'border-border'
                }`}
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-4">
                    <div className={`w-12 h-12 ${agent.color} rounded-lg flex items-center justify-center`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-foreground">{agent.name}</h3>
                      <p className="text-sm text-muted-foreground">{agent.status}</p>
                    </div>
                  </div>
                  {isComplete ? (
                    <CheckCircle2 className="w-6 h-6 text-green-500" />
                  ) : (
                    <Loader2 className="w-6 h-6 text-accent animate-spin" />
                  )}
                </div>

                {/* Progress Bar */}
                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className={`${agent.color} h-2 rounded-full transition-all duration-500`}
                    style={{ width: `${agent.progress}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        {/* Communication Log */}
        <div className="mt-8 bg-card rounded-xl shadow-md border border-border p-6">
          <h3 className="font-semibold text-foreground mb-4">Agent Communication Log</h3>
          <div className="space-y-3 text-sm">
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-primary rounded-full mt-2" />
              <p className="text-muted-foreground">
                <span className="text-foreground font-medium">Researcher:</span> Completed summary
                of 6 sources with 4 key findings
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-secondary rounded-full mt-2" />
              <p className="text-muted-foreground">
                <span className="text-foreground font-medium">Reviewer A:</span> Identified 3
                logical inconsistencies requiring additional support
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-secondary rounded-full mt-2" />
              <p className="text-muted-foreground">
                <span className="text-foreground font-medium">Reviewer B:</span> Found 2
                alternative interpretations worth exploring
              </p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-accent rounded-full mt-2 animate-pulse" />
              <p className="text-muted-foreground">
                <span className="text-foreground font-medium">Synthesizer:</span> Generating
                collective insights and testable hypotheses...
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
