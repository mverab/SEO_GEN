import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Steps } from "@/components/ui/steps"
import { ContentWizard } from "@/components/content/content-wizard"

export default function NewContentPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Nuevo Contenido</h1>
        <Button variant="outline">Cancelar</Button>
      </div>

      <Card className="p-6">
        <ContentWizard />
      </Card>
    </div>
  )
} 