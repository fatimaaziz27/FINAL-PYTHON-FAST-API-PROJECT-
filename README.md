## Bus Booking System API

A comprehensive Bus Ticket Booking System API built with FastAPI, demonstrating advanced OOP principles such as abstraction, encapsulation, and inheritance, along with decorators for logging and error handling.
This API allows users to view buses, book tickets, cancel bookings, and track all bookings.

## Project Structure

main.py – Main FastAPI application file with all endpoints and OOP implementation

requirements.txt – Python dependencies (FastAPI, Uvicorn, Pydantic)

README.md – Project documentation

## Features

View all available buses with routes, timing, fares, and seat availability

Book tickets for specific buses with seat validation

Cancel bookings by passenger name

Track all current bookings

## Built using OOP principles:

Abstraction – via abstract booking system class

Encapsulation – bus and booking classes with private attributes

Inheritance – concrete booking system implementation

Logging operations for actions like booking, canceling, and viewing

## Error handling with custom responses

## Install required packages
pip install fastapi uvicorn pydantic

## API Endpoints

| **Method** | **Endpoint** | **Description** |
|------------|--------------|-----------------|
| **GET**    | `/`          | Welcome endpoint with available endpoints |
| **GET**    | `/buses`     | View all available buses with details |
| **POST**   | `/bookings`  | Book a bus ticket |
| **GET**    | `/bookings`  | Get all current bookings |
| **DELETE** | `/bookings`  | Cancel a booking by passenger name |


## POST /bookings

{
  "name": "Fatima Aziz",
  "bus_id": 1,
  "seats": 2
}


## Response:

{
  "booking_id": "BK20251109153000",
  "name": "Fatima Aziz",
  "bus_id": 1,
  "route": "North Nazimabad - Power House",
  "time": "09:00 AM",
  "seats": 2,
  "total_fare": 1000,
  "booking_time": "2025-11-09T15:30:00.000000"
}

## Built With

Python 3.9+

FastAPI – API framework

Uvicorn – ASGI server

Pydantic – Data validation and serialization

## Project Members

Fatima Aziz

Hadiya Ahmed

Ayesha Aziz

 ## Future Enhancements

Add database integration (SQLite/PostgreSQL) for persistent storage

Add authentication and user roles

Create a frontend interface using React/Vue.js

Email confirmation for bookings

Add seat selection map for buses
