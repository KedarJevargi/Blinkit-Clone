import random

def generate_otp():
  """Generates a random 6-digit OTP."""
  return random.randint(100000, 999999)