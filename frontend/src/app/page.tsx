import Link from "next/link"
import { Button } from "../components/ui/button"

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] px-4">
      <div className="max-w-3xl mx-auto text-center space-y-8">
        <h1 className="text-4xl sm:text-6xl font-bold tracking-tight">
          Genera contenido SEO que{" "}
          <span className="text-primary">convierte</span>
        </h1>
        
        <p className="text-xl text-muted-foreground">
          Automatiza tu estrategia de contenido con IA. Investiga keywords,
          planifica contenido y genera artículos optimizados para SEO.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/keyword-research">
            <Button size="lg" className="w-full sm:w-auto">
              Empezar ahora
            </Button>
          </Link>
          <Link href="/docs">
            <Button size="lg" variant="outline" className="w-full sm:w-auto">
              Ver documentación
            </Button>
          </Link>
        </div>

        <div className="grid sm:grid-cols-3 gap-8 pt-12">
          <div className="rounded-lg border bg-card p-6">
            <h3 className="font-semibold mb-2">Investigación de Keywords</h3>
            <p className="text-sm text-muted-foreground">
              Encuentra las mejores keywords con análisis de volumen y competencia.
            </p>
          </div>

          <div className="rounded-lg border bg-card p-6">
            <h3 className="font-semibold mb-2">Planificación de Contenido</h3>
            <p className="text-sm text-muted-foreground">
              Crea planes de contenido optimizados basados en tus keywords objetivo.
            </p>
          </div>

          <div className="rounded-lg border bg-card p-6">
            <h3 className="font-semibold mb-2">Generación con IA</h3>
            <p className="text-sm text-muted-foreground">
              Genera contenido único y optimizado para SEO con inteligencia artificial.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
} 