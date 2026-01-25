# Parent-Student Assignment API

## New Features Added

### 1. **student_id Field in Parents Table**
- Added `student_id` column to parents table with foreign key reference to students table
- Field is nullable and supports CASCADE updates and SET NULL on delete

### 2. **Updated Parent Models**
- `ParentBase`: Added `student_id: Optional[str] = None`
- `ParentUpdate`: Added `student_id: Optional[str] = None`  
- `ParentResponse`: Inherits `student_id` from `ParentBase`

### 3. **Updated Parent Creation**
- `POST /api/v1/parents` now accepts `student_id` in request body
- Can create parent with student assignment in single request

### 4. **New API Endpoint**
```
PUT /api/v1/parents/{parent_id}/assign-student
```
**Purpose**: Assign a student to an existing parent

**Request Body**:
```json
{
  "student_id": "uuid-string"
}
```

**Response**: Updated parent object with assigned student_id

### 5. **Updated Parent Update**
- `PUT /api/v1/parents/{parent_id}` now supports updating `student_id`

## API Usage Examples

### Create Parent with Student Assignment
```bash
curl -X POST "http://127.0.0.1:8080/api/v1/parents" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": 9123456789,
    "name": "Parent Name",
    "password": "parent123",
    "parent_role": "MOTHER",
    "city": "Mumbai",
    "student_id": "student-uuid-here"
  }'
```

### Assign Student to Existing Parent
```bash
curl -X PUT "http://127.0.0.1:8080/api/v1/parents/{parent_id}/assign-student" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "student-uuid-here"
  }'
```

### Update Parent with Student Assignment
```bash
curl -X PUT "http://127.0.0.1:8080/api/v1/parents/{parent_id}" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Delhi",
    "student_id": "student-uuid-here"
  }'
```

## Response Format
All parent responses now include the `student_id` field:

```json
{
  "parent_id": "uuid",
  "phone": 9123456789,
  "name": "Parent Name",
  "student_id": "student-uuid-or-null",
  "status": "ACTIVE",
  "created_at": "2026-01-25T15:30:00",
  "updated_at": "2026-01-25T15:30:00"
}
```

## Database Constraints
- Foreign key constraint ensures `student_id` references valid student
- ON DELETE SET NULL: If student is deleted, parent's student_id becomes NULL
- ON UPDATE CASCADE: If student_id changes, parent's reference updates automatically

✅ **All functionality tested and working correctly!**