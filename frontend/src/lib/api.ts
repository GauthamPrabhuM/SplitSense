import useSWR from 'swr';
import type { Insights, IngestResponse } from '../types/api';

// Fetcher with credentials (sends cookies)
const fetcher = async (url: string) => {
  const res = await fetch(url, {
    credentials: 'include',  // Include cookies for session auth
  });
  if (!res.ok) {
    // Handle 401 specifically for auth errors
    if (res.status === 401) {
      const error = new Error('Not authenticated');
      (error as any).status = 401;
      throw error;
    }
    const error = await res.json();
    throw new Error(error.detail || 'An error occurred');
  }
  return res.json();
};

// User info type
export interface UserInfo {
  user_id: number;
  first_name: string;
  last_name: string;
  email?: string;
  has_data: boolean;
  expenses_count: number;
  groups_count: number;
}

// Hook to get current user (checks authentication)
export function useCurrentUser() {
  const { data, error, isLoading, mutate } = useSWR<UserInfo>('/api/me', fetcher, {
    revalidateOnFocus: false,
    shouldRetryOnError: false,
  });

  const isAuthenticated = !!data && !error;
  const isAuthError = error?.status === 401 || error?.message?.includes('Not authenticated');

  return {
    user: data,
    isLoading,
    isAuthenticated,
    isAuthError,
    refresh: mutate,
  };
}

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
  const res = await fetch('/auth/login', {
    credentials: 'include',
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Failed to initiate OAuth login');
  }
  const data: OAuthLoginResponse = await res.json();
  return data.auth_url;
}

// Logout function
export async function logout(): Promise<void> {
  await fetch('/auth/logout', {
    method: 'POST',
    credentials: 'include',
  });
  // Redirect to home page after logout
  window.location.href = '/';
}

// Refresh user data from Splitwise API
export async function refreshUserData(): Promise<IngestResponse> {
  const res = await fetch('/api/refresh', {
    method: 'POST',
    credentials: 'include',
  });
  
  if (!res.ok) {
    if (res.status === 401) {
      throw new Error('Session expired. Please log in again.');
    }
    const error = await res.json();
    throw new Error(error.detail || 'Failed to refresh data');
  }
  
  return res.json();
}
