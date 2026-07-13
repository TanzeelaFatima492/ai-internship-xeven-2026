import { NextRequest, NextResponse } from 'next/server'

// Sample restaurant menu data
const MENU_DATABASE = {
  biryani: {
    name: 'Chicken Biryani',
    price: '$12.99',
    description: 'Fragrant basmati rice with tender chicken, aromatic spices',
    source: 'Menu - Biryani',
  },
  kebab: {
    name: 'Seekh Kebab',
    price: '$10.99',
    description: 'Minced meat kebab with fresh herbs and spices, grilled to perfection',
    source: 'Menu - Kebabs',
  },
  karahi: {
    name: 'Chicken Karahi',
    price: '$11.99',
    description: 'Tender chicken in a traditional wok with tomatoes and peppers',
    source: 'Menu - Karahi',
  },
  nihari: {
    name: 'Beef Nihari',
    price: '$13.99',
    description: 'Slow-cooked beef in rich, aromatic gravy with special spices',
    source: 'Menu - Nihari',
  },
  samosa: {
    name: 'Vegetable Samosa',
    price: '$3.99',
    description: 'Crispy pastry filled with spiced potatoes and peas',
    source: 'Menu - Appetizers',
  },
  lassi: {
    name: 'Mango Lassi',
    price: '$4.99',
    description: 'Refreshing yogurt-based drink with fresh mango',
    source: 'Menu - Beverages',
  },
}

const POLICIES = {
  delivery: 'Free delivery on orders over $30. Delivery time: 30-45 minutes',
  hours: 'Open 11 AM - 11 PM, 7 days a week',
  returns: 'Satisfaction guaranteed. Food quality issues = full refund',
  reservation: 'Reservations available for groups of 4+. Call or book online',
}

const SPECIAL_OFFERS = {
  combo: 'Family Combo: Biryani + 2 Kebabs + Samosa + Lassi = $39.99 (Save $5!)',
  lunch: 'Lunch Special: Any main dish + rice + bread + drink = $9.99 (11 AM - 3 PM)',
  delivery: '20% off on orders above $25 using code BITEWISE20',
}

// Simple intent detection and response generation
function generateResponse(message: string): {
  message: string
  source?: string
  price?: string
} {
  const lowerMessage = message.toLowerCase()

  // Check for menu items
  for (const [key, item] of Object.entries(MENU_DATABASE)) {
    if (lowerMessage.includes(key) || lowerMessage.includes(item.name.toLowerCase())) {
      return {
        message: `${item.name}: ${item.description}. We carefully select premium ingredients and cook each dish to perfection. Highly recommended!`,
        source: item.source,
        price: item.price,
      }
    }
  }

  // Check for prices
  if (
    lowerMessage.includes('price') ||
    lowerMessage.includes('how much') ||
    lowerMessage.includes('cost')
  ) {
    return {
      message: `Our prices range from $3.99 for appetizers to $13.99 for premium main courses. We offer great value for authentic Pakistani cuisine. Would you like to know about a specific dish?`,
    }
  }

  // Check for offers
  if (
    lowerMessage.includes('offer') ||
    lowerMessage.includes('discount') ||
    lowerMessage.includes('special') ||
    lowerMessage.includes('deal')
  ) {
    const offers = Object.values(SPECIAL_OFFERS).join('\n\n')
    return {
      message: `Great question! Here are our current offers:\n\n${offers}\n\nThese are available for a limited time. Would you like more details?`,
    }
  }

  // Check for policies
  if (
    lowerMessage.includes('delivery') ||
    lowerMessage.includes('hours') ||
    lowerMessage.includes('open') ||
    lowerMessage.includes('return') ||
    lowerMessage.includes('refund') ||
    lowerMessage.includes('reservation')
  ) {
    let policyResponse = ''

    if (lowerMessage.includes('delivery')) {
      policyResponse += `Delivery: ${POLICIES.delivery}\n\n`
    }
    if (lowerMessage.includes('hour') || lowerMessage.includes('open')) {
      policyResponse += `Hours: ${POLICIES.hours}\n\n`
    }
    if (lowerMessage.includes('return') || lowerMessage.includes('refund')) {
      policyResponse += `Quality Guarantee: ${POLICIES.returns}\n\n`
    }
    if (lowerMessage.includes('reservation')) {
      policyResponse += `Reservations: ${POLICIES.reservation}\n\n`
    }

    if (!policyResponse) {
      policyResponse = `Delivery: ${POLICIES.delivery}\nHours: ${POLICIES.hours}\nReservations: ${POLICIES.reservation}`
    }

    return {
      message: policyResponse.trim(),
    }
  }

  // Check for menu browsing
  if (
    lowerMessage.includes('menu') ||
    lowerMessage.includes('what') ||
    lowerMessage.includes('recommend') ||
    lowerMessage.includes('popular')
  ) {
    const menuItems = Object.values(MENU_DATABASE)
      .slice(0, 3)
      .map((item) => `• ${item.name} (${item.price})`)
      .join('\n')

    return {
      message: `I'd love to help! Here are some of our popular dishes:\n\n${menuItems}\n\nEach is prepared with fresh ingredients and authentic Pakistani spices. What sounds good to you?`,
    }
  }

  // Default response
  return {
    message: `I'm BiteWise, your Pakistani restaurant AI assistant! I can help you with:\n\n• Menu items and descriptions\n• Pricing and specials\n• Delivery information\n• Restaurant hours\n• Reservations and policies\n\nWhat can I help you with today?`,
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { message, userId } = body

    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { error: 'Invalid message' },
        { status: 400 }
      )
    }

    // Generate AI response
    const response = generateResponse(message)

    // Add small delay to simulate thinking
    await new Promise((resolve) => setTimeout(resolve, 500))

    return NextResponse.json({
      message: response.message,
      source: response.source,
      price: response.price,
    })
  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      { error: 'Failed to process message' },
      { status: 500 }
    )
  }
}
