import { NextResponse } from "next/server"
import type { KeywordResearchResponse } from "@/types/api"

export async function POST(request: Request) {
  try {
    const { keyword } = await request.json()

    // TODO: Integrar con API real de SEO
    // Por ahora retornamos datos de ejemplo
    const mockResponse: KeywordResearchResponse = {
      topic_map: [
        {
          id: "1",
          label: keyword,
          children: [
            { id: "1.1", label: `${keyword} guía` },
            { id: "1.2", label: `${keyword} tutorial` },
            { id: "1.3", label: `${keyword} ejemplos` },
          ],
        },
      ],
      seo_potential: [
        {
          label: "Volumen de Búsqueda",
          value: Math.floor(Math.random() * 10000),
          description: "Búsquedas mensuales promedio",
        },
        {
          label: "Dificultad",
          value: Math.floor(Math.random() * 100),
          description: "Nivel de competencia",
        },
        {
          label: "Intención",
          value: "Informacional",
          description: "Tipo de intención de búsqueda",
        },
      ],
    }

    return NextResponse.json(mockResponse)
  } catch (error) {
    console.error("Error:", error)
    return NextResponse.json(
      { error: "Error procesando la solicitud" },
      { status: 500 }
    )
  }
} 