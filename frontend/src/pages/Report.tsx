import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Brain, Eye, MessageSquare, ArrowLeft, ExternalLink } from 'lucide-react';
import { ResearchResponse } from '@/lib/api';

const Report = () => {
  const navigate = useNavigate();
  const [result, setResult] = useState<ResearchResponse | null>(null);

  useEffect(() => {
    const storedResult = sessionStorage.getItem('researchResult');
    if (storedResult) {
      setResult(JSON.parse(storedResult));
    }
  }, []);

  if (!result) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto text-center">
          <FileText className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
          <h2 className="text-2xl font-semibold mb-4 text-foreground">No Report Available</h2>
          <p className="text-muted-foreground mb-6">
            Start a research session to generate a collective insight report.
          </p>
          <button
            onClick={() => navigate('/upload')}
            className="bg-accent text-accent-foreground px-6 py-3 rounded-lg font-medium hover:opacity-90 transition-opacity"
          >
            Start Research
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/upload')}
            className="flex items-center space-x-2 text-muted-foreground hover:text-foreground mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>New Research</span>
          </button>
          
          <h1 className="text-4xl font-bold mb-2 text-foreground">Collective Insight Report</h1>
          <p className="text-lg text-accent">Topic: {result.topic}</p>
        </div>

        {/* Summary Section */}
        <div className="bg-card rounded-xl shadow-lg border border-border p-8 mb-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <Brain className="w-5 h-5 text-primary-foreground" />
            </div>
            <h2 className="text-2xl font-semibold text-foreground">Research Summary</h2>
          </div>
          <div className="prose prose-slate max-w-none">
            <p className="text-foreground whitespace-pre-line">{result.summary}</p>
          </div>
        </div>

        {/* Critiques Section */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          {/* Critique A */}
          <div className="bg-card rounded-xl shadow-lg border border-border p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
                <Eye className="w-5 h-5 text-secondary-foreground" />
              </div>
              <h3 className="text-xl font-semibold text-foreground">Reviewer A</h3>
            </div>
            <div className="prose prose-sm prose-slate max-w-none">
              <p className="text-foreground whitespace-pre-line text-sm">{result.critique_a}</p>
            </div>
          </div>

          {/* Critique B */}
          <div className="bg-card rounded-xl shadow-lg border border-border p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
                <Eye className="w-5 h-5 text-secondary-foreground" />
              </div>
              <h3 className="text-xl font-semibold text-foreground">Reviewer B</h3>
            </div>
            <div className="prose prose-sm prose-slate max-w-none">
              <p className="text-foreground whitespace-pre-line text-sm">{result.critique_b}</p>
            </div>
          </div>
        </div>

        {/* Collective Insight */}
        <div className="bg-gradient-to-br from-accent/10 to-primary/10 rounded-xl shadow-lg border-2 border-accent p-8 mb-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-accent rounded-lg flex items-center justify-center">
              <MessageSquare className="w-5 h-5 text-accent-foreground" />
            </div>
            <h2 className="text-2xl font-semibold text-foreground">Collective Insight</h2>
          </div>
          <div className="prose prose-slate max-w-none">
            <p className="text-foreground whitespace-pre-line">{result.insight}</p>
          </div>
        </div>

        {/* Sources */}
        {result.sources && result.sources.length > 0 && (
          <div className="bg-card rounded-xl shadow-lg border border-border p-8">
            <h3 className="text-xl font-semibold mb-4 text-foreground">Sources & References</h3>
            <div className="space-y-3">
              {result.sources.map((source, index) => (
                <div
                  key={index}
                  className="flex items-start space-x-3 p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors"
                >
                  <ExternalLink className="w-4 h-4 text-accent mt-1 flex-shrink-0" />
                  <span className="text-sm text-foreground">{source}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Report;
