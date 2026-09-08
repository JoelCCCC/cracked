"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { User } from "@/types";
import { api, getAccessToken, clearTokens } from "@/lib/api";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (data: {
    username: string;
    email: string;
    password: string;
    display_name?: string;
  }) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  quickDemoLogin: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    const token = getAccessToken();
    if (!token) {
      try {
        const res = await api.auth.personalLogin();
        setUser(res.user);
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
      return;
    }

    try {
      const u = await api.auth.me();
      setUser(u);
    } catch {
      try {
        const res = await api.auth.personalLogin();
        setUser(res.user);
      } catch {
        clearTokens();
        setUser(null);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = async (username: string, password: string) => {
    await api.auth.login({ username, password });
    await refreshUser();
  };

  const register = async (data: {
    username: string;
    email: string;
    password: string;
    display_name?: string;
  }) => {
    const res = await api.auth.register(data);
    setUser(res.user);
  };

  const logout = () => {
    api.auth.logout();
    setUser(null);
  };

  const quickDemoLogin = async () => {
    try {
      await login("demo", "cracked123");
    } catch {
      // If demo user wasn't registered for some reason, register it
      await register({
        username: "demo",
        email: "demo@cracked.dev",
        password: "cracked123",
        display_name: "Demo Hacker",
      });
      await refreshUser();
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        refreshUser,
        quickDemoLogin,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
