import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { mainKeyword, targetAudience, contentType, numArticles } = body

    const response = await fetch('http://localhost:8001/content-plan/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${request.headers.get('authorization')?.split(' ')[1]}`
      },
      body: JSON.stringify({
        main_keyword: mainKeyword,
        target_audience: targetAudience,
        content_type: contentType,
        num_articles: numArticles
      })
    })

    if (!response.ok) {
      throw new Error('Error generando plan de contenido')
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error('Error:', error)
    return NextResponse.json(
      { error: 'Error generando plan de contenido' },
      { status: 500 }
    )
  }
} 