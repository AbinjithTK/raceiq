import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceArea, ReferenceLine } from 'recharts'
import './Card.css'

const StrategyChart = ({ currentLap, totalLaps }) => {
    // Mock data for strategy simulation
    const data = Array.from({ length: totalLaps }, (_, i) => {
        const lap = i + 1
        // Simulate tire degradation curve
        const tireLife = Math.max(0, 100 - (lap * 3.5) - (Math.random() * 2))
        return {
            lap,
            tireLife: Math.round(tireLife),
            pitWindow: lap >= 12 && lap <= 16 ? 100 : 0
        }
    })

    return (
        <div className="card">
            <div className="card-title">
                <span>📊</span> Real-Time Strategy
            </div>
            <div style={{ width: '100%', height: 200 }}>
                <ResponsiveContainer>
                    <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                        <XAxis
                            dataKey="lap"
                            stroke="#A1A1AA"
                            fontSize={12}
                            tickLine={false}
                        />
                        <YAxis
                            stroke="#A1A1AA"
                            fontSize={12}
                            tickLine={false}
                            domain={[0, 100]}
                        />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: '#101112',
                                border: '1px solid rgba(255,255,255,0.1)',
                                borderRadius: '8px'
                            }}
                            itemStyle={{ color: '#fff' }}
                        />
                        <ReferenceArea x1={12} x2={16} strokeOpacity={0.3} fill="#00f3ff" fillOpacity={0.1} />
                        <ReferenceLine x={currentLap} stroke="#ffaa00" strokeDasharray="3 3" label={{ value: 'Current', fill: '#ffaa00', fontSize: 10 }} />
                        <Line
                            type="monotone"
                            dataKey="tireLife"
                            stroke="#c96287"
                            strokeWidth={2}
                            dot={false}
                            activeDot={{ r: 4, fill: '#fff' }}
                            name="Tire Life %"
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
            <div className="mt-4 text-center">
                <p className="text-sm text-gray-400">Optimal Pit Window: <span className="text-cyan-400 font-bold">Lap 12-16</span></p>
            </div>
        </div>
    )
}

export default StrategyChart
