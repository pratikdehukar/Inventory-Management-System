export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  user_type: 'company_admin' | 'company_staff' | 'client';
  company?: number;
  company_name?: string;
  phone?: string;
  avatar?: string;
  is_verified: boolean;
  created_at: string;
}

export interface Company {
  id: number;
  name: string;
  description?: string;
  website?: string;
  email: string;
  phone?: string;
  address?: string;
  logo?: string;
  created_at: string;
  is_active: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  password_confirm: string;
  user_type: 'company_admin' | 'company_staff' | 'client';
  company?: number;
  phone?: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  message: string;
}