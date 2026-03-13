from products.models import Product

cars = [
    {
        "name": "Toyota Corolla",
        "description": "Reliable compact sedan",
        "price": 22000.00,
        "stock": 12,
    },
    {
        "name": "Honda Civic",
        "description": "Fuel efficient compact car",
        "price": 23000.00,
        "stock": 10,
    },
    {
        "name": "Ford Mustang",
        "description": "Classic American sports car",
        "price": 45000.00,
        "stock": 5,
    },
    {
        "name": "Chevrolet Camaro",
        "description": "High performance muscle car",
        "price": 43000.00,
        "stock": 6,
    },
    {
        "name": "Tesla Model 3",
        "description": "Electric sedan with autopilot",
        "price": 52000.00,
        "stock": 8,
    },
    {
        "name": "BMW 3 Series",
        "description": "Luxury compact sedan",
        "price": 48000.00,
        "stock": 7,
    },
    {
        "name": "Audi A4",
        "description": "Premium German sedan",
        "price": 47000.00,
        "stock": 9,
    },
    {
        "name": "Mercedes-Benz C-Class",
        "description": "Luxury midsize sedan",
        "price": 50000.00,
        "stock": 6,
    },
    {
        "name": "Hyundai Elantra",
        "description": "Affordable compact sedan",
        "price": 21000.00,
        "stock": 14,
    },
    {
        "name": "Kia Sportage",
        "description": "Compact SUV with modern features",
        "price": 28000.00,
        "stock": 11,
    },
    {
        "name": "Toyota RAV4",
        "description": "Popular compact SUV",
        "price": 30000.00,
        "stock": 13,
    },
    {
        "name": "Honda CR-V",
        "description": "Reliable family SUV",
        "price": 31000.00,
        "stock": 12,
    },
    {
        "name": "Nissan Altima",
        "description": "Comfortable midsize sedan",
        "price": 26000.00,
        "stock": 10,
    },
    {
        "name": "Subaru Outback",
        "description": "All-wheel-drive adventure wagon",
        "price": 34000.00,
        "stock": 8,
    },
    {
        "name": "Volkswagen Golf",
        "description": "Compact hatchback",
        "price": 24000.00,
        "stock": 9,
    },
    {
        "name": "Mazda CX-5",
        "description": "Stylish compact SUV",
        "price": 29000.00,
        "stock": 10,
    },
    {
        "name": "Jeep Wrangler",
        "description": "Off-road capable SUV",
        "price": 42000.00,
        "stock": 5,
    },
    {
        "name": "Land Rover Defender",
        "description": "Luxury off-road SUV",
        "price": 70000.00,
        "stock": 3,
    },
    {
        "name": "Porsche 911",
        "description": "Legendary sports car",
        "price": 120000.00,
        "stock": 2,
    },
    {
        "name": "Lamborghini Huracan",
        "description": "Exotic Italian supercar",
        "price": 250000.00,
        "stock": 1,
    },
    {
        "name": "Ferrari F8 Tributo",
        "description": "High performance Ferrari supercar",
        "price": 280000.00,
        "stock": 1,
    },
    {
        "name": "Toyota Hilux",
        "description": "Durable pickup truck",
        "price": 35000.00,
        "stock": 15,
    },
    {
        "name": "Ford Ranger",
        "description": "Mid-size pickup truck",
        "price": 33000.00,
        "stock": 14,
    },
    {
        "name": "Chevrolet Silverado",
        "description": "Full-size pickup truck",
        "price": 40000.00,
        "stock": 12,
    },
    {
        "name": "Ram 1500",
        "description": "Powerful American pickup truck",
        "price": 41000.00,
        "stock": 11,
    },
    {
        "name": "Tesla Model S",
        "description": "Luxury electric sedan",
        "price": 90000.00,
        "stock": 4,
    },
    {
        "name": "Tesla Model X",
        "description": "Electric SUV with falcon doors",
        "price": 98000.00,
        "stock": 3,
    },
    {
        "name": "Toyota Land Cruiser",
        "description": "Legendary off-road SUV",
        "price": 85000.00,
        "stock": 4,
    },
    {
        "name": "Honda Accord",
        "description": "Reliable midsize sedan",
        "price": 27000.00,
        "stock": 10,
    },
    {
        "name": "BMW X5",
        "description": "Luxury midsize SUV",
        "price": 65000.00,
        "stock": 6,
    },
]

for car in cars:
    Product.objects.create(**car)

print("30 cars created successfully")
