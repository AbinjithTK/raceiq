import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { processQuery } from '../lib/ai-logic'
import { Send, X, MessageSquare, Mic } from 'lucide-react'
import './Card.css'

const AIEngineer = ({ raceData }) => {
    const [isOpen, setIsOpen] = useState(false)
    const [messages, setMessages] = useState([
        { text: "Race Engineer online. I'm monitoring your telemetry. Ask me anything.", sender: 'ai', type: 'neutral' }
    ])
    const [input, setInput] = useState('')
    const [isTyping, setIsTyping] = useState(false)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const handleSend = async (e) => {
        e.preventDefault()
        if (!input.trim()) return

        const userMsg = { text: input, sender: 'user' }
        setMessages(prev => [...prev, userMsg])
        setInput('')
        setIsTyping(true)

        try {
            // Call AI with race context
            const response = await processQuery(userMsg.text, raceData)
            setMessages(prev => [...prev, {
                text: response.text,
                sender: 'ai',
                type: response.type,
                confidence: response.confidence
            }])
        } catch (error) {
            console.error('AI error:', error)
            setMessages(prev => [...prev, {
                text: "I'm having trouble processing that right now. Please try again.",
                sender: 'ai',
                type: 'error'
            }])
        } finally {
            setIsTyping(false)
        }
    }

    return (
        <>
            {/* Floating Toggle Button */}
            <motion.button
                className="fixed bottom-6 right-6 z-50 p-4 rounded-full bg-purple-600 text-white shadow-lg hover:bg-purple-700 focus:outline-none"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setIsOpen(!isOpen)}
                style={{ boxShadow: '0 0 20px rgba(189, 0, 255, 0.5)' }}
            >
                {isOpen ? <X size={24} /> : <MessageSquare size={24} />}
            </motion.button>

            {/* Chat Panel */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 50, scale: 0.9 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 50, scale: 0.9 }}
                        className="fixed bottom-24 right-6 z-50 w-80 md:w-96 h-[500px] flex flex-col rounded-xl overflow-hidden"
                        style={{
                            background: 'rgba(18, 18, 24, 0.95)',
                            backdropFilter: 'blur(20px)',
                            border: '1px solid rgba(189, 0, 255, 0.3)',
                            boxShadow: '0 10px 40px rgba(0, 0, 0, 0.5)'
                        }}
                    >
                        {/* Header */}
                        <div className="p-4 bg-purple-900/20 border-b border-purple-500/20 flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                                <h3 className="font-bold text-white">AI Race Engineer</h3>
                            </div>
                            <div className="text-xs text-purple-300">ONLINE</div>
                        </div>

                        {/* Messages */}
                        <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
                            {messages.map((msg, idx) => (
                                <div
                                    key={idx}
                                    className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                                >
                                    <div
                                        className={`max-w-[80%] p-3 rounded-lg text-sm ${msg.sender === 'user'
                                            ? 'bg-purple-600 text-white rounded-br-none'
                                            : 'bg-gray-800 text-gray-200 rounded-bl-none border border-gray-700'
                                            }`}
                                    >
                                        {msg.text}
                                    </div>
                                </div>
                            ))}
                            {isTyping && (
                                <div className="flex justify-start">
                                    <div className="bg-gray-800 p-3 rounded-lg rounded-bl-none border border-gray-700 flex gap-1">
                                        <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
                                        <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                                        <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input */}
                        <form onSubmit={handleSend} className="p-4 bg-black/20 border-t border-purple-500/20 flex gap-2">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Ask about tires, strategy..."
                                className="flex-1 bg-gray-900/50 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500 transition-colors"
                            />
                            <button
                                type="submit"
                                className="p-2 bg-purple-600 rounded-lg text-white hover:bg-purple-700 transition-colors"
                            >
                                <Send size={18} />
                            </button>
                        </form>
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    )
}

export default AIEngineer
