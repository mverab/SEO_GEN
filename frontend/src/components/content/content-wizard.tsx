"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Steps } from "@/components/ui/steps"
import { BasicInfoStep } from "./steps/basic-info"
import { KeywordsStep } from "./steps/keywords"
import { ReferencesStep } from "./steps/references"
import { PreviewStep } from "./steps/preview"

const steps = [
  "Datos Básicos",
  "Keywords y Tono",
  "Referencias",
  "Preview"
]

export function ContentWizard() {
  const [currentStep, setCurrentStep] = useState(0)

  const handleNext = () => {
    setCurrentStep((prev) => Math.min(prev + 1, steps.length - 1))
  }

  const handlePrev = () => {
    setCurrentStep((prev) => Math.max(prev - 1, 0))
  }

  return (
    <div className="space-y-8">
      <Steps
        steps={steps}
        currentStep={currentStep}
        onChange={setCurrentStep}
      />

      <div className="min-h-[400px] py-8">
        {currentStep === 0 && <BasicInfoStep />}
        {currentStep === 1 && <KeywordsStep />}
        {currentStep === 2 && <ReferencesStep />}
        {currentStep === 3 && <PreviewStep />}
      </div>

      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          onClick={handlePrev}
          disabled={currentStep === 0}
        >
          Anterior
        </Button>
        <Button
          onClick={currentStep === steps.length - 1 ? undefined : handleNext}
          disabled={currentStep === steps.length - 1}
        >
          {currentStep === steps.length - 1 ? "Generar" : "Siguiente"}
        </Button>
      </div>
    </div>
  )
} 