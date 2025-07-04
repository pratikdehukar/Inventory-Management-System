# Manufacturing System - Django + Angular

A comprehensive manufacturing management system built with Django REST Framework backend and Angular frontend.

## 🎯 Project Overview

This manufacturing system provides complete management capabilities for:
- **Production Management**: Work orders, production lines, scheduling
- **Inventory Management**: Stock tracking, warehouse management, movements
- **Quality Management**: Quality control and assurance (planned)
- **Maintenance Management**: Equipment maintenance scheduling (planned)

## 🚀 Quick Start

### Backend (Django) - ✅ COMPLETED

The Django backend is fully set up and operational!

#### ✅ What's Been Implemented

1. **Project Structure**
   - Django 5.1.5 with REST Framework
   - PostgreSQL-ready configuration (currently using SQLite for development)
   - JWT authentication setup
   - CORS configured for Angular integration
   - Celery & Redis configuration for background tasks
   - WebSocket support with Django Channels

2. **Core Models Created**
   - **Production Models**: Product, ProductionLine, WorkOrder, BillOfMaterials, ProductionReport
   - **Inventory Models**: Warehouse, Inventory, StockMovement
   - All models include comprehensive business logic and properties

3. **Features Available**
   - Complete ORM models with relationships
   - Admin interface ready
   - API documentation with drf-spectacular
   - JWT token-based authentication
   - CORS headers for frontend integration

#### 🎮 Available Commands

```bash
# Navigate to backend
cd backend

# Activate virtual environment
source venv/bin/activate

# Run development server
python manage.py runserver

# Access admin interface at http://127.0.0.1:8000/admin/
# Username: admin
# Password: admin123
```

### Frontend (Angular) - 🚧 NEXT STEPS

The Angular frontend needs to be created. Follow these steps:

1. **Navigate to frontend directory and create Angular app**
2. **Install required packages (Angular Material, JWT)**
3. **Create authentication service**
4. **Build dashboard and management interfaces**

## 📊 Current Status

✅ **Backend Foundation Complete**
- Django project configured
- Database models created
- Migrations applied
- Admin user created
- Development server ready

🚧 **Next: Frontend Development**
- Angular project setup needed
- Component creation
- API integration
- Real-time features

## 💡 Key Features

### Production Management
- Product catalog with SKUs and BOMs
- Production line capacity tracking
- Work order management with scheduling
- Real-time progress monitoring
- OEE (Overall Equipment Effectiveness) calculation

### Inventory Management
- Multi-warehouse support
- Stock level tracking by type (raw/WIP/finished)
- Automated reorder point alerts
- Complete stock movement audit trail

---

**Ready to start building the frontend!** 🚀
