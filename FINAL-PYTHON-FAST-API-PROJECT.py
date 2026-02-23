from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from abc import ABC, abstractmethod
import uvicorn

class BusResponse(BaseModel):
    bus_id: int
    route: str
    time: str
    fare: int
    seats_available: int

class BookingRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    bus_id: int = Field(..., gt=0)
    seats: int = Field(..., gt=0, le=30)

class BookingResponse(BaseModel):
    booking_id: str
    name: str
    bus_id: int
    route: str
    time: str
    seats: int
    total_fare: int
    booking_time: str

class CancelRequest(BaseModel):
    name: str = Field(..., min_length=1)

# === ABSTRACT BASE CLASS (Abstraction) ===
class BookingSystem(ABC):
    """Abstract base class defining the contract for booking systems"""
    
    @abstractmethod
    def create_booking(self, booking_data: BookingRequest) -> BookingResponse:
        pass
    
    @abstractmethod
    def cancel_booking(self, name: str) -> bool:
        pass
    
    @abstractmethod
    def get_all_bookings(self) -> List[BookingResponse]:
        pass

# === BUS CLASS (Encapsulation) ===
class Bus:
    """Encapsulates bus information and operations"""
    
    def __init__(self, bus_id: int, route: str, time: str, fare: int, total_seats: int = 30):
        self._bus_id = bus_id  # Private attribute
        self._route = route
        self._time = time
        self._fare = fare
        self._total_seats = total_seats
        self._available_seats = total_seats
    
    # Getter methods (Encapsulation)
    @property
    def bus_id(self) -> int:
        return self._bus_id
    
    @property
    def route(self) -> str:
        return self._route
    
    @property
    def time(self) -> str:
        return self._time
    
    @property
    def fare(self) -> int:
        return self._fare
    
    @property
    def available_seats(self) -> int:
        return self._available_seats
    
    def reserve_seats(self, seats: int) -> bool:
        """Reserve seats if available"""
        if seats <= self._available_seats:
            self._available_seats -= seats
            return True
        return False
    
    def release_seats(self, seats: int) -> None:
        """Release reserved seats"""
        self._available_seats = min(self._available_seats + seats, self._total_seats)
    
    def to_response(self) -> BusResponse:
        """Convert to response model"""
        return BusResponse(
            bus_id=self._bus_id,
            route=self._route,
            time=self._time,
            fare=self._fare,
            seats_available=self._available_seats
        )

# === BOOKING CLASS (Encapsulation) ===
class Booking:
    """Encapsulates booking information"""
    
    def __init__(self, name: str, bus: Bus, seats: int):
        self._booking_id = f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self._name = name
        self._bus = bus
        self._seats = seats
        self._total_fare = seats * bus.fare
        self._booking_time = datetime.now().isoformat()
    
    @property
    def booking_id(self) -> str:
        return self._booking_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def bus(self) -> Bus:
        return self._bus
    
    @property
    def seats(self) -> int:
        return self._seats
    
    @property
    def total_fare(self) -> int:
        return self._total_fare
    
    def to_response(self) -> BookingResponse:
        """Convert to response model"""
        return BookingResponse(
            booking_id=self._booking_id,
            name=self._name,
            bus_id=self._bus.bus_id,
            route=self._bus.route,
            time=self._bus.time,
            seats=self._seats,
            total_fare=self._total_fare,
            booking_time=self._booking_time
        )

# === CONCRETE IMPLEMENTATION (Inheritance) ===
class BusBookingSystem(BookingSystem):
    """Concrete implementation of BookingSystem"""
    
    def __init__(self):
        # Initialize buses (Data Storage)
        self._buses: Dict[int, Bus] = {
            1: Bus(1, "North Nazimabad - Power House", "09:00 AM", 500),
            2: Bus(2, "KDA - Gulshan", "12:00 PM", 700),
            3: Bus(3, "Ayesha Manzil - Bahria", "05:00 PM", 600)
        }
        self._bookings: List[Booking] = []
    
    def get_all_buses(self) -> List[BusResponse]:
        """Get all available buses"""
        return [bus.to_response() for bus in self._buses.values()]
    
    def get_bus(self, bus_id: int) -> Optional[Bus]:
        """Get bus by ID"""
        return self._buses.get(bus_id)
    
    def create_booking(self, booking_data: BookingRequest) -> BookingResponse:
        """Create a new booking"""
        bus = self.get_bus(booking_data.bus_id)
        
        if not bus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bus not found"
            )
        
        if not bus.reserve_seats(booking_data.seats):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough seats available"
            )
        
        booking = Booking(booking_data.name, bus, booking_data.seats)
        self._bookings.append(booking)
        
        return booking.to_response()
    
    def cancel_booking(self, name: str) -> bool:
        """Cancel booking by name"""
        for i, booking in enumerate(self._bookings):
            if booking.name.lower() == name.lower():
                # Release seats back to bus
                booking.bus.release_seats(booking.seats)
                # Remove booking
                del self._bookings[i]
                return True
        return False
    
    def get_all_bookings(self) -> List[BookingResponse]:
        """Get all bookings"""
        return [booking.to_response() for booking in self._bookings]

# === DECORATOR WRAPPER FUNCTIONS ===
def error_handler(func):
    """Decorator for consistent error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
    return wrapper

def log_operation(operation: str):
    """Decorator for logging operations"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[{datetime.now()}] {operation} operation started")
            result = func(*args, **kwargs)
            print(f"[{datetime.now()}] {operation} operation completed")
            return result
        return wrapper
    return decorator

# === FASTAPI APPLICATION ===
app = FastAPI(
    title="Bus Booking System API",
    description="A comprehensive bus ticket booking system with OOP principles",
    version="1.0.0"
)

# Initialize booking system (Dependency Injection)
booking_system = BusBookingSystem()

# === API ENDPOINTS ===

@app.get("/", summary="Welcome endpoint")
def read_root():
    """Welcome message"""
    return {
        "message": "Welcome to Bus Booking System API",
        "endpoints": {
            "GET /buses": "View all buses",
            "POST /bookings": "Book a ticket",
            "DELETE /bookings": "Cancel booking",
            "GET /bookings": "View all bookings"
        }
    }

@app.get("/buses", response_model=List[BusResponse], summary="Get all buses")
@error_handler
@log_operation("VIEW_BUSES")
def get_buses():
    """Get all available buses with their schedules"""
    return booking_system.get_all_buses()

@app.post("/bookings", response_model=BookingResponse, summary="Book a ticket")
@error_handler
@log_operation("BOOK_TICKET")
def book_ticket(booking_request: BookingRequest):
    """Book a bus ticket"""
    return booking_system.create_booking(booking_request)

@app.delete("/bookings", summary="Cancel booking")
@error_handler
@log_operation("CANCEL_BOOKING")
def cancel_booking(cancel_request: CancelRequest):
    """Cancel a booking by passenger name"""
    if booking_system.cancel_booking(cancel_request.name):
        return {"message": "Booking cancelled successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

@app.get("/bookings", response_model=List[BookingResponse], summary="Get all bookings")
@error_handler
@log_operation("VIEW_BOOKINGS")
def get_bookings():
    """Get all current bookings"""
    return booking_system.get_all_bookings()

# === APPLICATION RUNNER ===
if __name__ == "__main__":
    print(" Starting Bus Booking System API...")
    print(" Available endpoints:")
    print("  • GET  /buses     - View bus schedules")
    print("  • POST /bookings  - Book tickets")
    print("  • GET  /bookings  - View bookings")
    print("  • DELETE /bookings - Cancel bookings")
    print("\n🌐 Access API docs at: http://localhost:8000/docs")
    

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
