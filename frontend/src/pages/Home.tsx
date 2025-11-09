import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Brain, Eye, MessageSquare, CheckCircle2, Zap, Upload, FileText } from 'lucide-react';
import { researchAPI } from '@/lib/api';

const Home = () => {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const data = await researchAPI.health();
        setStatus(data);
      } catch (error) {
        console.error('Failed to fetch status:', error);
      } finally {
        setLoading(false);
      }
    };
    
    checkStatus();
  }, []);

  const agents = [
    {
      name: 'Researcher',
      icon: Brain,
      description: 'Reads and summarizes research papers with context',
      color: 'bg-primary',
    },
    {
      name: 'Reviewer A',
      icon: Eye,
      description: 'Critiques logical consistency and evidence support',
      color: 'bg-secondary',
    },
    {
      name: 'Reviewer B',
      icon: Eye,
      description: 'Identifies gaps, biases, and alternative views',
      color: 'bg-secondary',
    },
    {
      name: 'Synthesizer',
      icon: MessageSquare,
      description: 'Combines insights into actionable hypotheses',
      color: 'bg-accent',
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto text-center space-y-6">
          <div className="inline-block">
            <div className="w-24 h-24 bg-gradient-to-br from-primary to-accent rounded-2xl mx-auto mb-6 flex items-center justify-center animate-float shadow-lg">
              <Brain className="w-12 h-12 text-white" />
            </div>
          </div>
          
          <h1 className="text-5xl font-bold text-foreground">
            Research Agent
          </h1>
          
          <p className="text-2xl text-accent font-medium">
            Agentic AI for Accelerated Research
          </p>
          
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Harness the power of collaborative AI agents to analyze research papers,
            generate critical insights, and accelerate scientific discovery.
          </p>

          {!loading && (
            <div className="flex items-center justify-center space-x-2 text-sm">
              {status?.status === 'ok' ? (
                <>
                  <CheckCircle2 className="w-4 h-4 text-green-500" />
                  <span className="text-muted-foreground">
                    System Ready
                  </span>
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4 text-yellow-500" />
                  <span className="text-muted-foreground">Initializing...</span>
                </>
              )}
            </div>
          )}

          <div className="pt-4">
            <Link
              to="/upload"
              className="inline-flex items-center space-x-2 bg-accent text-accent-foreground px-8 py-4 rounded-lg font-medium hover:opacity-90 transition-opacity shadow-lg"
            >
              <span>Start Research</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-foreground">
            How It Works
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-card p-6 rounded-xl shadow-md border border-border">
              <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center mb-4">
                <Upload className="w-6 h-6 text-primary-foreground" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-foreground">1. Upload Sources</h3>
              <p className="text-muted-foreground">
                Upload PDFs or fetch papers from arXiv and Wikipedia on your research topic.
              </p>
            </div>

            <div className="bg-card p-6 rounded-xl shadow-md border border-border">
              <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center mb-4">
                <Brain className="w-6 h-6 text-accent-foreground" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-foreground">2. Agent Analysis</h3>
              <p className="text-muted-foreground">
                Multiple AI agents collaborate to read, critique, and debate the research.
              </p>
            </div>

            <div className="bg-card p-6 rounded-xl shadow-md border border-border">
              <div className="w-12 h-12 bg-secondary rounded-lg flex items-center justify-center mb-4">
                <FileText className="w-6 h-6 text-secondary-foreground" />
              </div>
              <h3 className="text-xl font-semibold mb-2 text-foreground">3. Get Insights</h3>
              <p className="text-muted-foreground">
                Receive a comprehensive report with actionable hypotheses and citations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Agents Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12 text-foreground">
            Meet the Agents
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {agents.map((agent) => {
              const Icon = agent.icon;
              return (
                <div
                  key={agent.name}
                  className="bg-card p-6 rounded-xl shadow-md border border-border hover:shadow-lg transition-shadow"
                >
                  <div className={`w-16 h-16 ${agent.color} rounded-xl flex items-center justify-center mb-4 mx-auto`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-center mb-2 text-foreground">
                    {agent.name}
                  </h3>
                  <p className="text-sm text-muted-foreground text-center">
                    {agent.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
