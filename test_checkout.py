#!/usr/bin/env python
"""
Test script to verify checkout functionality with Vault API
Tests with card: 4196591200000002 (3DS Challenge Card)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_platform.settings')
django.setup()

from events.models import Event, TicketType, Order, CustomerVaultProfile, SavedPaymentMethod
from events.services.cobalt_payment import CobaltPaymentGateway
from django.utils import timezone
from decimal import Decimal
import json

def test_new_card_payment():
    """Test payment with new card (no saving)"""
    print("\n" + "="*60)
    print("TEST 1: New Card Payment (Without Saving)")
    print("="*60)
    
    # Find a test event
    event = Event.objects.filter(status='published').first()
    if not event:
        print("❌ No published events found")
        return False
    
    print(f"✓ Using event: {event.title}")
    
    # Get ticket type
    ticket_type = event.ticket_types.first()
    if not ticket_type:
        print("❌ No ticket types found")
        return False
    
    print(f"✓ Ticket type: {ticket_type.name} (${ticket_type.price})")
    
    # Prepare payment data
    gateway = CobaltPaymentGateway()
    
    # Test card data
    card_data = {
        'pan': '4196591200000002',  # 3DS Challenge card
        'exp_date': '1225',  # 12/25
        'cvv2': '123',
        'card_holder': 'TEST USER'
    }
    
    # 3DS params (simulated browser data)
    three_ds_params = {
        'deviceChannel': 'browser',
        'browserJavaEnabled': False,
        'browserJavascriptEnabled': True,
        'browserLanguage': 'es-CR',
        'browserColorDepth': 24,
        'browserScreenHeight': 1080,
        'browserScreenWidth': 1920,
        'browserTZ': 360,
        'browserUserAgent': 'Mozilla/5.0 Test',
        'challengeWindowSize': '05',
        'browserIP': '192.168.1.1'
    }
    
    print("\n📤 Sending payment request to Cobalt...")
    print(f"   Amount: ${ticket_type.price}")
    print(f"   Card: {card_data['pan'][:4]}...{card_data['pan'][-4:]}")
    
    try:
        result = gateway.process_sale(
            amount=float(ticket_type.price),
            pan=card_data['pan'],
            exp_date=card_data['exp_date'],
            cvv2=card_data['cvv2'],
            card_holder=card_data['card_holder'],
            three_ds_params=three_ds_params,
            webhook='https://passclub.online/payments/webhook/',
            return_url='https://passclub.online/order/TEST-123/',
            metas={'order_id': 'TEST-001', 'event': event.slug}
        )
        
        print(f"\n📥 Response received:")
        print(f"   Success: {result.get('success')}")
        print(f"   Status: {result.get('status')}")
        print(f"   TX ID: {result.get('transaction_id')}")
        print(f"   Message: {result.get('message', 'N/A')}")
        
        if result.get('status') == 'authenticating':
            print(f"\n🔐 3DS Challenge URL:")
            print(f"   {result.get('authentication_url', 'N/A')}")
            print(f"\n   ⚠️  In production, redirect user to this URL")
            print(f"   ⚠️  User will enter OTP: 123456")
            print(f"   ⚠️  Result will be sent to webhook")
        
        if result.get('success') or result.get('status') == 'authenticating':
            print("\n✅ TEST 1 PASSED: Payment request successful")
            return True
        else:
            print(f"\n❌ TEST 1 FAILED: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"\n❌ TEST 1 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_order_creation_with_vault_fields():
    """Test that Order model accepts vault fields"""
    print("\n" + "="*60)
    print("TEST 2: Order Creation with Vault Fields")
    print("="*60)
    
    event = Event.objects.filter(status='published').first()
    if not event:
        print("❌ No published events found")
        return False
    
    try:
        order = Order.objects.create(
            event=event,
            customer_email='test_vault@example.com',
            customer_name='Test Vault User',
            customer_phone='8888-8888',
            total_amount=Decimal('50.00'),
            status='pending',
            payment_method='card',
            vault_customer_id=12345,  # Test vault fields
            used_saved_card=False,
            saved_card_token=''
        )
        
        print(f"✓ Order created: {order.order_number}")
        print(f"✓ vault_customer_id: {order.vault_customer_id}")
        print(f"✓ used_saved_card: {order.used_saved_card}")
        print(f"✓ saved_card_token: '{order.saved_card_token}'")
        
        # Clean up
        order.delete()
        
        print("\n✅ TEST 2 PASSED: Order creation with vault fields works")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 2 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_vault_profile_creation():
    """Test CustomerVaultProfile model"""
    print("\n" + "="*60)
    print("TEST 3: Vault Profile Creation")
    print("="*60)
    
    try:
        # Create profile
        profile = CustomerVaultProfile.objects.create(
            customer_email='test_profile@example.com',
            vault_customer_id=99999,
            vault_reference='TEST-REF-123',
            name='Test',
            first_surname='Profile',
            second_surname='User',
            doc_id_type='C',
            doc_id='123456789'
        )
        
        print(f"✓ Profile created: {profile.customer_email}")
        print(f"✓ vault_customer_id: {profile.vault_customer_id}")
        print(f"✓ vault_reference: {profile.vault_reference}")
        
        # Create saved card
        saved_card = SavedPaymentMethod.objects.create(
            customer_profile=profile,
            vault_card_id=88888,
            customer_token='TEST-TOKEN-ABC123',
            card_brand='Visa',
            last_four='0002',
            exp_month='12',
            exp_year='2025',
            card_holder='TEST USER',
            alias='Visa •••• 0002',
            is_default=True
        )
        
        print(f"✓ Saved card created: {saved_card.alias}")
        print(f"✓ customer_token: {saved_card.customer_token}")
        print(f"✓ is_default: {saved_card.is_default}")
        
        # Clean up
        saved_card.delete()
        profile.delete()
        
        print("\n✅ TEST 3 PASSED: Vault profile and saved card creation works")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 3 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       Vault API Integration Test Suite                    ║")
    print("║       Testing with card: 4196591200000002                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    results = []
    
    # Run tests
    results.append(("Database Schema", test_order_creation_with_vault_fields()))
    results.append(("Vault Models", test_vault_profile_creation()))
    results.append(("Payment Gateway", test_new_card_payment()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n📋 Next Steps:")
        print("   1. Deploy to production (migrations will run automatically)")
        print("   2. Test on passclub.online with real checkout")
        print("   3. Use card 4196591200000002 and OTP: 123456")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("   Review errors above and fix before deploying")
    
    print("\n")


if __name__ == '__main__':
    main()

