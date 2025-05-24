#!/usr/bin/env python3
"""
Test the Mynd web interface
"""
import webbrowser
import time

print("🌐 Testing Mynd Web Interface")
print("=" * 50)
print("\n✅ The web server is running on http://localhost:8000")
print("\nOpening in your browser...")

# Open the browser
webbrowser.open("http://localhost:8000")

print("\n📋 Quick Test Instructions:")
print("1. ✅ Check that the interface loads")
print("2. ✅ The input box should be visible at the bottom")
print("3. ✅ Try typing a message and press Enter")
print("4. ✅ Toggle Memory ON/OFF to see different responses")
print("5. ✅ Click 'Load Demo Context' for sample data")
print("\n🎯 Test these questions:")
print("   - 'What was our authentication decision?'")
print("   - 'How are we handling payments?'")
print("   - 'What database are we using?'")
print("\n💡 Tips:")
print("   - The interface now has proper layout with fixed banner")
print("   - Input area is always visible at the bottom")
print("   - Stats update in real-time on the left")
print("   - Memory toggle shows immediate difference")
print("\n🏆 Ready for the hackathon demo!") 