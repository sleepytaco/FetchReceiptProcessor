"""
This file contains blueprints to build Receipt and Item objects. It also contains a method to compute points for
a given receipt object.
"""

import math
from datetime import datetime
from pydantic import BaseModel
from typing import List


class Item(BaseModel):
    shortDescription: str
    price: float


class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    total: float
    items: List[Item]


def calculate_points(receipt: Receipt) -> int:
    points = 0

    # One point for every alphanumeric character in the retailer name
    for c in receipt.retailer:
        if c.isalnum():
            points += 1

    # 50 points if the total is a round dollar amount with no cents
    if receipt.total == int(receipt.total):
        points += 50

    # 25 points if the total is a multiple of 0.25
    if receipt.total % 0.25 == 0:
        points += 25

    # 5 points for every two items on the receipt
    points += (len(receipt.items) // 2) * 5

    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the
    # nearest integer. The result is the number of points earned
    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            points += math.ceil(item.price * 0.2)

    # 6 points if the day in the purchase date is odd
    purchase_date = datetime.strptime(receipt.purchaseDate, '%Y-%m-%d')
    if purchase_date.day % 2 != 0:
        points += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(receipt.purchaseTime, '%H:%M')
    if datetime.strptime('14:00', '%H:%M').time() < purchase_time.time() < datetime.strptime('16:00', '%H:%M').time():
        points += 10

    return points
