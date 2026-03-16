# 🏗️ Valet Parking System - Architecture Diagrams

This folder contains comprehensive architecture diagrams for the Valet Parking Reservation System using **Eraser Diagram** syntax.

## 📊 Diagram Files

### 1. **diagram.eraserdiagram** - System Architecture
**Type**: Cloud Architecture Diagram  
**Purpose**: High-level overview of all system components and their relationships

**Shows**:
- 8 major layers (Presentation, Service, Core, Models, Storage, Infrastructure, External)
- All components with their responsibilities
- Data flow between components
- Color-coded by layer for easy understanding
- Future integration points (SMS, Payment, Email, Cloud Storage)

**Key Highlights**:
- ✅ Clean separation of concerns
- ✅ Repository pattern for data abstraction
- ✅ Dependency injection for testability
- ✅ Comprehensive error handling
- ✅ Extensible for future features

---

### 2. **sequence_flow.eraserdiagram** - Reservation Lifecycle
**Type**: Sequence Diagram  
**Purpose**: Shows the complete flow of creating and closing a reservation

**Flows Covered**:
1. **Create Reservation** - Customer check-in process
2. **Parking Period** - Duration calculation
3. **Update Damage** - Vehicle damage reporting
4. **Close Reservation** - Customer checkout process
5. **Error Scenarios** - Common failure cases

**Key Interactions**:
- Customer ↔ Valet Staff ↔ System
- Validation steps
- QR code generation
- Time calculations
- Error handling

---

### 3. **data_model.eraserdiagram** - Entity Relationships
**Type**: Entity Relationship Diagram  
**Purpose**: Database schema and entity relationships

**Entities**:
- **Customer** (mobile_number, full_name)
- **Vehicle** (license_plate, damage_report, key_scan_data)
- **Reservation** (UUID, timestamps, QR, status, duration)
- **ReservationStatus** (ACTIVE, COMPLETED, CANCELLED)

**Relationships**:
- Reservation → Customer (1:1)
- Reservation → Vehicle (1:1)  
- Reservation → ReservationStatus (1:1)

**Additional Info**:
- Validation rules documented
- Entity lifecycle explained
- Query patterns and complexity
- Future database indexes

---

### 4. **class_structure.eraserdiagram** - Component Dependencies
**Type**: Cloud Architecture Diagram  
**Purpose**: Detailed class structure and dependency graph

**Package Structure**:
- `models/` - Pydantic data models
- `core/` - Business logic (QR, Time, Service)
- `storage/` - Repository pattern implementation
- `utils/` - Validators and formatters
- `exceptions.py` - Custom error types
- `config.py` - Configuration management

**Design Patterns**:
- ✅ Repository Pattern
- ✅ Dependency Injection
- ✅ Strategy Pattern
- ✅ Factory Method
- ✅ Data Transfer Object

**SOLID Principles**:
- ✅ Single Responsibility
- ✅ Open/Closed
- ✅ Liskov Substitution
- ✅ Interface Segregation
- ✅ Dependency Inversion

---

## 🎨 How to View the Diagrams

### Option 1: VS Code with Eraser Extension (Recommended)

1. **Install Eraser Extension**:
   - Open VS Code
   - Go to Extensions (Cmd+Shift+X / Ctrl+Shift+X)
   - Search for "Eraser"
   - Install "Eraser Diagram" extension

2. **View Diagrams**:
   - Open any `.eraserdiagram` file
   - The diagram will render automatically
   - Use zoom and pan controls

3. **Edit Diagrams**:
   - Edit the text file directly
   - The diagram updates in real-time
   - Full syntax highlighting

### Option 2: Eraser.io Web Platform

1. Go to [eraser.io](https://www.eraser.io/)
2. Create a free account
3. Create new diagram
4. Copy/paste the content from any `.eraserdiagram` file
5. View and edit online

### Option 3: Export to Other Formats

Using eraser.io, you can export to:
- PNG image
- SVG vector
- PDF document
- Markdown (with embedded images)

---

## 🔍 Quick Reference

### Diagram Syntax Elements

```
// Comments
Component [icon: icon-name, color: blue]
Group Name { nested components }
Component1 > Component2: Label
note Description text
group Section Name [color: blue] { ... }
```

### Common Icons Used

- `server` - Services and APIs
- `database` - Storage and repositories
- `shield` - Validation and security
- `clock` - Time calculations
- `qrcode` - QR code operations
- `user` - Customer/user entities
- `car` - Vehicle entities
- `file-text` - Documents and logs
- `settings` - Configuration
- `alert-triangle` - Errors and exceptions

### Color Coding

- **Blue** - Presentation/Client layer
- **Green** - Service layer
- **Orange** - Core business logic
- **Purple** - Data models
- **Cyan** - Storage layer
- **Red** - Infrastructure/Errors
- **Yellow** - External services (future)
- **Gray** - Optional/Future features

---

## 📚 Understanding the Architecture

### Layer Breakdown

```
┌─────────────────────────────────────┐
│  Client Applications (Web/Mobile)   │
├─────────────────────────────────────┤
│  ReservationService (API/Service)   │
├─────────────────────────────────────┤
│  Core Components (QR, Time, Valid)  │
├─────────────────────────────────────┤
│  Data Models (Pydantic)             │
├─────────────────────────────────────┤
│  Storage (Repository Pattern)       │
├─────────────────────────────────────┤
│  Infrastructure (Config, Logging)   │
└─────────────────────────────────────┘
```

### Data Flow Example

```
1. Client Request
   ↓
2. ReservationService.create_reservation()
   ↓
3. Validators.validate_phone_number()
   ↓
4. QRGenerator.generate_qr_data()
   ↓
5. Models: Customer + Vehicle + Reservation
   ↓
6. Repository.save()
   ↓
7. Response with QR code
```

---

## 🛠️ Extending the Architecture

### Adding a REST API

```python
# Add FastAPI layer
from fastapi import FastAPI, HTTPException
from valet_parking import ReservationService

app = FastAPI()

@app.post("/reservations")
def create_reservation(data: dict):
    return service.create_reservation(**data)
```

### Adding Database Persistence

```python
# Implement Repository for PostgreSQL
class PostgresReservationRepository:
    def save(self, reservation):
        # SQL INSERT logic
        pass
    
    def find_by_id(self, uuid):
        # SQL SELECT logic
        pass
```

### Adding Real-time Notifications

```python
# Add to ReservationService
def create_reservation(self, ...):
    reservation = # ... create reservation
    self.notification_service.send_sms(
        reservation.customer.mobile_number,
        f"Reservation confirmed: {reservation.reservation_id}"
    )
    return reservation
```

---

## 📖 Related Documentation

- **Main README**: `../../README.md` - Installation and usage
- **Testing Guide**: `../../TESTING_GUIDE.md` - How to run tests
- **Implementation Plan**: `../out_doc/valet_parking_reservation_plan.md`
- **JSON Spec**: `../out_doc/valet_parking_reservation_plan.json`

---

## 🎯 Architecture Principles

### 1. **Separation of Concerns**
Each layer has a distinct responsibility and doesn't mix concerns.

### 2. **Loose Coupling**
Components depend on abstractions (Protocols) not implementations.

### 3. **High Cohesion**
Related functionality is grouped together in the same module.

### 4. **Testability**
Dependency injection makes all components easily testable.

### 5. **Extensibility**
Repository pattern allows easy addition of new storage backends.

### 6. **Type Safety**
Full type hints throughout for better IDE support and error detection.

---

## 🚀 Next Steps

1. **View the diagrams** using Eraser extension
2. **Understand the flow** using sequence diagram
3. **Review data model** in entity diagram
4. **Explore class structure** in component diagram
5. **Implement extensions** following the patterns shown

---

## 💡 Tips for Diagram Maintenance

- Update diagrams when adding new features
- Keep comments up to date
- Use consistent color coding
- Document design decisions in comments
- Export to PNG for presentations
- Version control the `.eraserdiagram` files

---

**Created**: March 16, 2026  
**System**: Valet Parking Reservation System  
**Architecture Style**: Clean Architecture with Layers
