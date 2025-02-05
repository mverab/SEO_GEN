import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface AIMetricsProps {
  score: number
  wasImproved: boolean
  features?: Record<string, any>
}

export function AIMetrics({ score, wasImproved, features }: AIMetricsProps) {
  const scorePercentage = score * 100
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>Métricas de IA</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm font-medium">Score de IA</span>
              <span className="text-sm text-muted-foreground">{scorePercentage.toFixed(1)}%</span>
            </div>
            <Progress value={scorePercentage} />
          </div>
          
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${wasImproved ? 'bg-yellow-500' : 'bg-green-500'}`} />
            <span className="text-sm">
              {wasImproved ? 'Contenido mejorado' : 'Contenido original'}
            </span>
          </div>
          
          {features && (
            <div className="mt-4">
              <h4 className="text-sm font-medium mb-2">Características</h4>
              <div className="space-y-2">
                {Object.entries(features).map(([key, value]) => (
                  <div key={key} className="flex justify-between text-sm">
                    <span className="text-muted-foreground">{key}</span>
                    <span>{typeof value === 'number' ? `${(value * 100).toFixed(1)}%` : value}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
} 