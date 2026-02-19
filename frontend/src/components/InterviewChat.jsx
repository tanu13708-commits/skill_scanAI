import { useState, useRef, useEffect } from 'react'
import { startInterview, submitAnswer } from '../services'

const InterviewChat = ({ resumeData, onComplete }) => {
  const [messages, setMessages] = useState([])
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [userInput, setUserInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [interviewStarted, setInterviewStarted] = useState(false)
  const [questionNumber, setQuestionNumber] = useState(0)
  const [totalQuestions] = useState(5)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleStartInterview = async () => {
    setIsLoading(true)
    try {
      const response = await startInterview({ resumeData })
      setInterviewStarted(true)
      setQuestionNumber(1)
      setCurrentQuestion(response.question)
      setMessages([
        {
          type: 'system',
          content: 'Welcome to your Technical Interview. I will ask you a series of questions based on your resume and skills. Take your time to provide thoughtful answers.',
        },
        {
          type: 'ai',
          content: response.question,
        },
      ])
    } catch (error) {
      setMessages([
        {
          type: 'error',
          content: error.message || 'Failed to start interview. Please try again.',
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmitAnswer = async (e) => {
    e.preventDefault()
    if (!userInput.trim() || isLoading) return

    const answer = userInput.trim()
    setUserInput('')
    setIsLoading(true)

    // Add user message
    setMessages((prev) => [
      ...prev,
      { type: 'user', content: answer },
    ])

    try {
      const response = await submitAnswer({
        question: currentQuestion,
        answer,
        questionNumber,
      })

      // Add evaluation feedback
      if (response.score !== undefined || response.feedback) {
        setMessages((prev) => [
          ...prev,
          {
            type: 'evaluation',
            score: response.score,
            feedback: response.feedback,
          },
        ])
      }

      if (response.isComplete) {
        setMessages((prev) => [
          ...prev,
          {
            type: 'system',
            content: 'Technical interview completed! Moving to the next round...',
          },
        ])
        onComplete?.(response)
      } else {
        setQuestionNumber((prev) => prev + 1)
        setCurrentQuestion(response.nextQuestion)
        setMessages((prev) => [
          ...prev,
          { type: 'ai', content: response.nextQuestion },
        ])
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          type: 'error',
          content: error.message || 'Failed to submit answer. Please try again.',
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 80) return { text: 'text-green-400', bg: 'bg-green-500', border: 'border-green-500/30' }
    if (score >= 60) return { text: 'text-yellow-400', bg: 'bg-yellow-500', border: 'border-yellow-500/30' }
    return { text: 'text-red-400', bg: 'bg-red-500', border: 'border-red-500/30' }
  }

  const renderMessage = (message, index) => {
    const baseClasses = 'max-w-[80%] rounded-2xl px-4 py-3 mb-4'
    
    switch (message.type) {
      case 'ai':
        return (
          <div key={index} className="flex justify-start">
            <div className="flex gap-3 max-w-[80%]">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div className={`${baseClasses} bg-slate-700 text-white`}>
                <p className="whitespace-pre-wrap">{message.content}</p>
              </div>
            </div>
          </div>
        )
      case 'user':
        return (
          <div key={index} className="flex justify-end">
            <div className={`${baseClasses} bg-blue-600 text-white`}>
              <p className="whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        )
      case 'evaluation':
        const scoreColors = getScoreColor(message.score || 0)
        return (
          <div key={index} className="flex justify-start mb-4">
            <div className="flex gap-3 max-w-[85%]">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center flex-shrink-0">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className={`rounded-2xl px-5 py-4 bg-slate-800/80 border ${scoreColors.border}`}>
                {/* Score Display */}
                <div className="flex items-center gap-4 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-slate-400 text-sm">Score:</span>
                    <span className={`text-2xl font-bold ${scoreColors.text}`}>
                      {message.score || 0}/100
                    </span>
                  </div>
                  <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden min-w-[100px]">
                    <div 
                      className={`h-full ${scoreColors.bg} transition-all duration-500`}
                      style={{ width: `${message.score || 0}%` }}
                    />
                  </div>
                </div>
                {/* Feedback */}
                {message.feedback && (
                  <div className="border-t border-slate-700 pt-3">
                    <p className="text-sm text-slate-400 mb-1">Feedback:</p>
                    <p className="text-white text-sm whitespace-pre-wrap">{message.feedback}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )
      case 'system':
        return (
          <div key={index} className="flex justify-center mb-4">
            <div className="px-4 py-2 rounded-full bg-slate-700/50 text-slate-400 text-sm">
              {message.content}
            </div>
          </div>
        )
      case 'error':
        return (
          <div key={index} className="flex justify-center mb-4">
            <div className="px-4 py-2 rounded-lg bg-red-500/10 border border-red-500/50 text-red-400 text-sm">
              {message.content}
            </div>
          </div>
        )
      default:
        return null
    }
  }

  if (!interviewStarted) {
    return (
      <div className="flex flex-col items-center justify-center h-full py-16">
        <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-blue-500/25">
          <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-white mb-3">Ready to Begin?</h2>
        <p className="text-slate-400 text-center max-w-md mb-8">
          You will be asked {totalQuestions} technical questions based on your resume and skills.
          Take your time to provide detailed answers.
        </p>
        <button
          onClick={handleStartInterview}
          disabled={isLoading}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-xl transition-all duration-200 hover:shadow-lg hover:shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {isLoading ? (
            <>
              <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Starting...
            </>
          ) : (
            <>
              Start Interview
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </>
          )}
        </button>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* Progress Bar */}
      <div className="px-4 py-3 border-b border-slate-700">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-slate-400">Question {questionNumber} of {totalQuestions}</span>
          <span className="text-sm text-slate-400">{Math.round((questionNumber / totalQuestions) * 100)}% Complete</span>
        </div>
        <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-500"
            style={{ width: `${(questionNumber / totalQuestions) * 100}%` }}
          />
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((message, index) => renderMessage(message, index))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div className="bg-slate-700 rounded-2xl px-4 py-3">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmitAnswer} className="p-4 border-t border-slate-700">
        <div className="flex gap-3">
          <textarea
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSubmitAnswer(e)
              }
            }}
            placeholder="Type your answer... (Press Enter to send, Shift+Enter for new line)"
            className="flex-1 px-4 py-3 rounded-xl bg-slate-800 border border-slate-600 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows={2}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!userInput.trim() || isLoading}
            className="px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </form>
    </div>
  )
}

export default InterviewChat
