// Configuration for AI service
// TODO: Update this URL when deploying Vertex AI agent to Google Cloud
const AI_SERVICE_URL = import.meta.env.VITE_AI_SERVICE_URL || 'http://localhost:8000/ai/query'

/**
 * Process user query through AI Race Engineer
 * 
 * Integration with Vertex AI + RAG:
 * - Endpoint should accept POST requests with query and context
 * - Expected request format:
 *   {
 *     "query": "string",
 *     "context": {
 *       "track": "string",
 *       "lap": number,
 *       "speed": number,
 *       "sector": number,
 *       "tireLife": number,
 *       "vehicle": number
 *     }
 *   }
 * 
 * - Expected response format:
 *   {
 *     "response": "string",
 *     "type": "info" | "warning" | "success" | "error" | "neutral",
 *     "confidence": number (0-1),
 *     "sources": string[] (optional)
 *   }
 */
export const processQuery = async (query, raceData) => {
    try {
        // Call the AI service endpoint (Vertex AI + RAG)
        const response = await fetch(AI_SERVICE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                context: {
                    track: raceData?.track || 'barber',
                    lap: raceData?.lap || 15,
                    speed: raceData?.speed || 0,
                    sector: raceData?.sector || 1,
                    tireLife: raceData?.tireLife || 85,
                    vehicle: raceData?.vehicle || null
                }
            })
        })

        if (!response.ok) {
            throw new Error(`AI service returned ${response.status}`)
        }

        const data = await response.json()
        
        return {
            text: data.response,
            type: data.type || 'neutral',
            confidence: data.confidence || 0.5,
            sources: data.sources || []
        }
    } catch (error) {
        console.error('AI service error:', error)
        
        // Fallback to local processing if AI service is unavailable
        return processQueryLocal(query, raceData)
    }
}

// Fallback local processing
const processQueryLocal = (query, raceData) => {
    const lowerQuery = query.toLowerCase()

    if (lowerQuery.includes('tire') || lowerQuery.includes('wear')) {
        return {
            text: `Based on current telemetry at lap ${raceData?.lap || 15}, tire life is at ${raceData?.tireLife || 85}%. Monitor degradation closely and consider pit strategy.`,
            type: 'warning'
        }
    }

    if (lowerQuery.includes('gap') || lowerQuery.includes('leader') || lowerQuery.includes('position')) {
        return {
            text: "Gap analysis shows you're competitive in Sector 2. Maintain your pace and focus on consistency.",
            type: 'success'
        }
    }

    if (lowerQuery.includes('strategy') || lowerQuery.includes('pit')) {
        const currentLap = raceData?.lap || 15
        const pitWindow = currentLap < 15 ? '12-15' : '18-22'
        return {
            text: `Optimal pit window is laps ${pitWindow}. Monitor tire degradation and fuel levels. Track position is crucial.`,
            type: 'info'
        }
    }

    if (lowerQuery.includes('weather') || lowerQuery.includes('rain') || lowerQuery.includes('temperature')) {
        return {
            text: "Track temperature is optimal for tire performance. No weather concerns at this time.",
            type: 'info'
        }
    }

    if (lowerQuery.includes('speed') || lowerQuery.includes('fast') || lowerQuery.includes('slow')) {
        return {
            text: `Current speed: ${raceData?.speed || 0} km/h. Focus on maintaining momentum through corners and optimizing exit speed.`,
            type: 'neutral'
        }
    }

    if (lowerQuery.includes('sector')) {
        return {
            text: `Currently in Sector ${raceData?.sector || 1}. Analyze sector times to identify improvement opportunities.`,
            type: 'neutral'
        }
    }

    if (lowerQuery.includes('track') || lowerQuery.includes('circuit')) {
        return {
            text: "This circuit rewards smooth driving and precise braking. Focus on consistency and tire management.",
            type: 'info'
        }
    }

    return {
        text: "I'm analyzing that data. I can help with strategy, tire management, lap times, track information, and performance analysis. What would you like to know?",
        type: 'neutral'
    }
}
