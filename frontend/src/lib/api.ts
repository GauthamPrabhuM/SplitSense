import useSWR from 'swr';
import type { Insights, IngestResponse } from '../types/api';

const fetcher = async (url: string) => {
  const res = await fetch(url);
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'An error occurred');
  }
  return res.json();
};

export function useInsights() {
  const { data, error, isLoading, mutate } = useSWR<Insights>('/api/insights', fetcher, {
    revalidateOnFocus: false,
    shouldRetryOnError: false,
  });

  return {
    insights: data,
    isLoading,
    isError: error,
    refresh: mutate,
  };
}

export interface FriendBalance {
  user_id: number;
  first_name: string;
  last_name?: string;
  email?: string;
  balance: number;  // Positive = they owe you, Negative = you owe them
  currency_code: string;
}

export interface FriendsResponse {
  friends: FriendBalance[];
}

export function useFriends() {
  const { data, error, isLoading, mutate } = useSWR<FriendsResponse>('/api/friends', fetcher, {
    revalidateOnFocus: false,
    shouldRetryOnError: false,
  });

  return {
    friends: data?.friends || [],
    isLoading,
    isError: error,
    refresh: mutate,
  };
}

export async function ingestFromAPI(apiToken: string): Promise<IngestResponse> {
  const res = await fetch('/api/ingest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_token: apiToken, base_currency: 'USD' }),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Ingestion failed');
  }

  return res.json();
}

export async function ingestFromFile(file: File): Promise<IngestResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('base_currency', 'USD');

  const res = await fetch('/api/ingest/file', {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'File ingestion failed');
  }

  return res.json();
}

// OAuth functions
export interface OAuthLoginResponse {
  auth_url: string;
  state: string;
  redirect_uri?: string;
}

export async function checkOAuthAvailable(): Promise<boolean> {
  try {
    const res = await fetch('/api/health');
    if (!res.ok) return false;
    const data = await res.json();
    return data.oauth_available === true;
  } catch {
    return false;
  }
}

export async function initiateOAuthLogin(): Promise<string> {
  const res = await fetch('/auth/login');
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Failed to initiate OAuth login');
  }
  const data: OAuthLoginResponse = await res.json();
  return data.auth_url;
}
