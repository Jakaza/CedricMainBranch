#!/usr/bin/env python
"""
Script to check if Yoco is in test or production mode
"""
import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(BASE_DIR / '.env')

# Get Yoco keys
secret_key = os.environ.get('YOCO_SECRET_KEY', '')
public_key = os.environ.get('YOCO_PUBLIC_KEY', '')

print("=" * 60)
print("YOCO PAYMENT MODE CHECK")
print("=" * 60)

if not secret_key or not public_key:
    print("❌ ERROR: Yoco keys not found in .env file!")
    print("\nPlease ensure your .env file contains:")
    print("  YOCO_SECRET_KEY=your_key_here")
    print("  YOCO_PUBLIC_KEY=your_key_here")
else:
    # Check if keys are test or production
    is_test_secret = secret_key.startswith('sk_test_')
    is_test_public = public_key.startswith('pk_test_')
    is_prod_secret = secret_key.startswith('sk_live_')
    is_prod_public = public_key.startswith('pk_live_')
    
    print(f"\n📋 Secret Key: {secret_key[:12]}... (hidden)")
    print(f"📋 Public Key: {public_key[:12]}... (hidden)")
    
    print("\n" + "=" * 60)
    
    if is_test_secret and is_test_public:
        print("✅ MODE: TEST MODE")
        print("\n💡 What this means:")
        print("   • NO real money will be charged")
        print("   • Use Yoco test card numbers for checkout")
        print("   • Perfect for development and testing")
        print("\n🧪 Test Card: 5200 0000 0000 1096 (any CVV, future expiry)")
        
    elif is_prod_secret and is_prod_public:
        print("⚠️  MODE: PRODUCTION MODE")
        print("\n💰 What this means:")
        print("   • REAL money WILL be charged")
        print("   • Real credit/debit cards required")
        print("   • Transactions will appear in your bank account")
        print("\n⚠️  WARNING: Only use this mode when ready for real payments!")
        
    else:
        print("❌ MODE: MIXED/INVALID")
        print("\n⚠️  Problem detected:")
        if is_test_secret:
            print("   • Secret key is TEST")
        elif is_prod_secret:
            print("   • Secret key is PRODUCTION")
        else:
            print("   • Secret key format is INVALID")
            
        if is_test_public:
            print("   • Public key is TEST")
        elif is_prod_public:
            print("   • Public key is PRODUCTION")
        else:
            print("   • Public key format is INVALID")
            
        print("\n💡 Both keys should be either test or production!")

print("\n" + "=" * 60)
print()
