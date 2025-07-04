# Manufacturing System with Angular and Django: Complete Implementation Guide

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Design](#architecture-design)
3. [Backend Setup (Django)](#backend-setup-django)
4. [Frontend Setup (Angular)](#frontend-setup-angular)
5. [Core Features Implementation](#core-features-implementation)
6. [Advanced Features](#advanced-features)
7. [Deployment Strategy](#deployment-strategy)
8. [Security Considerations](#security-considerations)

## System Overview

A modern manufacturing system requires comprehensive management of:

### Core Modules
- **Production Planning & Control**
  - Master Production Scheduling (MPS)
  - Material Requirements Planning (MRP)
  - Capacity Planning
  - Work Order Management

- **Inventory Management**
  - Raw Materials Tracking
  - Work-in-Progress (WIP) Monitoring
  - Finished Goods Management
  - Stock Level Optimization

- **Quality Management**
  - In-process Quality Checks
  - Statistical Process Control (SPC)
  - Defect Tracking
  - Quality Reports

- **Asset & Maintenance Management**
  - Equipment Monitoring
  - Preventive Maintenance
  - Overall Equipment Effectiveness (OEE)
  - Spare Parts Management

- **Shop Floor Management**
  - Real-time Production Monitoring
  - Job Dispatching
  - Resource Allocation
  - Performance Analytics

## Architecture Design

### Backend Architecture (Django)
```
Manufacturing System Backend
│
├── Django Project Root
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   │
│   ├── apps/
│   │   ├── authentication/
│   │   ├── production/
│   │   ├── inventory/
│   │   ├── quality/
│   │   ├── maintenance/
│   │   ├── analytics/
│   │   └── common/
│   │
│   ├── api/
│   │   ├── v1/
│   │   └── v2/
│   │
│   └── utils/
│       ├── permissions.py
│       ├── pagination.py
│       └── mixins.py
```

### Frontend Architecture (Angular)
```
Manufacturing System Frontend
│
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── guards/
│   │   │   ├── interceptors/
│   │   │   └── services/
│   │   │
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   ├── pipes/
│   │   │   └── directives/
│   │   │
│   │   ├── features/
│   │   │   ├── production/
│   │   │   ├── inventory/
│   │   │   ├── quality/
│   │   │   ├── maintenance/
│   │   │   └── analytics/
│   │   │
│   │   └── layout/
│   │
│   ├── assets/
│   └── environments/
```

## Backend Setup (Django)

### 1. Project Initialization

```bash
# Create virtual environment
python -m venv manufacturing_env
source manufacturing_env/bin/activate  # On Windows: manufacturing_env\Scripts\activate

# Install dependencies
pip install django djangorestframework
pip install django-cors-headers
pip install djangorestframework-simplejwt
pip install celery redis
pip install psycopg2-binary  # For PostgreSQL
pip install django-filter
pip install drf-spectacular  # For API documentation

# Create Django project
django-admin startproject manufacturing_system
cd manufacturing_system
```

### 2. Core Models

#### Production Models
```python
# apps/production/models.py
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    unit_of_measure = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WorkOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    work_order_id = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.IntegerField(default=1)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class ProductionLine(models.Model):
    name = models.CharField(max_length=100)
    capacity_per_hour = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    maintenance_schedule = models.DateTimeField(null=True, blank=True)
```

#### Inventory Models
```python
# apps/inventory/models.py
from django.db import models
from apps.production.models import Product

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()

class Inventory(models.Model):
    STOCK_TYPE_CHOICES = [
        ('raw', 'Raw Material'),
        ('wip', 'Work in Progress'),
        ('finished', 'Finished Goods'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    stock_type = models.CharField(max_length=20, choices=STOCK_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    reserved_quantity = models.PositiveIntegerField(default=0)
    reorder_point = models.PositiveIntegerField()
    max_stock_level = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
    ]
    
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    reference_number = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
```

### 3. API Serializers

```python
# apps/production/serializers.py
from rest_framework import serializers
from .models import Product, WorkOrder, ProductionLine

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class WorkOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = WorkOrder
        fields = '__all__'
    
    def get_progress_percentage(self, obj):
        if obj.status == 'completed':
            return 100
        elif obj.status == 'in_progress':
            # Calculate based on time elapsed
            if obj.actual_start:
                from django.utils import timezone
                now = timezone.now()
                total_time = (obj.scheduled_end - obj.scheduled_start).total_seconds()
                elapsed_time = (now - obj.actual_start).total_seconds()
                return min(int((elapsed_time / total_time) * 100), 95)
        return 0

class ProductionLineSerializer(serializers.ModelSerializer):
    current_efficiency = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductionLine
        fields = '__all__'
    
    def get_current_efficiency(self, obj):
        # Calculate OEE (Overall Equipment Effectiveness)
        # This would integrate with real-time data
        return 85.5  # Placeholder
```

### 4. API Views

```python
# apps/production/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, WorkOrder, ProductionLine
from .serializers import ProductSerializer, WorkOrderSerializer, ProductionLineSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'sku']

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'product']
    
    @action(detail=True, methods=['post'])
    def start_production(self, request, pk=None):
        work_order = self.get_object()
        if work_order.status == 'pending':
            from django.utils import timezone
            work_order.status = 'in_progress'
            work_order.actual_start = timezone.now()
            work_order.save()
            return Response({'status': 'Production started'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def complete_production(self, request, pk=None):
        work_order = self.get_object()
        if work_order.status == 'in_progress':
            from django.utils import timezone
            work_order.status = 'completed'
            work_order.actual_end = timezone.now()
            work_order.save()
            return Response({'status': 'Production completed'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

class ProductionLineViewSet(viewsets.ModelViewSet):
    queryset = ProductionLine.objects.all()
    serializer_class = ProductionLineSerializer
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        total_lines = ProductionLine.objects.count()
        active_lines = ProductionLine.objects.filter(is_active=True).count()
        
        # Calculate average efficiency
        avg_efficiency = 82.3  # This would come from real-time calculations
        
        return Response({
            'total_lines': total_lines,
            'active_lines': active_lines,
            'avg_efficiency': avg_efficiency,
            'production_rate': '1,234 units/hour'
        })
```

### 5. Settings Configuration

```python
# settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    
    # Local apps
    'apps.authentication',
    'apps.production',
    'apps.inventory',
    'apps.quality',
    'apps.maintenance',
    'apps.analytics',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# JWT Configuration
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Angular development server
]

# Celery Configuration (for background tasks)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

## Frontend Setup (Angular)

### 1. Project Initialization

```bash
# Install Angular CLI
npm install -g @angular/cli

# Create Angular project
ng new manufacturing-frontend
cd manufacturing-frontend

# Install dependencies
npm install @angular/material @angular/cdk
npm install @angular/flex-layout
npm install chart.js ng2-charts
npm install @ngrx/store @ngrx/effects @ngrx/store-devtools
npm install rxjs
npm install date-fns
```

### 2. Core Services

#### Authentication Service
```typescript
// src/app/core/services/auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api';
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.loadUserProfile();
    }
  }

  login(username: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/auth/login/`, {
      username,
      password
    }).pipe(
      tap(response => {
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
        this.currentUserSubject.next(response.user);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.currentUserSubject.next(null);
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }

  private loadUserProfile(): void {
    this.http.get<User>(`${this.apiUrl}/auth/profile/`).subscribe(
      user => this.currentUserSubject.next(user)
    );
  }
}
```

#### Production Service
```typescript
// src/app/features/production/services/production.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Product {
  id: number;
  name: string;
  sku: string;
  description: string;
  unit_of_measure: string;
}

export interface WorkOrder {
  id: number;
  work_order_id: string;
  product: number;
  product_name: string;
  quantity: number;
  status: string;
  priority: number;
  scheduled_start: string;
  scheduled_end: string;
  actual_start?: string;
  actual_end?: string;
  progress_percentage: number;
}

export interface DashboardStats {
  total_lines: number;
  active_lines: number;
  avg_efficiency: number;
  production_rate: string;
}

@Injectable({
  providedIn: 'root'
})
export class ProductionService {
  private apiUrl = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {}

  // Products
  getProducts(params?: any): Observable<any> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key]) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get(`${this.apiUrl}/products/`, { params: httpParams });
  }

  createProduct(product: Partial<Product>): Observable<Product> {
    return this.http.post<Product>(`${this.apiUrl}/products/`, product);
  }

  updateProduct(id: number, product: Partial<Product>): Observable<Product> {
    return this.http.patch<Product>(`${this.apiUrl}/products/${id}/`, product);
  }

  deleteProduct(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/products/${id}/`);
  }

  // Work Orders
  getWorkOrders(filters?: any): Observable<any> {
    let httpParams = new HttpParams();
    if (filters) {
      Object.keys(filters).forEach(key => {
        if (filters[key]) {
          httpParams = httpParams.set(key, filters[key]);
        }
      });
    }
    return this.http.get(`${this.apiUrl}/work-orders/`, { params: httpParams });
  }

  createWorkOrder(workOrder: Partial<WorkOrder>): Observable<WorkOrder> {
    return this.http.post<WorkOrder>(`${this.apiUrl}/work-orders/`, workOrder);
  }

  startProduction(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/work-orders/${id}/start_production/`, {});
  }

  completeProduction(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/work-orders/${id}/complete_production/`, {});
  }

  // Dashboard
  getDashboardStats(): Observable<DashboardStats> {
    return this.http.get<DashboardStats>(`${this.apiUrl}/production-lines/dashboard_stats/`);
  }
}
```

### 3. Components

#### Dashboard Component
```typescript
// src/app/features/dashboard/dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { ProductionService, DashboardStats } from '../production/services/production.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  dashboardStats$: Observable<DashboardStats>;
  
  // Chart data
  productionChartData: any[] = [
    {
      name: 'Production',
      series: [
        { name: 'Jan', value: 8940 },
        { name: 'Feb', value: 8700 },
        { name: 'Mar', value: 9200 },
        { name: 'Apr', value: 9500 }
      ]
    }
  ];

  oeeChartData: any[] = [
    { name: 'Availability', value: 85 },
    { name: 'Performance', value: 92 },
    { name: 'Quality', value: 88 }
  ];

  constructor(private productionService: ProductionService) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.dashboardStats$ = this.productionService.getDashboardStats();
  }
}
```

#### Work Orders Component
```typescript
// src/app/features/production/components/work-orders/work-orders.component.ts
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatDialog } from '@angular/material/dialog';
import { ProductionService, WorkOrder } from '../../services/production.service';

@Component({
  selector: 'app-work-orders',
  templateUrl: './work-orders.component.html',
  styleUrls: ['./work-orders.component.scss']
})
export class WorkOrdersComponent implements OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  displayedColumns: string[] = [
    'work_order_id', 
    'product_name', 
    'quantity', 
    'status', 
    'priority',
    'scheduled_start',
    'progress_percentage',
    'actions'
  ];
  
  dataSource = new MatTableDataSource<WorkOrder>();
  loading = false;
  
  statusFilter = '';
  priorityFilter = '';

  constructor(
    private productionService: ProductionService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loadWorkOrders();
  }

  loadWorkOrders(): void {
    this.loading = true;
    const filters = {
      status: this.statusFilter || undefined,
      priority: this.priorityFilter || undefined
    };

    this.productionService.getWorkOrders(filters).subscribe({
      next: (response) => {
        this.dataSource.data = response.results;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading work orders:', error);
        this.loading = false;
      }
    });
  }

  startProduction(workOrder: WorkOrder): void {
    this.productionService.startProduction(workOrder.id).subscribe({
      next: () => {
        this.loadWorkOrders();
      },
      error: (error) => {
        console.error('Error starting production:', error);
      }
    });
  }

  completeProduction(workOrder: WorkOrder): void {
    this.productionService.completeProduction(workOrder.id).subscribe({
      next: () => {
        this.loadWorkOrders();
      },
      error: (error) => {
        console.error('Error completing production:', error);
      }
    });
  }

  getStatusColor(status: string): string {
    const colors = {
      'pending': 'warn',
      'in_progress': 'primary',
      'completed': 'accent',
      'cancelled': 'basic'
    };
    return colors[status] || 'basic';
  }

  applyFilter(): void {
    this.loadWorkOrders();
  }

  clearFilters(): void {
    this.statusFilter = '';
    this.priorityFilter = '';
    this.loadWorkOrders();
  }
}
```

### 4. State Management (NgRx)

```typescript
// src/app/store/production/production.actions.ts
import { createAction, props } from '@ngrx/store';
import { WorkOrder, Product } from '../../features/production/services/production.service';

export const loadWorkOrders = createAction(
  '[Production] Load Work Orders',
  props<{ filters?: any }>()
);

export const loadWorkOrdersSuccess = createAction(
  '[Production] Load Work Orders Success',
  props<{ workOrders: WorkOrder[]; totalCount: number }>()
);

export const loadWorkOrdersFailure = createAction(
  '[Production] Load Work Orders Failure',
  props<{ error: any }>()
);

export const startProduction = createAction(
  '[Production] Start Production',
  props<{ workOrderId: number }>()
);

export const startProductionSuccess = createAction(
  '[Production] Start Production Success',
  props<{ workOrderId: number }>()
);
```

## Core Features Implementation

### 1. Real-time Updates with WebSockets

```python
# Backend - Django Channels
# Install: pip install channels channels-redis

# settings.py
INSTALLED_APPS += ['channels']
ASGI_APPLICATION = 'manufacturing_system.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProductionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'production_updates'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def production_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'production_update',
            'data': event['data']
        }))
```

```typescript
// Frontend - Angular WebSocket Service
import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private socket: WebSocket;
  private messageSubject = new Subject<any>();
  public messages$ = this.messageSubject.asObservable();

  connect(): void {
    this.socket = new WebSocket('ws://localhost:8000/ws/production/');
    
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.messageSubject.next(data);
    };

    this.socket.onclose = () => {
      console.log('WebSocket connection closed');
      // Implement reconnection logic
      setTimeout(() => this.connect(), 5000);
    };
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.close();
    }
  }
}
```

### 2. Advanced Analytics Dashboard

```typescript
// src/app/features/analytics/components/oee-dashboard/oee-dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { AnalyticsService } from '../../services/analytics.service';

@Component({
  selector: 'app-oee-dashboard',
  template: `
    <div class="oee-dashboard">
      <mat-card class="oee-summary">
        <mat-card-header>
          <mat-card-title>Overall Equipment Effectiveness (OEE)</mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <div class="oee-metrics">
            <div class="metric">
              <h3>{{ oeeData.availability }}%</h3>
              <p>Availability</p>
            </div>
            <div class="metric">
              <h3>{{ oeeData.performance }}%</h3>
              <p>Performance</p>
            </div>
            <div class="metric">
              <h3>{{ oeeData.quality }}%</h3>
              <p>Quality</p>
            </div>
            <div class="metric overall">
              <h3>{{ oeeData.overall }}%</h3>
              <p>Overall OEE</p>
            </div>
          </div>
        </mat-card-content>
      </mat-card>

      <mat-card class="trend-chart">
        <mat-card-header>
          <mat-card-title>OEE Trend</mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <ngx-charts-line-chart
            [results]="oeeHistoryData"
            [xAxis]="true"
            [yAxis]="true"
            [showXAxisLabel]="true"
            [showYAxisLabel]="true"
            xAxisLabel="Time"
            yAxisLabel="OEE %">
          </ngx-charts-line-chart>
        </mat-card-content>
      </mat-card>
    </div>
  `
})
export class OeeDashboardComponent implements OnInit {
  oeeData = {
    availability: 85.2,
    performance: 92.1,
    quality: 88.7,
    overall: 69.5
  };

  oeeHistoryData: any[] = [];

  constructor(private analyticsService: AnalyticsService) {}

  ngOnInit(): void {
    this.loadOeeData();
  }

  loadOeeData(): void {
    this.analyticsService.getOeeHistory().subscribe(data => {
      this.oeeHistoryData = data;
    });
  }
}
```

### 3. Mobile-Responsive Design

```scss
// src/app/shared/styles/responsive.scss
@mixin mobile-only {
  @media (max-width: 767px) {
    @content;
  }
}

@mixin tablet-only {
  @media (min-width: 768px) and (max-width: 1023px) {
    @content;
  }
}

@mixin desktop-only {
  @media (min-width: 1024px) {
    @content;
  }
}

.dashboard-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));

  @include mobile-only {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  @include tablet-only {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

## Advanced Features

### 1. Predictive Maintenance with AI Integration

```python
# Backend - AI Integration
from rest_framework.decorators import api_view
from rest_framework.response import Response
import joblib
import numpy as np

@api_view(['POST'])
def predict_maintenance(request):
    """
    Predict equipment maintenance needs using ML model
    """
    # Load pre-trained model
    model = joblib.load('models/maintenance_predictor.pkl')
    
    # Extract features from request
    features = np.array([
        request.data.get('temperature'),
        request.data.get('vibration'),
        request.data.get('pressure'),
        request.data.get('running_hours')
    ]).reshape(1, -1)
    
    # Make prediction
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0].max()
    
    return Response({
        'maintenance_needed': bool(prediction),
        'confidence': float(probability),
        'recommended_action': 'Schedule maintenance within 7 days' if prediction else 'Continue normal operation'
    })
```

### 2. QR Code Integration for Work Orders

```typescript
// src/app/features/production/components/qr-scanner/qr-scanner.component.ts
import { Component, OnInit } from '@angular/core';
import { BarcodeScanner } from '@ionic-native/barcode-scanner/ngx';

@Component({
  selector: 'app-qr-scanner',
  template: `
    <div class="scanner-container">
      <button mat-raised-button color="primary" (click)="scanQRCode()">
        <mat-icon>qr_code_scanner</mat-icon>
        Scan Work Order QR Code
      </button>
      
      <div class="manual-entry">
        <mat-form-field>
          <mat-label>Work Order ID</mat-label>
          <input matInput [(ngModel)]="manualWorkOrderId">
        </mat-form-field>
        <button mat-button (click)="loadWorkOrder()">Load</button>
      </div>
    </div>
  `
})
export class QrScannerComponent {
  manualWorkOrderId = '';

  constructor(
    private barcodeScanner: BarcodeScanner,
    private productionService: ProductionService
  ) {}

  async scanQRCode(): Promise<void> {
    try {
      const result = await this.barcodeScanner.scan();
      if (result.text) {
        this.loadWorkOrderById(result.text);
      }
    } catch (error) {
      console.error('Error scanning QR code:', error);
    }
  }

  loadWorkOrder(): void {
    if (this.manualWorkOrderId) {
      this.loadWorkOrderById(this.manualWorkOrderId);
    }
  }

  private loadWorkOrderById(workOrderId: string): void {
    this.productionService.getWorkOrderByBarcode(workOrderId).subscribe({
      next: (workOrder) => {
        // Navigate to work order details or update status
        console.log('Work order loaded:', workOrder);
      },
      error: (error) => {
        console.error('Work order not found:', error);
      }
    });
  }
}
```

## Deployment Strategy

### 1. Docker Configuration

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "manufacturing_system.wsgi:application"]
```

```dockerfile
# Frontend Dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build --prod

FROM nginx:alpine
COPY --from=build /app/dist/manufacturing-frontend /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

### 2. Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: manufacturing_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/manufacturing_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  celery:
    build: ./backend
    command: celery -A manufacturing_system worker -l info
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/manufacturing_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
  redis_data:
```

## Security Considerations

### 1. Authentication & Authorization

```python
# Backend - Role-based permissions
from rest_framework.permissions import BasePermission

class IsProductionManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='production_managers').exists()

class IsQualityInspector(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='quality_inspectors').exists()

# Apply to views
class WorkOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProductionManager]
```

### 2. Data Encryption

```python
# Backend - Field-level encryption
from django_cryptography.fields import encrypt

class SensitiveProductData(models.Model):
    formula = encrypt(models.TextField())  # Encrypted field
    cost_data = encrypt(models.JSONField())  # Encrypted JSON
```

### 3. API Rate Limiting

```python
# Backend - Throttling
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

This comprehensive guide provides a solid foundation for building a modern manufacturing system with Angular and Django. The architecture is scalable, secure, and follows industry best practices for both frontend and backend development.

Key benefits of this approach:
- **Modular Architecture**: Easy to extend and maintain
- **Real-time Updates**: WebSocket integration for live data
- **Mobile-Responsive**: Works across all devices
- **Security-First**: Role-based access and data encryption
- **Scalable**: Microservices-ready with Docker
- **AI-Ready**: Integration points for machine learning
- **Industry 4.0 Compliant**: Modern manufacturing standards

The system can be extended with additional modules like:
- Advanced analytics and reporting
- Integration with IoT devices
- Supply chain management
- Customer relationship management
- Financial management
- Compliance and audit trails