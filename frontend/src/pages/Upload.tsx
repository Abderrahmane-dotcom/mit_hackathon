import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Loader2 } from 'lucide-react';
import { researchAPI } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

const Upload = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [topic, setTopic] = useState('');
  const [useWikipedia, setUseWikipedia] = useState(true);
  const [useArxiv, setUseArxiv] = useState(true);
  const [useLocalPdfs, setUseLocalPdfs] = useState(false);
  const [localPdfCount, setLocalPdfCount] = useState<number | null>(null);
  const [maxWikipediaArticles, setMaxWikipediaArticles] = useState(3);
  const [maxArxivPapers, setMaxArxivPapers] = useState(3);
  const [isResearching, setIsResearching] = useState(false);

  const handleStartResearch = async () => {
    if (!topic.trim()) {
      toast({
        title: 'Error',
        description: 'Please enter a research topic',
        variant: 'destructive',
      });
      return;
    }

    setIsResearching(true);

    try {
      // Start research
      const result = await researchAPI.research({
        topic,
        // If user selected local PDFs, disable external scrapers
        use_wikipedia: useLocalPdfs ? false : useWikipedia,
        use_arxiv: useLocalPdfs ? false : useArxiv,
        max_wikipedia_articles: maxWikipediaArticles,
        max_arxiv_papers: maxArxivPapers,
      });

      // Store result in sessionStorage for Report page
      sessionStorage.setItem('researchResult', JSON.stringify(result));

      toast({
        title: 'Research Complete!',
        description: 'Analysis finished successfully',
      });

      // Navigate to report
      navigate('/report');
    } catch (error: any) {
      console.error('Research failed:', error);
      toast({
        title: 'Research Failed',
        description: error.response?.data?.detail || error.message || 'Failed to complete research',
        variant: 'destructive',
      });
    } finally {
      setIsResearching(false);
    }
  };

  useEffect(() => {
    // Fetch health to get pdf_count
    let mounted = true;
    (async () => {
      try {
        const health = await researchAPI.health();
        if (!mounted) return;
        // health may include pdf_count (backend provides it)
        // @ts-ignore - optional field added to type
        setLocalPdfCount(health.pdf_count ?? null);
      } catch (err) {
        console.warn('Failed to fetch health info', err);
      }
    })();

    return () => {
      mounted = false;
    };
  }, []);

  const handleReinitialize = async () => {
    try {
      setIsResearching(true);
      await researchAPI.reinitialize();
      // refresh health
      const health = await researchAPI.health();
      // @ts-ignore
      setLocalPdfCount(health.pdf_count ?? null);
      toast({ title: 'Reinitialized', description: 'PDF index refreshed' });
    } catch (err: any) {
      console.error('Reinitialize failed', err);
      toast({ title: 'Reinitialize failed', description: err.message || 'Failed' , variant: 'destructive'});
    } finally {
      setIsResearching(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4 text-foreground">Start Your Research</h1>
          <p className="text-muted-foreground text-lg">
            Enter a topic and configure your research parameters
          </p>
        </div>

        <div className="bg-card rounded-2xl shadow-lg border border-border p-8 space-y-8">
          {/* Topic Input */}
          <div className="space-y-3">
            <label htmlFor="topic" className="block text-sm font-medium text-foreground">
              Research Topic *
            </label>
              <input
                id="topic"
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., quantum computing, machine learning, CRISPR gene editing"
                className="w-full px-4 py-3 rounded-lg border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                disabled={isResearching}
              />
          </div>

          {/* Source Configuration */}
            <div className="space-y-4">
            <h3 className="text-lg font-semibold text-foreground">Data Sources</h3>
            
            {/* Local PDFs info */}
            <div className="flex items-center justify-between p-3 rounded-lg border border-border bg-muted/20">
              <div className="space-y-1">
                <div className="text-sm text-foreground font-medium">Local PDFs</div>
                <div className="text-xs text-muted-foreground">Located in backend/files</div>
              </div>
              <div className="flex items-center space-x-3">
                <div className="text-sm text-foreground">{localPdfCount ?? '—'}</div>
                <button
                  onClick={handleReinitialize}
                  className="px-3 py-1 bg-accent text-accent-foreground rounded-md text-sm hover:opacity-90"
                  disabled={isResearching}
                >
                  Reindex
                </button>
              </div>
            </div>

            <div className="flex items-center space-x-3 mt-2">
              <input
                type="checkbox"
                id="localPdfs"
                checked={useLocalPdfs}
                onChange={(e) => {
                  const checked = e.target.checked;
                  setUseLocalPdfs(checked);
                  // If using local PDFs, turn off external scrapers by default
                  if (checked) {
                    setUseWikipedia(false);
                    setUseArxiv(false);
                  }
                }}
                className="w-4 h-4 text-accent border-input rounded focus:ring-accent"
                disabled={isResearching}
              />
              <label htmlFor="localPdfs" className="font-medium text-foreground">Use Local PDFs Only</label>
            </div>
            <div className="grid md:grid-cols-2 gap-6">
              {/* Wikipedia */}
              <div className="space-y-3 p-4 rounded-lg border border-border bg-muted/30">
                <div className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    id="wikipedia"
                    checked={useWikipedia}
                    onChange={(e) => setUseWikipedia(e.target.checked)}
                    className="w-4 h-4 text-accent border-input rounded focus:ring-accent"
                    disabled={isResearching}
                  />
                  <label htmlFor="wikipedia" className="font-medium text-foreground">
                    Wikipedia
                  </label>
                </div>
                {useWikipedia && (
                  <div className="ml-7 space-y-2">
                    <label htmlFor="maxWikipediaArticles" className="block text-sm text-muted-foreground">
                      Max Articles
                    </label>
                    <input
                      id="maxWikipediaArticles"
                      type="number"
                      min="1"
                      max="10"
                      value={maxWikipediaArticles}
                      onChange={(e) => setMaxWikipediaArticles(Number.parseInt(e.target.value))}
                      className="w-20 px-3 py-1 rounded border border-input bg-background text-foreground"
                      disabled={isResearching}
                    />
                  </div>
                )}
              </div>

              {/* ArXiv */}
              <div className="space-y-3 p-4 rounded-lg border border-border bg-muted/30">
                <div className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    id="arxiv"
                    checked={useArxiv}
                    onChange={(e) => setUseArxiv(e.target.checked)}
                    className="w-4 h-4 text-accent border-input rounded focus:ring-accent"
                    disabled={isResearching}
                  />
                  <label htmlFor="arxiv" className="font-medium text-foreground">
                    ArXiv Papers
                  </label>
                </div>
                {useArxiv && (
                  <div className="ml-7 space-y-2">
                    <label htmlFor="maxArxivPapers" className="block text-sm text-muted-foreground">
                      Max Papers
                    </label>
                    <input
                      id="maxArxivPapers"
                      type="number"
                      min="1"
                      max="10"
                      value={maxArxivPapers}
                      onChange={(e) => setMaxArxivPapers(Number.parseInt(e.target.value))}
                      className="w-20 px-3 py-1 rounded border border-input bg-background text-foreground"
                      disabled={isResearching}
                    />
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Info Box */}
          <div className="bg-accent/10 border border-accent/20 rounded-lg p-4">
            <p className="text-sm text-foreground">
              <strong>Note:</strong> The research process involves multiple AI agents analyzing sources,
              generating critiques, and synthesizing insights. This may take 30-60 seconds depending on
              the complexity of your topic.
            </p>
          </div>

          {/* Start Button */}
          <button
            onClick={handleStartResearch}
            disabled={isResearching || !topic.trim()}
            className="w-full bg-accent text-accent-foreground py-4 rounded-lg font-semibold hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {isResearching ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Researching...</span>
              </>
            ) : (
              <>
                <FileText className="w-5 h-5" />
                <span>Start Research</span>
              </>
            )}
          </button>
        </div>

        {/* Loading State */}
        {isResearching && (
          <div className="mt-8 bg-card rounded-xl shadow-lg border border-border p-6">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <Loader2 className="w-5 h-5 animate-spin text-accent" />
                <span className="font-medium text-foreground">Research in progress...</span>
              </div>
              <div className="space-y-2 text-sm text-muted-foreground">
                <p>• Fetching sources from Wikipedia and ArXiv...</p>
                <p>• Researcher agent analyzing content...</p>
                <p>• Reviewer agents critiquing findings...</p>
                <p>• Synthesizer generating collective insights...</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Upload;
