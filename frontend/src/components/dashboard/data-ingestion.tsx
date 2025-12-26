'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Key, CheckCircle2, AlertCircle, Loader2, FileUp, X, Lock } from 'lucide-react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { ingestFromAPI, ingestFromFile, checkOAuthAvailable, initiateOAuthLogin } from '../../lib/api';
import { cn } from '../../lib/utils';

interface DataIngestionProps {
  onSuccess: () => void;
}

type IngestionMethod = 'oauth' | 'api' | 'file' | null;
type IngestionStatus = 'idle' | 'loading' | 'success' | 'error';

export function DataIngestion({ onSuccess }: DataIngestionProps) {
  const [method, setMethod] = useState<IngestionMethod>(null);
  const [status, setStatus] = useState<IngestionStatus>('idle');
  const [message, setMessage] = useState('');
  const [apiToken, setApiToken] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [oauthAvailable, setOAuthAvailable] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Check OAuth availability on mount
  useEffect(() => {
    checkOAuthAvailable().then(setOAuthAvailable);
    
    // Check if coming from OAuth callback
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('oauth') === 'success') {
      // OAuth was successful, data should be loaded
      setStatus('success');
      setMessage('Successfully connected to Splitwise! Your data is being loaded...');
      setTimeout(() => {
        onSuccess();
        // Clean up URL
        window.history.replaceState({}, '', window.location.pathname);
      }, 2000);
    }
  }, [onSuccess]);

  const handleOAuthLogin = async () => {
    setStatus('loading');
    setMessage('Redirecting to Splitwise...');

    try {
      const authUrl = await initiateOAuthLogin();
      // Redirect to Splitwise OAuth page
      window.location.href = authUrl;
    } catch (err) {
      setStatus('error');
      setMessage(err instanceof Error ? err.message : 'Failed to initiate OAuth login');
    }
  };

  const handleAPISubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!apiToken.trim()) return;

    setStatus('loading');
    setMessage('Connecting to Splitwise API...');

    try {
      const result = await ingestFromAPI(apiToken);
      setStatus('success');
      setMessage(`Successfully imported ${result.expenses_count} expenses from ${result.groups_count} groups`);
      setTimeout(() => onSuccess(), 1500);
    } catch (err) {
      setStatus('error');
      setMessage(err instanceof Error ? err.message : 'Failed to ingest data');
    }
  };

  const handleFileSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setStatus('loading');
    setMessage('Processing file...');

    try {
      const result = await ingestFromFile(selectedFile);
      setStatus('success');
      setMessage(`Successfully imported ${result.expenses_count} expenses from ${result.groups_count} groups`);
      setTimeout(() => onSuccess(), 1500);
    } catch (err) {
      setStatus('error');
      setMessage(err instanceof Error ? err.message : 'Failed to process file');
    }
  };

  const handleFileDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && (file.name.endsWith('.csv') || file.name.endsWith('.json'))) {
      setSelectedFile(file);
      setMethod('file');
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="mx-auto max-w-2xl"
    >
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold">Connect Your Data</h2>
        <p className="mt-2 text-muted-foreground">
          Import your Splitwise data to get started with analytics
        </p>
      </div>

      {/* Method Selection */}
      <AnimatePresence mode="wait">
        {method === null && status === 'idle' && (
          <motion.div
            key="selection"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="space-y-4"
          >
            {/* OAuth Option (Primary) */}
            {oauthAvailable && (
              <motion.button
                onClick={handleOAuthLogin}
                className="group relative w-full rounded-xl border-2 border-primary bg-primary/5 p-8 text-left transition-all hover:border-primary hover:bg-primary/10"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <div className="flex items-center gap-4">
                  <div className="flex h-16 w-16 items-center justify-center rounded-lg bg-primary transition-colors group-hover:bg-primary/90">
                    <Lock className="h-8 w-8 text-primary-foreground" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold">Connect with Splitwise</h3>
                    <p className="mt-1 text-sm text-muted-foreground">
                      Secure OAuth login - no API token needed
                    </p>
                  </div>
                  <div className="text-primary">→</div>
                </div>
              </motion.button>
            )}

            {/* Alternative Methods */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="bg-background px-4 text-muted-foreground">
                  Or use alternative methods
                </span>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <button
                onClick={() => setMethod('api')}
                className="group relative rounded-xl border-2 border-dashed p-6 text-left transition-all hover:border-primary hover:bg-primary/5"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 transition-colors group-hover:bg-primary/20">
                  <Key className="h-5 w-5 text-primary" />
                </div>
                <h3 className="mt-3 font-semibold">API Token</h3>
                <p className="mt-1 text-xs text-muted-foreground">
                  Manual API token entry
                </p>
              </button>

              <button
                onClick={() => setMethod('file')}
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleFileDrop}
                className="group relative rounded-xl border-2 border-dashed p-6 text-left transition-all hover:border-primary hover:bg-primary/5"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 transition-colors group-hover:bg-primary/20">
                  <Upload className="h-5 w-5 text-primary" />
                </div>
                <h3 className="mt-3 font-semibold">Upload File</h3>
                <p className="mt-1 text-xs text-muted-foreground">
                  CSV or JSON export
                </p>
              </button>
            </div>
          </motion.div>
        )}

        {/* API Token Form */}
        {method === 'api' && status !== 'success' && (
          <motion.form
            key="api-form"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            onSubmit={handleAPISubmit}
            className="space-y-4"
          >
            <div className="flex items-center justify-between">
              <h3 className="font-semibold">Enter API Token</h3>
              <button
                type="button"
                onClick={() => { setMethod(null); setStatus('idle'); setMessage(''); }}
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                ← Back
              </button>
            </div>

            <Input
              type="password"
              placeholder="Your Splitwise API Token"
              value={apiToken}
              onChange={(e) => setApiToken(e.target.value)}
              disabled={status === 'loading'}
              className="h-12"
            />

            <p className="text-sm text-muted-foreground">
              Get your API token from{' '}
              <a
                href="https://secure.splitwise.com/apps"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary underline-offset-4 hover:underline"
              >
                secure.splitwise.com/apps
              </a>
            </p>

            <Button
              type="submit"
              variant="gradient"
              size="lg"
              className="w-full"
              disabled={!apiToken.trim() || status === 'loading'}
            >
              {status === 'loading' ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Importing...
                </>
              ) : (
                'Import Data'
              )}
            </Button>
          </motion.form>
        )}

        {/* File Upload Form */}
        {method === 'file' && status !== 'success' && (
          <motion.form
            key="file-form"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            onSubmit={handleFileSubmit}
            className="space-y-4"
          >
            <div className="flex items-center justify-between">
              <h3 className="font-semibold">Upload File</h3>
              <button
                type="button"
                onClick={() => { setMethod(null); setStatus('idle'); setMessage(''); setSelectedFile(null); }}
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                ← Back
              </button>
            </div>

            <div
              onClick={() => fileInputRef.current?.click()}
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleFileDrop}
              className={cn(
                'flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-8 transition-all',
                selectedFile ? 'border-primary bg-primary/5' : 'hover:border-primary hover:bg-primary/5'
              )}
            >
              {selectedFile ? (
                <div className="flex items-center gap-3">
                  <FileUp className="h-8 w-8 text-primary" />
                  <div>
                    <p className="font-medium">{selectedFile.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {(selectedFile.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={(e) => { e.stopPropagation(); setSelectedFile(null); }}
                    className="ml-4 rounded-full p-1 hover:bg-muted"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ) : (
                <>
                  <Upload className="h-12 w-12 text-muted-foreground" />
                  <p className="mt-4 font-medium">Drop your file here</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    or click to browse
                  </p>
                </>
              )}
            </div>

            <input
              ref={fileInputRef}
              type="file"
              accept=".csv,.json"
              className="hidden"
              onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
            />

            <Button
              type="submit"
              variant="gradient"
              size="lg"
              className="w-full"
              disabled={!selectedFile || status === 'loading'}
            >
              {status === 'loading' ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Processing...
                </>
              ) : (
                'Import File'
              )}
            </Button>
          </motion.form>
        )}

        {/* Status Messages */}
        {status === 'success' && (
          <motion.div
            key="success"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex flex-col items-center rounded-xl bg-success/10 p-8 text-center"
          >
            <CheckCircle2 className="h-12 w-12 text-success" />
            <h3 className="mt-4 font-semibold text-success">Success!</h3>
            <p className="mt-2 text-muted-foreground">{message}</p>
          </motion.div>
        )}

        {status === 'error' && (
          <motion.div
            key="error"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="rounded-xl bg-destructive/10 p-4"
          >
            <div className="flex items-center gap-3">
              <AlertCircle className="h-5 w-5 text-destructive" />
              <p className="text-destructive">{message}</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              className="mt-4"
              onClick={() => setStatus('idle')}
            >
              Try Again
            </Button>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
